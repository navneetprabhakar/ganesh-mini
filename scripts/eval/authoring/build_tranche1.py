#!/usr/bin/env python3
"""Build and audit private development tranche 1 deterministically."""

from __future__ import annotations

import json
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.eval.contracts import (
    CANDIDATE_PATH,
    LANGUAGE_FAMILY,
    sha256_object,
    sha256_text,
    validate_task,
    write_json,
)

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "eval/private/development/tranche1"
MANIFEST = ROOT / "manifests/evaluation/private/development-tranche1.json"
OVERLAP = ROOT / "manifests/evaluation/private/development-tranche1-overlap.json"
RUNTIME = {
    "go": "go-1.22.12",
    "java": "java-21.0.11",
    "javascript": "javascript-node-22.23.2",
    "typescript": "typescript-5.5.4-node-22",
    "python": "python-3.11.15",
    "rust": "rust-1.85.0",
}
KINDS = {
    "go": ("generation", "generation", "generation", "repair", "repair"),
    "java": ("generation", "generation", "repair", "repair", "repair"),
    "javascript": ("generation", "generation", "generation", "repair", "repair"),
    "typescript": ("generation", "generation", "repair", "repair", "repair"),
    "python": ("generation", "generation", "generation", "repair", "repair"),
    "rust": ("generation", "generation", "repair", "repair", "repair"),
}
SLUGS = ("collapse-runs", "bounded-prefix-sum", "split-escaped", "keep-last", "clamp-window")
BEHAVIOR = {
    "collapse-runs": "Return one value for each maximal adjacent run. Preserve order, do not mutate input, and return a non-null empty collection for empty input.",
    "bounded-prefix-sum": "Return the exact sum only when every prefix sum, including the initial zero, remains within the inclusive symmetric bound. Reject a negative bound and return the failure value on arithmetic overflow.",
    "split-escaped": "Split on unescaped commas. Backslash may escape only comma or backslash. Preserve empty fields. Return the failure value for another escape or a trailing backslash.",
    "keep-last": "Keep only the last occurrence of each exact string while preserving the retained elements' original order. Do not mutate input and return a non-null empty collection.",
    "clamp-window": "Reject negative size or length. Clamp start into the inclusive range from zero to length, then return the half-open window ending at the smaller of start plus size and length, without arithmetic overflow.",
}


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def s(reference: str, bad: str, test: str, bad_label: str) -> dict[str, str]:
    return {"reference": reference, "bad": bad, "test": test, "bad_label": bad_label}


LANG: dict[str, dict[str, dict[str, str]]] = {
"go": {
"collapse-runs": s(
r"""package solution

func CollapseRuns(values []int) []int {
 out:=make([]int,0,len(values))
 for _,v:=range values { if len(out)==0 || out[len(out)-1]!=v { out=append(out,v) } }
 return out
}
""",
r"""package solution
func CollapseRuns(values []int) []int { if len(values)==0{return nil}; return values[:1] }
""",
r"""package solution
import "testing"
func TestCollapse(t *testing.T){in:=[]int{2,2,1,1,3,2,2};g:=CollapseRuns(in);w:=[]int{2,1,3,2};if len(g)!=len(w){t.Fatal(g)};for i:=range w{if g[i]!=w[i]{t.Fatal(g)}};if CollapseRuns(nil)==nil{t.Fatal("nil")};if in[1]!=2{t.Fatal("mutated")}}
""", "nil-empty-and-truncation"),
"bounded-prefix-sum": s(
"""package solution
func BoundedPrefixSum(values []int64,bound int64)(int64,bool){if bound<0{return 0,false};var x int64;for _,v:=range values{if (v>0&&x>int64(^uint64(0)>>1)-v)||(v<0&&x<(-int64(^uint64(0)>>1)-1)-v){return 0,false};x+=v;if x>bound||x < -bound{return 0,false}};return x,true}
""",
"""package solution
func BoundedPrefixSum(values []int64,bound int64)(int64,bool){var x int64;for _,v:=range values{x+=v};return x,x<=bound&&x>=-bound}
""",
"""package solution
import "testing"
func TestBounded(t *testing.T){if x,ok:=BoundedPrefixSum([]int64{3,-2},3);!ok||x!=1{t.Fatal(x,ok)};if _,ok:=BoundedPrefixSum([]int64{5,-5},4);ok{t.Fatal("prefix")};if _,ok:=BoundedPrefixSum([]int64{9223372036854775807,1},9223372036854775807);ok{t.Fatal("overflow")};if _,ok:=BoundedPrefixSum(nil,-1);ok{t.Fatal("bound")}}
""", "final-only-wrapping-sum"),
"split-escaped": s(
"""package solution
func SplitEscaped(x string)([]string,bool){out:=[]string{};cur:=[]byte{};esc:=false;for i:=0;i<len(x);i++{c:=x[i];if esc{if c!=','&&c!='\\\\'{return nil,false};cur=append(cur,c);esc=false}else if c=='\\\\'{esc=true}else if c==','{out=append(out,string(cur));cur=nil}else{cur=append(cur,c)}};if esc{return nil,false};out=append(out,string(cur));return out,true}
""",
"""package solution
import "strings"
func SplitEscaped(x string)([]string,bool){return strings.Split(x,","),true}
""",
"""package solution
import "testing"
func TestSplit(t *testing.T){g,ok:=SplitEscaped("a\\\\,b,,c\\\\\\\\d");w:=[]string{"a,b","","c\\\\d"};if !ok||len(g)!=3{t.Fatal(g,ok)};for i:=range w{if g[i]!=w[i]{t.Fatal(g)}};for _,x:=range []string{"a\\\\q","a\\\\"}{if _,ok:=SplitEscaped(x);ok{t.Fatal(x)}}}
""", "naive-delimiter-split"),
"keep-last": s(
"""package solution
func KeepLast(v []string)[]string{seen:=map[string]bool{};r:=[]string{};for i:=len(v)-1;i>=0;i--{if !seen[v[i]]{seen[v[i]]=true;r=append(r,v[i])}};out:=make([]string,len(r));for i:=range r{out[len(r)-1-i]=r[i]};return out}
""",
"""package solution
func KeepLast(v []string)[]string{seen:=map[string]bool{};out:=[]string{};for _,x:=range v{if !seen[x]{seen[x]=true;out=append(out,x)}};return out}
""",
"""package solution
import "testing"
func TestKeep(t *testing.T){in:=[]string{"a","b","a","c","b"};g:=KeepLast(in);w:=[]string{"a","c","b"};if len(g)!=3{t.Fatal(g)};for i:=range w{if g[i]!=w[i]{t.Fatal(g)}};if KeepLast(nil)==nil{t.Fatal("nil")};if in[0]!="a"{t.Fatal("mutated")}}
""", "keeps-first-occurrence"),
"clamp-window": s(
"""package solution
func ClampWindow(start,size,length int)(int,int,bool){if size<0||length<0{return 0,0,false};if start<0{start=0};if start>length{start=length};end:=length;if size<=length-start{end=start+size};return start,end,true}
""",
"""package solution
func ClampWindow(start,size,length int)(int,int,bool){if size<0||length<0{return 0,0,false};end:=start+size;if end>length{end=length};return start,end,true}
""",
"""package solution
import "testing"
func TestClamp(t *testing.T){a,b,ok:=ClampWindow(-2,3,10);if !ok||a!=0||b!=3{t.Fatal(a,b)};a,b,ok=ClampWindow(20,2,10);if !ok||a!=10||b!=10{t.Fatal(a,b)};m:=int(^uint(0)>>1);a,b,ok=ClampWindow(m-1,10,m);if !ok||a!=m-1||b!=m{t.Fatal(a,b)};if _,_,ok=ClampWindow(0,-1,1);ok{t.Fatal("negative")}}
""", "unclamped-overflowing-start"),
},
"java": {
"collapse-runs": s(
"""import java.util.*;
public final class Solution { public static List<Integer> collapseRuns(List<Integer> v){var out=new ArrayList<Integer>();for(int x:v)if(out.isEmpty()||out.get(out.size()-1)!=x)out.add(x);return out;} }
""",
"""import java.util.*;
public final class Solution { public static List<Integer> collapseRuns(List<Integer> v){return v.isEmpty()?null:v.subList(0,1);} }
""",
"""import java.util.*;
public final class SolutionTest{public static void main(String[]z){var in=new ArrayList<>(List.of(2,2,1,1,3,2,2));assert Solution.collapseRuns(in).equals(List.of(2,1,3,2));assert Solution.collapseRuns(List.of()).equals(List.of());assert in.equals(List.of(2,2,1,1,3,2,2));}}
""", "null-empty-and-truncation"),
"bounded-prefix-sum": s(
"""public final class Solution { public static Long boundedPrefixSum(long[]v,long b){if(b<0)return null;long x=0;for(long n:v){try{x=Math.addExact(x,n);}catch(ArithmeticException e){return null;}if(x>b||x < -b)return null;}return x;} }
""",
"""public final class Solution { public static Long boundedPrefixSum(long[]v,long b){long x=0;for(long n:v)x+=n;return x<=b&&x>=-b?x:null;} }
""",
"""public final class SolutionTest{public static void main(String[]z){assert Solution.boundedPrefixSum(new long[]{3,-2},3)==1;assert Solution.boundedPrefixSum(new long[]{5,-5},4)==null;assert Solution.boundedPrefixSum(new long[]{Long.MAX_VALUE,1},Long.MAX_VALUE)==null;assert Solution.boundedPrefixSum(new long[]{},-1)==null;}}
""", "final-only-wrapping-sum"),
"split-escaped": s(
"""import java.util.*;
public final class Solution { public static List<String> splitEscaped(String x){var out=new ArrayList<String>();var cur=new StringBuilder();boolean e=false;for(char c:x.toCharArray()){if(e){if(c!=','&&c!='\\')return null;cur.append(c);e=false;}else if(c=='\\')e=true;else if(c==','){out.add(cur.toString());cur.setLength(0);}else cur.append(c);}if(e)return null;out.add(cur.toString());return out;} }
""",
"""import java.util.*;
public final class Solution { public static List<String> splitEscaped(String x){return Arrays.asList(x.split(","));} }
""",
"""import java.util.*;
public final class SolutionTest{public static void main(String[]z){assert Solution.splitEscaped("a\\,b,,c\\\\d").equals(List.of("a,b","","c\\d"));assert Solution.splitEscaped("a\\q")==null;assert Solution.splitEscaped("a\\")==null;}}
""", "naive-delimiter-split"),
"keep-last": s(
"""import java.util.*;
public final class Solution { public static List<String> keepLast(List<String>v){var seen=new HashSet<String>();var r=new ArrayList<String>();for(int i=v.size()-1;i>=0;i--)if(seen.add(v.get(i)))r.add(v.get(i));Collections.reverse(r);return r;} }
""",
"""import java.util.*;
public final class Solution { public static List<String> keepLast(List<String>v){return new ArrayList<>(new LinkedHashSet<>(v));} }
""",
"""import java.util.*;
public final class SolutionTest{public static void main(String[]z){var in=new ArrayList<>(List.of("a","b","a","c","b"));assert Solution.keepLast(in).equals(List.of("a","c","b"));assert Solution.keepLast(List.of()).equals(List.of());assert in.equals(List.of("a","b","a","c","b"));}}
""", "keeps-first-occurrence"),
"clamp-window": s(
"""public final class Solution { public static int[] clampWindow(int s,int n,int len){if(n<0||len<0)return null;s=Math.max(0,Math.min(s,len));int end=n<=len-s?s+n:len;return new int[]{s,end};} }
""",
"""public final class Solution { public static int[] clampWindow(int s,int n,int len){if(n<0||len<0)return null;return new int[]{s,Math.min(s+n,len)};} }
""",
"""import java.util.*;
public final class SolutionTest{public static void main(String[]z){assert Arrays.equals(Solution.clampWindow(-2,3,10),new int[]{0,3});assert Arrays.equals(Solution.clampWindow(20,2,10),new int[]{10,10});assert Arrays.equals(Solution.clampWindow(Integer.MAX_VALUE-1,10,Integer.MAX_VALUE),new int[]{Integer.MAX_VALUE-1,Integer.MAX_VALUE});assert Solution.clampWindow(0,-1,1)==null;}}
""", "unclamped-overflowing-start"),
},
"javascript": {
"collapse-runs": s(
"""exports.collapseRuns=function(v){const out=[];for(const x of v)if(!out.length||!Object.is(out.at(-1),x))out.push(x);return out}
""",
"""exports.collapseRuns=function(v){return v.length?v.slice(0,1):null}
""",
"""const {collapseRuns}=require('./solution');const x=[2,2,1,1,3,2,2];if(JSON.stringify(collapseRuns(x))!=='[2,1,3,2]')throw Error('runs');if(JSON.stringify(collapseRuns([]))!=='[]'||x.length!==7)throw Error('contract');
""", "null-empty-and-truncation"),
"bounded-prefix-sum": s(
"""exports.boundedPrefixSum=function(v,b){if(typeof b!=='bigint'||b<0n)return null;let x=0n;for(const n of v){if(typeof n!=='bigint')return null;x+=n;if(x>b||x < -b)return null}return x}
""",
"""exports.boundedPrefixSum=function(v,b){const x=v.reduce((a,n)=>a+n,0n);return x<=b&&x>=-b?x:null}
""",
"""const {boundedPrefixSum}=require('./solution');if(boundedPrefixSum([3n,-2n],3n)!==1n)throw Error('sum');if(boundedPrefixSum([5n,-5n],4n)!==null)throw Error('prefix');if(boundedPrefixSum([], -1n)!==null)throw Error('bound');
""", "final-only-sum"),
"split-escaped": s(
"""exports.splitEscaped=function(x){const out=[],cur=[];let e=false;for(const c of x){if(e){if(c!==','&&c!=='\\')return null;cur.push(c);e=false}else if(c==='\\')e=true;else if(c===','){out.push(cur.join(''));cur.length=0}else cur.push(c)}if(e)return null;out.push(cur.join(''));return out}
""",
"""exports.splitEscaped=x=>x.split(',')
""",
"""const {splitEscaped}=require('./solution');if(JSON.stringify(splitEscaped('a\\,b,,c\\\\d'))!==JSON.stringify(['a,b','','c\\d']))throw Error('split');if(splitEscaped('a\\q')!==null||splitEscaped('a\\')!==null)throw Error('invalid');
""", "naive-delimiter-split"),
"keep-last": s(
"""exports.keepLast=function(v){const seen=new Set(),r=[];for(let i=v.length-1;i>=0;i--)if(!seen.has(v[i])){seen.add(v[i]);r.push(v[i])}return r.reverse()}
""",
"""exports.keepLast=v=>[...new Set(v)]
""",
"""const {keepLast}=require('./solution');const x=['a','b','a','c','b'];if(JSON.stringify(keepLast(x))!==JSON.stringify(['a','c','b']))throw Error('last');if(JSON.stringify(keepLast([]))!=='[]'||x.length!==5)throw Error('contract');
""", "keeps-first-occurrence"),
"clamp-window": s(
"""exports.clampWindow=function(s,n,len){if(!Number.isSafeInteger(s)||!Number.isSafeInteger(n)||!Number.isSafeInteger(len)||n<0||len<0)return null;s=Math.max(0,Math.min(s,len));return [s,n<=len-s?s+n:len]}
""",
"""exports.clampWindow=function(s,n,len){if(n<0||len<0)return null;return[s,Math.min(s+n,len)]}
""",
"""const {clampWindow}=require('./solution');const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);if(!eq(clampWindow(-2,3,10),[0,3])||!eq(clampWindow(20,2,10),[10,10])||!eq(clampWindow(Number.MAX_SAFE_INTEGER-1,10,Number.MAX_SAFE_INTEGER),[Number.MAX_SAFE_INTEGER-1,Number.MAX_SAFE_INTEGER])||clampWindow(0,-1,1)!==null)throw Error('clamp');
""", "unclamped-unsafe-start"),
},
"typescript": {},
"python": {
"collapse-runs": s(
"""def collapse_runs(values: list[int]) -> list[int]:
    out=[]
    for value in values:
        if not out or out[-1] != value: out.append(value)
    return out
""",
"""def collapse_runs(values: list[int]) -> list[int]:
    return values[:1] if values else None
""",
"""from solution import collapse_runs
+x=[2,2,1,1,3,2,2]
+assert collapse_runs(x)==[2,1,3,2]
+assert collapse_runs([])==[]
+assert x==[2,2,1,1,3,2,2]
""".replace("+",""), "null-empty-and-truncation"),
"bounded-prefix-sum": s(
"""def bounded_prefix_sum(values: list[int], bound: int) -> int | None:
    if type(bound) is not int or bound < 0: return None
    total=0
    for value in values:
        if type(value) is not int: return None
        total += value
        if abs(total) > bound: return None
    return total
""",
"""def bounded_prefix_sum(values: list[int], bound: int) -> int | None:
    total=sum(values)
    return total if abs(total)<=bound else None
""",
"""from solution import bounded_prefix_sum
+assert bounded_prefix_sum([3,-2],3)==1
+assert bounded_prefix_sum([5,-5],4) is None
+assert bounded_prefix_sum([], -1) is None
+assert bounded_prefix_sum([True],1) is None
""".replace("+",""), "final-only-sum"),
"split-escaped": s(
"""def split_escaped(x: str) -> list[str] | None:
    out=[];cur=[];escaped=False
    for char in x:
        if escaped:
            if char not in ",\\": return None
            cur.append(char);escaped=False
        elif char=="\\": escaped=True
        elif char==",": out.append("".join(cur));cur=[]
        else: cur.append(char)
    if escaped: return None
    out.append("".join(cur));return out
""",
"""def split_escaped(x: str) -> list[str] | None:
    return x.split(",")
""",
"""from solution import split_escaped
+assert split_escaped("a\\,b,,c\\\\d")==["a,b","","c\\d"]
+assert split_escaped("a\\q") is None
+assert split_escaped("a\\") is None
""".replace("+",""), "naive-delimiter-split"),
"keep-last": s(
"""def keep_last(values: list[str]) -> list[str]:
    seen=set();result=[]
    for value in reversed(values):
        if value not in seen: seen.add(value);result.append(value)
    result.reverse();return result
""",
"""def keep_last(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))
""",
"""from solution import keep_last
+x=["a","b","a","c","b"]
+assert keep_last(x)==["a","c","b"]
+assert keep_last([])==[]
+assert x==["a","b","a","c","b"]
""".replace("+",""), "keeps-first-occurrence"),
"clamp-window": s(
"""def clamp_window(start: int, size: int, length: int) -> tuple[int,int] | None:
    if size < 0 or length < 0: return None
    start=max(0,min(start,length))
    return start,start+min(size,length-start)
""",
"""def clamp_window(start: int, size: int, length: int) -> tuple[int,int] | None:
    if size<0 or length<0:return None
    return start,min(start+size,length)
""",
"""from solution import clamp_window
+assert clamp_window(-2,3,10)==(0,3)
+assert clamp_window(20,2,10)==(10,10)
+assert clamp_window(0,-1,1) is None
""".replace("+",""), "unclamped-start"),
},
"rust": {
"collapse-runs": s(
"""pub fn collapse_runs(v:&[i32])->Vec<i32>{let mut out=Vec::new();for &x in v{if out.last()!=Some(&x){out.push(x)}}out}
""",
"""pub fn collapse_runs(v:&[i32])->Vec<i32>{v.first().copied().into_iter().collect()}
""",
"""#[path="solution.rs"]mod solution;
+#[test]fn test(){let x=[2,2,1,1,3,2,2];assert_eq!(solution::collapse_runs(&x),vec![2,1,3,2]);assert!(solution::collapse_runs(&[]).is_empty());assert_eq!(x,[2,2,1,1,3,2,2]);}
""".replace("+",""), "truncates-runs"),
"bounded-prefix-sum": s(
"""pub fn bounded_prefix_sum(v:&[i64],b:i64)->Option<i64>{if b<0{return None}let mut x=0i64;for &n in v{x=x.checked_add(n)?;if x>b||x < -b{return None}}Some(x)}
""",
"""pub fn bounded_prefix_sum(v:&[i64],b:i64)->Option<i64>{let x=v.iter().fold(0i64,|a,n|a.wrapping_add(*n));if x<=b&&x>=-b{Some(x)}else{None}}
""",
"""#[path="solution.rs"]mod solution;
+#[test]fn test(){assert_eq!(solution::bounded_prefix_sum(&[3,-2],3),Some(1));assert_eq!(solution::bounded_prefix_sum(&[5,-5],4),None);assert_eq!(solution::bounded_prefix_sum(&[i64::MAX,1],i64::MAX),None);assert_eq!(solution::bounded_prefix_sum(&[],-1),None);}
""".replace("+",""), "final-only-wrapping-sum"),
"split-escaped": s(
"""pub fn split_escaped(x:&str)->Option<Vec<String>>{let mut out=Vec::new();let mut cur=String::new();let mut esc=false;for c in x.chars(){if esc{if c!=','&&c!='\\'{return None}cur.push(c);esc=false}else if c=='\\'{esc=true}else if c==','{out.push(cur);cur=String::new()}else{cur.push(c)}}if esc{return None}out.push(cur);Some(out)}
""",
"""pub fn split_escaped(x:&str)->Option<Vec<String>>{Some(x.split(',').map(String::from).collect())}
""",
"""#[path="solution.rs"]mod solution;
+#[test]fn test(){assert_eq!(solution::split_escaped("a\\,b,,c\\\\d"),Some(vec!["a,b".into(),"".into(),"c\\d".into()]));assert_eq!(solution::split_escaped("a\\q"),None);assert_eq!(solution::split_escaped("a\\"),None);}
""".replace("+",""), "naive-delimiter-split"),
"keep-last": s(
"""use std::collections::HashSet;pub fn keep_last(v:&[String])->Vec<String>{let mut seen=HashSet::new();let mut r=Vec::new();for x in v.iter().rev(){if seen.insert(x.clone()){r.push(x.clone())}}r.reverse();r}
""",
"""use std::collections::HashSet;pub fn keep_last(v:&[String])->Vec<String>{let mut s=HashSet::new();v.iter().filter(|x|s.insert((*x).clone())).cloned().collect()}
""",
"""#[path="solution.rs"]mod solution;
+#[test]fn test(){let x:Vec<String>=["a","b","a","c","b"].into_iter().map(String::from).collect();assert_eq!(solution::keep_last(&x),vec!["a","c","b"]);assert!(solution::keep_last(&[]).is_empty());assert_eq!(x[0],"a");}
""".replace("+",""), "keeps-first-occurrence"),
"clamp-window": s(
"""pub fn clamp_window(mut s:usize,n:usize,len:usize)->(usize,usize){s=s.min(len);let end=s.saturating_add(n).min(len);(s,end)}
""",
"""pub fn clamp_window(s:usize,n:usize,len:usize)->(usize,usize){(s,(s+n).min(len))}
""",
"""#[path="solution.rs"]mod solution;
+#[test]fn test(){assert_eq!(solution::clamp_window(20,2,10),(10,10));assert_eq!(solution::clamp_window(usize::MAX-1,10,usize::MAX),(usize::MAX-1,usize::MAX));assert_eq!(solution::clamp_window(0,3,10),(0,3));}
""".replace("+",""), "unclamped-overflowing-start"),
},
}

# TypeScript uses the JavaScript algorithms with explicit types and exports.
LANG["typescript"] = {
"collapse-runs": s(
"""export function collapseRuns(v:readonly number[]):number[]{const out:number[]=[];for(const x of v)if(!out.length||!Object.is(out[out.length-1],x))out.push(x);return out}
""",
"""export function collapseRuns(v:readonly number[]):number[]{return v.length?[v[0]]:null as unknown as number[]}
""",
"""import{collapseRuns}from'./solution';const x=[2,2,1,1,3,2,2];if(JSON.stringify(collapseRuns(x))!=='[2,1,3,2]')throw Error('runs');if(JSON.stringify(collapseRuns([]))!=='[]'||x.length!==7)throw Error('contract');
""", "null-empty-and-truncation"),
"bounded-prefix-sum": s(
"""export function boundedPrefixSum(v:readonly bigint[],b:bigint):bigint|null{if(b<0n)return null;let x=0n;for(const n of v){x+=n;if(x>b||x < -b)return null}return x}
""",
"""export function boundedPrefixSum(v:readonly bigint[],b:bigint):bigint|null{const x=v.reduce((a,n)=>a+n,0n);return x<=b&&x>=-b?x:null}
""",
"""import{boundedPrefixSum}from'./solution';if(boundedPrefixSum([3n,-2n],3n)!==1n)throw Error('sum');if(boundedPrefixSum([5n,-5n],4n)!==null)throw Error('prefix');if(boundedPrefixSum([],-1n)!==null)throw Error('bound');
""", "final-only-sum"),
"split-escaped": s(
"""export function splitEscaped(x:string):string[]|null{const out:string[]=[],cur:string[]=[];let e=false;for(const c of x){if(e){if(c!==','&&c!=='\\')return null;cur.push(c);e=false}else if(c==='\\')e=true;else if(c===','){out.push(cur.join(''));cur.length=0}else cur.push(c)}if(e)return null;out.push(cur.join(''));return out}
""",
"""export function splitEscaped(x:string):string[]|null{return x.split(',')}
""",
"""import{splitEscaped}from'./solution';if(JSON.stringify(splitEscaped('a\\,b,,c\\\\d'))!==JSON.stringify(['a,b','','c\\d']))throw Error('split');if(splitEscaped('a\\q')!==null||splitEscaped('a\\')!==null)throw Error('invalid');
""", "naive-delimiter-split"),
"keep-last": s(
"""export function keepLast(v:readonly string[]):string[]{const seen=new Set<string>(),r:string[]=[];for(let i=v.length-1;i>=0;i--)if(!seen.has(v[i])){seen.add(v[i]);r.push(v[i])}return r.reverse()}
""",
"""export function keepLast(v:readonly string[]):string[]{return[...new Set(v)]}
""",
"""import{keepLast}from'./solution';const x=['a','b','a','c','b'];if(JSON.stringify(keepLast(x))!==JSON.stringify(['a','c','b']))throw Error('last');if(JSON.stringify(keepLast([]))!=='[]'||x.length!==5)throw Error('contract');
""", "keeps-first-occurrence"),
"clamp-window": s(
"""export function clampWindow(s:number,n:number,len:number):readonly[number,number]|null{if(!Number.isSafeInteger(s)||!Number.isSafeInteger(n)||!Number.isSafeInteger(len)||n<0||len<0)return null;s=Math.max(0,Math.min(s,len));return[s,n<=len-s?s+n:len]}
""",
"""export function clampWindow(s:number,n:number,len:number):readonly[number,number]|null{if(n<0||len<0)return null;return[s,Math.min(s+n,len)]}
""",
"""import{clampWindow}from'./solution';const eq=(a:unknown,b:unknown)=>JSON.stringify(a)===JSON.stringify(b);if(!eq(clampWindow(-2,3,10),[0,3])||!eq(clampWindow(20,2,10),[10,10])||!eq(clampWindow(Number.MAX_SAFE_INTEGER-1,10,Number.MAX_SAFE_INTEGER),[Number.MAX_SAFE_INTEGER-1,Number.MAX_SAFE_INTEGER])||clampWindow(0,-1,1)!==null)throw Error('clamp');
""", "unclamped-unsafe-start"),
}

# These definitions use a visible placeholder so Python cannot consume escapes
# intended for the target-language source and tests.
def _bs(text: str) -> str:
    return text.replace("§", chr(92))

LANG["go"]["split-escaped"] = s(
    _bs("""package solution
func SplitEscaped(x string)([]string,bool){out:=[]string{};cur:=[]byte{};esc:=false;for i:=0;i<len(x);i++{c:=x[i];if esc{if c!=','&&c!='§§'{return nil,false};cur=append(cur,c);esc=false}else if c=='§§'{esc=true}else if c==','{out=append(out,string(cur));cur=nil}else{cur=append(cur,c)}};if esc{return nil,false};out=append(out,string(cur));return out,true}
"""),
    """package solution
import "strings"
func SplitEscaped(x string)([]string,bool){return strings.Split(x,","),true}
""",
    _bs("""package solution
import "testing"
func TestSplit(t *testing.T){g,ok:=SplitEscaped("a§§,b,,c§§§§d");w:=[]string{"a,b","","c§§d"};if !ok||len(g)!=3{t.Fatal(g,ok)};for i:=range w{if g[i]!=w[i]{t.Fatal(g)}};for _,x:=range []string{"a§§q","a§§"}{if _,ok:=SplitEscaped(x);ok{t.Fatal(x)}}}
"""), "naive-delimiter-split")
LANG["java"]["split-escaped"] = s(
    _bs("""import java.util.*;
public final class Solution { public static List<String> splitEscaped(String x){var out=new ArrayList<String>();var cur=new StringBuilder();boolean e=false;for(char c:x.toCharArray()){if(e){if(c!=','&&c!='§§')return null;cur.append(c);e=false;}else if(c=='§§')e=true;else if(c==','){out.add(cur.toString());cur.setLength(0);}else cur.append(c);}if(e)return null;out.add(cur.toString());return out;} }
"""),
    """import java.util.*;
public final class Solution { public static List<String> splitEscaped(String x){return Arrays.asList(x.split(",",-1));} }
""",
    _bs("""import java.util.*;
public final class SolutionTest{public static void main(String[]z){assert Solution.splitEscaped("a§§,b,,c§§§§d").equals(List.of("a,b","","c§§d"));assert Solution.splitEscaped("a§§q")==null;assert Solution.splitEscaped("a§§")==null;}}
"""), "naive-delimiter-split")
LANG["javascript"]["split-escaped"] = s(
    _bs("""exports.splitEscaped=function(x){const out=[],cur=[];let e=false;for(const c of x){if(e){if(c!==','&&c!=='§§')return null;cur.push(c);e=false}else if(c==='§§')e=true;else if(c===','){out.push(cur.join(''));cur.length=0}else cur.push(c)}if(e)return null;out.push(cur.join(''));return out}
"""),
    """exports.splitEscaped=x=>x.split(',')
""",
    _bs("""const {splitEscaped}=require('./solution');if(JSON.stringify(splitEscaped('a§§,b,,c§§§§d'))!==JSON.stringify(['a,b','','c§§d']))throw Error('split');if(splitEscaped('a§§q')!==null||splitEscaped('a§§')!==null)throw Error('invalid');
"""), "naive-delimiter-split")
LANG["typescript"]["split-escaped"] = s(
    _bs("""export function splitEscaped(x:string):string[]|null{const out:string[]=[],cur:string[]=[];let e=false;for(const c of x){if(e){if(c!==','&&c!=='§§')return null;cur.push(c);e=false}else if(c==='§§')e=true;else if(c===','){out.push(cur.join(''));cur.length=0}else cur.push(c)}if(e)return null;out.push(cur.join(''));return out}
"""),
    """export function splitEscaped(x:string):string[]|null{return x.split(',')}
""",
    _bs("""import{splitEscaped}from'./solution';if(JSON.stringify(splitEscaped('a§§,b,,c§§§§d'))!==JSON.stringify(['a,b','','c§§d']))throw Error('split');if(splitEscaped('a§§q')!==null||splitEscaped('a§§')!==null)throw Error('invalid');
"""), "naive-delimiter-split")
LANG["python"]["split-escaped"] = s(
    _bs("""def split_escaped(x: str) -> list[str] | None:
    out=[];cur=[];escaped=False
    for char in x:
        if escaped:
            if char not in ",§§": return None
            cur.append(char);escaped=False
        elif char=="§§": escaped=True
        elif char==",": out.append("".join(cur));cur=[]
        else: cur.append(char)
    if escaped: return None
    out.append("".join(cur));return out
"""),
    """def split_escaped(x: str) -> list[str] | None:
    return x.split(",")
""",
    _bs("""from solution import split_escaped
assert split_escaped("a§§,b,,c§§§§d")==["a,b","","c§§d"]
assert split_escaped("a§§q") is None
assert split_escaped("a§§") is None
"""), "naive-delimiter-split")
LANG["rust"]["split-escaped"] = s(
    _bs("""pub fn split_escaped(x:&str)->Option<Vec<String>>{let mut out=Vec::new();let mut cur=String::new();let mut esc=false;for c in x.chars(){if esc{if c!=','&&c!='§§'{return None}cur.push(c);esc=false}else if c=='§§'{esc=true}else if c==','{out.push(cur);cur=String::new()}else{cur.push(c)}}if esc{return None}out.push(cur);Some(out)}
"""),
    """pub fn split_escaped(x:&str)->Option<Vec<String>>{Some(x.split(',').map(String::from).collect())}
""",
    _bs("""#[path="solution.rs"]mod solution;
#[test]fn test(){assert_eq!(solution::split_escaped("a§§,b,,c§§§§d"),Some(vec!["a,b".into(),"".into(),"c§§d".into()]));assert_eq!(solution::split_escaped("a§§q"),None);assert_eq!(solution::split_escaped("a§§"),None);}
"""), "naive-delimiter-split")

FILE_CONTRACT = {
    "go": "Return solution.go using package solution.",
    "java": "Return Solution.java containing public final class Solution.",
    "javascript": "Return solution.js and expose the function as a CommonJS export.",
    "typescript": "Return solution.ts and use a named export.",
    "python": "Return solution.py with the function at module scope.",
    "rust": "Return solution.rs with a public function.",
}
API = {
    "go": {
        "collapse-runs": "func CollapseRuns(values []int) []int",
        "bounded-prefix-sum": "func BoundedPrefixSum(values []int64, bound int64) (int64, bool); use (0,false) for failure",
        "split-escaped": "func SplitEscaped(x string) ([]string, bool); use (nil,false) for failure",
        "keep-last": "func KeepLast(values []string) []string",
        "clamp-window": "func ClampWindow(start, size, length int) (int, int, bool); use (0,0,false) for failure",
    },
    "java": {
        "collapse-runs": "public static List<Integer> collapseRuns(List<Integer> values)",
        "bounded-prefix-sum": "public static Long boundedPrefixSum(long[] values, long bound); return null on failure",
        "split-escaped": "public static List<String> splitEscaped(String x); return null on failure",
        "keep-last": "public static List<String> keepLast(List<String> values)",
        "clamp-window": "public static int[] clampWindow(int start, int size, int length); return null on failure",
    },
    "javascript": {
        "collapse-runs": "exports.collapseRuns = function(values), where values contains numbers and the result is an array",
        "bounded-prefix-sum": "exports.boundedPrefixSum = function(values, bound), using bigint inputs and returning bigint or null on failure",
        "split-escaped": "exports.splitEscaped = function(x), returning an array of strings or null on failure",
        "keep-last": "exports.keepLast = function(values), accepting and returning string arrays",
        "clamp-window": "exports.clampWindow = function(start, size, length), using safe integers and returning [start,end] or null on failure",
    },
    "typescript": {
        "collapse-runs": "export function collapseRuns(values: readonly number[]): number[]",
        "bounded-prefix-sum": "export function boundedPrefixSum(values: readonly bigint[], bound: bigint): bigint | null",
        "split-escaped": "export function splitEscaped(x: string): string[] | null",
        "keep-last": "export function keepLast(values: readonly string[]): string[]",
        "clamp-window": "export function clampWindow(start: number, size: number, length: number): readonly [number,number] | null; all numbers must be safe integers",
    },
    "python": {
        "collapse-runs": "def collapse_runs(values: list[int]) -> list[int]",
        "bounded-prefix-sum": "def bounded_prefix_sum(values: list[int], bound: int) -> int | None; booleans are not valid integers here",
        "split-escaped": "def split_escaped(x: str) -> list[str] | None",
        "keep-last": "def keep_last(values: list[str]) -> list[str]",
        "clamp-window": "def clamp_window(start: int, size: int, length: int) -> tuple[int,int] | None",
    },
    "rust": {
        "collapse-runs": "pub fn collapse_runs(values: &[i32]) -> Vec<i32>",
        "bounded-prefix-sum": "pub fn bounded_prefix_sum(values: &[i64], bound: i64) -> Option<i64>",
        "split-escaped": "pub fn split_escaped(x: &str) -> Option<Vec<String>>",
        "keep-last": "pub fn keep_last(values: &[String]) -> Vec<String>",
        "clamp-window": "pub fn clamp_window(start: usize, size: usize, length: usize) -> (usize,usize); usize inputs make negative values unrepresentable",
    },
}
EXAMPLE = {
    "collapse-runs": "[2,2,1,1,2] becomes [2,1,2].",
    "bounded-prefix-sum": "With bound 3, [3,-2] succeeds with 1, while [4,-4] fails because its first prefix exceeds the bound.",
    "split-escaped": r'The input a\,b,,c produces the three fields ["a,b", "", "c"].',
    "keep-last": '["a","b","a","c","b"] becomes ["a","c","b"].',
    "clamp-window": "With start -2, size 3, and length 10, signed APIs return the window [0,3]; with start beyond length, return the empty window at length.",
}


def make_task(language: str, slug: str, kind: str) -> dict[str, Any]:
    item = LANG[language][slug]
    symbol = {
        "go": {"collapse-runs":"CollapseRuns","bounded-prefix-sum":"BoundedPrefixSum","split-escaped":"SplitEscaped","keep-last":"KeepLast","clamp-window":"ClampWindow"},
        "java": {"collapse-runs":"collapseRuns","bounded-prefix-sum":"boundedPrefixSum","split-escaped":"splitEscaped","keep-last":"keepLast","clamp-window":"clampWindow"},
        "javascript": {"collapse-runs":"collapseRuns","bounded-prefix-sum":"boundedPrefixSum","split-escaped":"splitEscaped","keep-last":"keepLast","clamp-window":"clampWindow"},
        "typescript": {"collapse-runs":"collapseRuns","bounded-prefix-sum":"boundedPrefixSum","split-escaped":"splitEscaped","keep-last":"keepLast","clamp-window":"clampWindow"},
        "python": {"collapse-runs":"collapse_runs","bounded-prefix-sum":"bounded_prefix_sum","split-escaped":"split_escaped","keep-last":"keep_last","clamp-window":"clamp_window"},
        "rust": {"collapse-runs":"collapse_runs","bounded-prefix-sum":"bounded_prefix_sum","split-escaped":"split_escaped","keep-last":"keep_last","clamp-window":"clamp_window"},
    }[language][slug]
    behavior = BEHAVIOR[slug]
    if language == "rust" and slug == "clamp-window":
        behavior = "Clamp start to length, then return the half-open window ending at min(start + size, length) without usize overflow."
    lead = "Implement the following API." if kind == "generation" else "Repair the buggy source below without changing the required API."
    prompt = (
        f"{lead}\n\nFile contract: {FILE_CONTRACT[language]}\n"
        f"Required API: {API[language][slug]}\n"
        f"Behavior: {behavior}\n"
        f"Visible example: {EXAMPLE[slug]}\n"
    )
    if kind == "repair":
        prompt += f"\nBuggy source to repair:\n\n{item['bad']}"
    prompt += "\nReturn only the complete source file; do not include Markdown fences or prose."
    files = []
    if language == "go":
        module = "module private.invalid/ganesh/development/tranche1\n\ngo 1.22\n"
        files.append({"path":"go.mod","role":"support","content":module,"sha256":sha256_text(module)})
        test_path = "solution_test.go"
    else:
        test_path = {"java":"SolutionTest.java","javascript":"solution.test.js","typescript":"solution.test.ts","python":"test_solution.py","rust":"solution_test.rs"}[language]
    files.append({"path":test_path,"role":"test","content":item["test"],"sha256":sha256_text(item["test"])})
    task = {
        "schema_version":"1.0",
        "task_id":f"dev-t1-{language}-{slug}",
        "surface":"development",
        "language":language,
        "family":LANGUAGE_FAMILY[language],
        "task_type":kind,
        "prompt":{"text":prompt,"sha256":sha256_text(prompt)},
        "rendered_prompt":{"text":prompt,"sha256":sha256_text(prompt)},
        "candidate_path":CANDIDATE_PATH[language],
        "files":files,
        "runtime_id":RUNTIME[language],
        "limits":{"timeout_seconds":60 if language in {"go","java","rust"} else 30,"memory_mb":512,"cpus":1,"pids":64,"output_bytes":65536},
        "validation":{
            "reference":{"label":"author-reference","code":item["reference"],"sha256":sha256_text(item["reference"])},
            "known_bad":[{"label":item["bad_label"],"code":item["bad"],"sha256":sha256_text(item["bad"])}],
        },
    }
    return validate_task(task)


def seed_fingerprints() -> tuple[set[str], set[str], int]:
    exact, norm, count = set(), set(), 0
    for relative in ("data/seed/ganesh_v01/train.jsonl","data/seed/ganesh_v01/validation.jsonl"):
        for line in (ROOT/relative).read_text(encoding="utf-8").splitlines():
            text=json.loads(line)["messages"][0]["content"]
            exact.add(sha256_text(text));norm.add(sha256_text(normalized(text)));count+=1
    return exact,norm,count


def build() -> tuple[dict[str,Any],dict[str,Any]]:
    OUT.mkdir(parents=True,exist_ok=True)
    tasks=[]
    for language,kinds in KINDS.items():
        tasks.extend(make_task(language,slug,kind) for slug,kind in zip(SLUGS,kinds))
    exact,norm,seed_count=seed_fingerprints()
    exact_hits=[t["task_id"] for t in tasks if t["prompt"]["sha256"] in exact]
    norm_hits=[t["task_id"] for t in tasks if sha256_text(normalized(t["prompt"]["text"])) in norm]
    if exact_hits or norm_hits:
        raise RuntimeError("private prompt overlaps seed corpus")
    entries=[]
    for task in tasks:
        path=OUT/f"{task['task_id']}.task.json"
        write_json(path,task)
        entries.append({"task_id":task["task_id"],"language":task["language"],"task_type":task["task_type"],"path":str(path.relative_to(ROOT)),"sha256":sha256_object(task),"prompt_sha256":task["prompt"]["sha256"],"rendered_prompt_sha256":task["rendered_prompt"]["sha256"]})
    counts=Counter((t["language"],t["task_type"]) for t in tasks)
    manifest={"schema_version":"ganesh-mini-private-eval-manifest/v1","surface":"development","tranche":"tranche1","status":"authored","task_count":len(tasks),"counts_by_lane":{l:{k:counts[(l,k)] for k in ("generation","repair")} for l in RUNTIME},"runtime_config":"configs/eval/runtimes.json","tasks":entries}
    manifest["manifest_sha256"]=sha256_object(manifest)
    overlap={"schema_version":"ganesh-mini-evaluation-overlap/v1","evaluation_manifest":str(MANIFEST.relative_to(ROOT)),"evaluation_manifest_sha256":manifest["manifest_sha256"],"seed_manifest":"manifests/datasets/ganesh_v01_seed.json","seed_records_inspected":seed_count,"evaluation_prompts_inspected":len(tasks),"normalization":"NFKC + Unicode casefold + whitespace collapse","exact_prompt_overlaps":exact_hits,"normalized_prompt_overlaps":norm_hits,"status":"passed"}
    overlap["report_sha256"]=sha256_object(overlap)
    write_json(MANIFEST,manifest);write_json(OVERLAP,overlap)
    return manifest,overlap


if __name__=="__main__":
    manifest,overlap=build()
    print(json.dumps({"tasks":manifest["task_count"],"manifest_sha256":manifest["manifest_sha256"],"overlap_sha256":overlap["report_sha256"]},sort_keys=True))
