#!/usr/bin/env python3
"""Build and audit private development tranche 3 deterministically."""

from __future__ import annotations

import json
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.eval.contracts import CANDIDATE_PATH, LANGUAGE_FAMILY, sha256_object, sha256_text, validate_task, write_json

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "eval/private/development/tranche3"
MANIFEST = ROOT / "manifests/evaluation/private/development-tranche3.json"
OVERLAP = ROOT / "manifests/evaluation/private/development-tranche3-overlap.json"
COMPARISON_TRANCHES = ("tranche1", "tranche2", "tranche4")
RUNTIME = {
    "go": "go-1.22.12", "java": "java-21.0.11",
    "javascript": "javascript-node-22.23.2", "typescript": "typescript-5.5.4-node-22",
    "python": "python-3.11.15", "rust": "rust-1.85.0",
}
SLUGS = ("cap-per-key", "multiset-overlap", "first-min-per-key", "first-frequency-counts", "stable-top-k")
KINDS = {
    "go": ("generation", "generation", "generation", "repair", "repair"),
    "java": ("generation", "generation", "repair", "repair", "repair"),
    "javascript": ("generation", "generation", "generation", "repair", "repair"),
    "typescript": ("generation", "generation", "repair", "repair", "repair"),
    "python": ("generation", "generation", "generation", "repair", "repair"),
    "rust": ("generation", "generation", "repair", "repair", "repair"),
}
BEHAVIOR = {
    "cap-per-key": "Reject a negative limit. Otherwise return the original indices of at most the first limit occurrences of each exact key, preserving global input order. A zero limit or empty input succeeds with a non-null empty result.",
    "multiset-overlap": "Treat right as a multiset. Scan left in order and retain each value only while an unused equal occurrence remains in right. Preserve left order, do not mutate either input, and return a non-null empty result when there is no overlap.",
    "first-min-per-key": "Reject unequal key and score lengths. For each exact key choose the index with the smallest score, breaking ties by earliest index. Return chosen indices in order of each key's first appearance; empty inputs succeed with a non-null empty result.",
    "first-frequency-counts": "Return one total frequency for each distinct exact string, ordering the counts by the value's first appearance. Do not mutate input and return a non-null empty result for empty input.",
    "stable-top-k": "Reject a negative k. Return the indices of the min(k, length) smallest scores ordered by ascending score, breaking equal-score ties by original index. Do not mutate input; zero k succeeds with a non-null empty result.",
}
EXAMPLE = {
    "cap-per-key": 'For keys ["a","b","a","a","b"] and limit 2, return indices [0,1,2,4].',
    "multiset-overlap": "For left [3,1,3,2,3] and right [3,3,2], return [3,3,2].",
    "first-min-per-key": 'For keys ["b","a","b","a"] and scores [5,4,3,3], return [2,3].',
    "first-frequency-counts": 'For ["b","a","a","c","c","c"], return [1,2,3].',
    "stable-top-k": "For scores [4,1,1,3] and k 3, return indices [1,2,3].",
}


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def sample(reference: str, bad: str, test: str, label: str) -> dict[str, str]:
    return {"reference": reference, "bad": bad, "test": test, "bad_label": label}


LANG: dict[str, dict[str, dict[str, str]]] = {
"go": {
"cap-per-key": sample(
'''package solution
func CapPerKey(keys []string, limit int) ([]int,bool) { if limit<0{return nil,false}; out:=[]int{}; seen:=map[string]int{}; for i,k:=range keys {if seen[k]<limit {out=append(out,i)}; seen[k]++}; return out,true }
''',
'''package solution
func CapPerKey(keys []string, limit int) ([]int,bool) { if limit<0{return nil,false}; out:=[]int{}; seen:=map[string]int{}; for i,k:=range keys {seen[k]++; if seen[k]<limit {out=append(out,i)}}; return out,true }
''',
'''package solution
import "testing"
func TestCap(t *testing.T){g,ok:=CapPerKey([]string{"a","b","a","a","b"},2);w:=[]int{0,1,2,4};if !ok||len(g)!=len(w){t.Fatal(g,ok)};for i:=range w{if g[i]!=w[i]{t.Fatal(g)}};if g,ok:=CapPerKey(nil,0);!ok||g==nil||len(g)!=0{t.Fatal("empty")};if _,ok:=CapPerKey(nil,-1);ok{t.Fatal("negative")}}
''', "off-by-one-cap"),
"multiset-overlap": sample(
'''package solution
func MultisetOverlap(left,right []int) []int {c:=map[int]int{};for _,x:=range right{c[x]++};out:=[]int{};for _,x:=range left{if c[x]>0{out=append(out,x);c[x]--}};return out}
''',
'''package solution
func MultisetOverlap(left,right []int) []int {s:=map[int]bool{};for _,x:=range right{s[x]=true};out:=[]int{};for _,x:=range left{if s[x]{out=append(out,x)}};return out}
''',
'''package solution
import "testing"
func TestOverlap(t *testing.T){a:=[]int{3,1,3,2,3};b:=[]int{3,3,2};g:=MultisetOverlap(a,b);w:=[]int{3,3,2};if len(g)!=3{t.Fatal(g)};for i:=range w{if g[i]!=w[i]{t.Fatal(g)}};if MultisetOverlap(nil,nil)==nil{t.Fatal("nil")};if len(a)!=5||len(b)!=3{t.Fatal("mutated")}}
''', "set-instead-of-multiset"),
"first-min-per-key": sample(
'''package solution
func FirstMinPerKey(keys []string,scores []int)([]int,bool){if len(keys)!=len(scores){return nil,false};order:=[]string{};best:=map[string]int{};for i,k:=range keys{j,ok:=best[k];if !ok{order=append(order,k);best[k]=i}else if scores[i]<scores[j]{best[k]=i}};out:=[]int{};for _,k:=range order{out=append(out,best[k])};return out,true}
''',
'''package solution
func FirstMinPerKey(keys []string,scores []int)([]int,bool){if len(keys)!=len(scores){return nil,false};best:=map[string]int{};for i,k:=range keys{best[k]=i};out:=[]int{};for _,i:=range best{out=append(out,i)};return out,true}
''',
'''package solution
import "testing"
func TestMin(t *testing.T){g,ok:=FirstMinPerKey([]string{"b","a","b","a","c"},[]int{5,4,3,3,9});w:=[]int{2,3,4};if !ok||len(g)!=3{t.Fatal(g,ok)};for i:=range w{if g[i]!=w[i]{t.Fatal(g)}};g,ok=FirstMinPerKey([]string{"x","x"},[]int{1,1});if !ok||len(g)!=1||g[0]!=0{t.Fatal("tie")};if _,ok=FirstMinPerKey([]string{"x"},nil);ok{t.Fatal("length")}}
''', "last-index-and-map-order"),
"first-frequency-counts": sample(
'''package solution
func FirstFrequencyCounts(values []string) []int {order:=[]string{};c:=map[string]int{};for _,v:=range values{if c[v]==0{order=append(order,v)};c[v]++};out:=[]int{};for _,v:=range order{out=append(out,c[v])};return out}
''',
'''package solution
import "sort"
func FirstFrequencyCounts(values []string) []int {c:=map[string]int{};for _,v:=range values{c[v]++};keys:=[]string{};for k:=range c{keys=append(keys,k)};sort.Strings(keys);out:=[]int{};for _,k:=range keys{out=append(out,c[k])};return out}
''',
'''package solution
import "testing"
func TestCounts(t *testing.T){in:=[]string{"b","a","a","c","c","c"};g:=FirstFrequencyCounts(in);w:=[]int{1,2,3};if len(g)!=3{t.Fatal(g)};for i:=range w{if g[i]!=w[i]{t.Fatal(g)}};if FirstFrequencyCounts(nil)==nil{t.Fatal("nil")};if len(in)!=6{t.Fatal("mutated")}}
''', "sorts-keys"),
"stable-top-k": sample(
'''package solution
import "sort"
func StableTopK(scores []int,k int)([]int,bool){if k<0{return nil,false};idx:=make([]int,len(scores));for i:=range idx{idx[i]=i};sort.SliceStable(idx,func(i,j int)bool{return scores[idx[i]]<scores[idx[j]]});if k<len(idx){idx=idx[:k]};return idx,true}
''',
'''package solution
import "sort"
func StableTopK(scores []int,k int)([]int,bool){if k<0{return nil,false};sort.Ints(scores);if k>len(scores){k=len(scores)};out:=make([]int,k);copy(out,scores[:k]);return out,true}
''',
'''package solution
import "testing"
func TestTop(t *testing.T){in:=[]int{4,1,1,3};g,ok:=StableTopK(in,3);w:=[]int{1,2,3};if !ok||len(g)!=3{t.Fatal(g,ok)};for i:=range w{if g[i]!=w[i]{t.Fatal(g)}};g,ok=StableTopK(in,9);if !ok||len(g)!=4{t.Fatal("bound")};if _,ok=StableTopK(in,-1);ok{t.Fatal("negative")};if in[0]!=4{t.Fatal("mutated")}}
''', "returns-sorted-values-and-mutates"),
},
"java": {
"cap-per-key": sample(
'''import java.util.*;
public final class Solution { public static List<Integer> capPerKey(List<String> keys,int limit){if(limit<0)return null;var out=new ArrayList<Integer>();var c=new HashMap<String,Integer>();for(int i=0;i<keys.size();i++){int n=c.getOrDefault(keys.get(i),0);if(n<limit)out.add(i);c.put(keys.get(i),n+1);}return out;} }
''',
'''import java.util.*;
public final class Solution { public static List<Integer> capPerKey(List<String> keys,int limit){if(limit<0)return null;var out=new ArrayList<Integer>();var c=new HashMap<String,Integer>();for(int i=0;i<keys.size();i++){int n=c.merge(keys.get(i),1,Integer::sum);if(n<limit)out.add(i);}return out;} }
''',
'''import java.util.*; public final class SolutionTest{public static void main(String[]z){assert Solution.capPerKey(List.of("a","b","a","a","b"),2).equals(List.of(0,1,2,4));assert Solution.capPerKey(List.of(),0).equals(List.of());assert Solution.capPerKey(List.of(),-1)==null;}}
''', "off-by-one-cap"),
"multiset-overlap": sample(
'''import java.util.*;
public final class Solution { public static List<Integer> multisetOverlap(List<Integer> left,List<Integer> right){var c=new HashMap<Integer,Integer>();for(int x:right)c.merge(x,1,Integer::sum);var out=new ArrayList<Integer>();for(int x:left){int n=c.getOrDefault(x,0);if(n>0){out.add(x);c.put(x,n-1);}}return out;} }
''',
'''import java.util.*;
public final class Solution { public static List<Integer> multisetOverlap(List<Integer> left,List<Integer> right){var s=new HashSet<>(right);var out=new ArrayList<Integer>();for(int x:left)if(s.contains(x))out.add(x);return out;} }
''',
'''import java.util.*; public final class SolutionTest{public static void main(String[]z){var a=new ArrayList<>(List.of(3,1,3,2,3));var b=new ArrayList<>(List.of(3,3,2));assert Solution.multisetOverlap(a,b).equals(List.of(3,3,2));assert Solution.multisetOverlap(List.of(),List.of()).equals(List.of());assert a.size()==5&&b.size()==3;}}
''', "set-instead-of-multiset"),
"first-min-per-key": sample(
'''import java.util.*;
public final class Solution { public static List<Integer> firstMinPerKey(List<String> keys,List<Integer> scores){if(keys.size()!=scores.size())return null;var order=new ArrayList<String>();var best=new HashMap<String,Integer>();for(int i=0;i<keys.size();i++){String k=keys.get(i);if(!best.containsKey(k)){order.add(k);best.put(k,i);}else if(scores.get(i)<scores.get(best.get(k)))best.put(k,i);}var out=new ArrayList<Integer>();for(String k:order)out.add(best.get(k));return out;} }
''',
'''import java.util.*;
public final class Solution { public static List<Integer> firstMinPerKey(List<String> keys,List<Integer> scores){if(keys.size()!=scores.size())return null;var best=new HashMap<String,Integer>();for(int i=0;i<keys.size();i++)best.put(keys.get(i),i);return new ArrayList<>(best.values());} }
''',
'''import java.util.*; public final class SolutionTest{public static void main(String[]z){assert Solution.firstMinPerKey(List.of("b","a","b","a","c"),List.of(5,4,3,3,9)).equals(List.of(2,3,4));assert Solution.firstMinPerKey(List.of("x","x"),List.of(1,1)).equals(List.of(0));assert Solution.firstMinPerKey(List.of("x"),List.of())==null;}}
''', "last-index-and-map-order"),
"first-frequency-counts": sample(
'''import java.util.*;
public final class Solution { public static List<Integer> firstFrequencyCounts(List<String> values){var c=new LinkedHashMap<String,Integer>();for(String v:values)c.merge(v,1,Integer::sum);return new ArrayList<>(c.values());} }
''',
'''import java.util.*;
public final class Solution { public static List<Integer> firstFrequencyCounts(List<String> values){var c=new TreeMap<String,Integer>();for(String v:values)c.merge(v,1,Integer::sum);return new ArrayList<>(c.values());} }
''',
'''import java.util.*; public final class SolutionTest{public static void main(String[]z){var in=new ArrayList<>(List.of("b","a","a","c","c","c"));assert Solution.firstFrequencyCounts(in).equals(List.of(1,2,3));assert Solution.firstFrequencyCounts(List.of()).equals(List.of());assert in.size()==6;}}
''', "sorts-keys"),
"stable-top-k": sample(
'''import java.util.*;
public final class Solution { public static List<Integer> stableTopK(List<Integer> scores,int k){if(k<0)return null;var idx=new ArrayList<Integer>();for(int i=0;i<scores.size();i++)idx.add(i);idx.sort(Comparator.comparingInt(scores::get).thenComparingInt(i->i));return new ArrayList<>(idx.subList(0,Math.min(k,idx.size())));} }
''',
'''import java.util.*;
public final class Solution { public static List<Integer> stableTopK(List<Integer> scores,int k){if(k<0)return null;var copy=new ArrayList<>(scores);Collections.sort(copy);return copy.subList(0,Math.min(k,copy.size()));} }
''',
'''import java.util.*; public final class SolutionTest{public static void main(String[]z){var in=new ArrayList<>(List.of(4,1,1,3));assert Solution.stableTopK(in,3).equals(List.of(1,2,3));assert Solution.stableTopK(in,9).equals(List.of(1,2,3,0));assert Solution.stableTopK(in,-1)==null;assert in.equals(List.of(4,1,1,3));}}
''', "returns-sorted-values"),
},
"javascript": {}, "typescript": {}, "python": {}, "rust": {},
}

# JS and TS share algorithms, but TS keeps explicit exported signatures.
LANG["javascript"] = {
"cap-per-key": sample("exports.capPerKey=function(keys,limit){if(!Number.isInteger(limit)||limit<0)return null;const out=[],c=new Map();keys.forEach((x,i)=>{const n=c.get(x)||0;if(n<limit)out.push(i);c.set(x,n+1)});return out}\n", "exports.capPerKey=function(keys,limit){if(limit<0)return null;const out=[],c=new Map();keys.forEach((x,i)=>{const n=(c.get(x)||0)+1;c.set(x,n);if(n<limit)out.push(i)});return out}\n", "const {capPerKey}=require('./solution');const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);if(!eq(capPerKey(['a','b','a','a','b'],2),[0,1,2,4])||!eq(capPerKey([],0),[])||capPerKey([],-1)!==null)throw Error('cap');\n", "off-by-one-cap"),
"multiset-overlap": sample("exports.multisetOverlap=function(left,right){const c=new Map();for(const x of right)c.set(x,(c.get(x)||0)+1);const out=[];for(const x of left){const n=c.get(x)||0;if(n>0){out.push(x);c.set(x,n-1)}}return out}\n", "exports.multisetOverlap=function(left,right){const s=new Set(right);return left.filter(x=>s.has(x))}\n", "const {multisetOverlap}=require('./solution');const a=[3,1,3,2,3],b=[3,3,2];if(JSON.stringify(multisetOverlap(a,b))!=='[3,3,2]'||JSON.stringify(multisetOverlap([],[]))!=='[]'||a.length!==5||b.length!==3)throw Error('overlap');\n", "set-instead-of-multiset"),
"first-min-per-key": sample("exports.firstMinPerKey=function(keys,scores){if(keys.length!==scores.length)return null;const order=[],best=new Map();keys.forEach((k,i)=>{if(!best.has(k)){order.push(k);best.set(k,i)}else if(scores[i]<scores[best.get(k)])best.set(k,i)});return order.map(k=>best.get(k))}\n", "exports.firstMinPerKey=function(keys,scores){if(keys.length!==scores.length)return null;const best=new Map();keys.forEach((k,i)=>best.set(k,i));return [...best.values()]}\n", "const {firstMinPerKey}=require('./solution');const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);if(!eq(firstMinPerKey(['b','a','b','a','c'],[5,4,3,3,9]),[2,3,4])||!eq(firstMinPerKey(['x','x'],[1,1]),[0])||firstMinPerKey(['x'],[])!==null)throw Error('min');\n", "last-index-selection"),
"first-frequency-counts": sample("exports.firstFrequencyCounts=function(values){const c=new Map();for(const v of values)c.set(v,(c.get(v)||0)+1);return [...c.values()]}\n", "exports.firstFrequencyCounts=function(values){const c={};for(const v of values)c[v]=(c[v]||0)+1;return Object.keys(c).sort().map(k=>c[k])}\n", "const {firstFrequencyCounts}=require('./solution');const x=['b','a','a','c','c','c'];if(JSON.stringify(firstFrequencyCounts(x))!=='[1,2,3]'||JSON.stringify(firstFrequencyCounts([]))!=='[]'||x.length!==6)throw Error('counts');\n", "sorts-keys"),
"stable-top-k": sample("exports.stableTopK=function(scores,k){if(!Number.isInteger(k)||k<0)return null;return scores.map((_,i)=>i).sort((a,b)=>scores[a]-scores[b]||a-b).slice(0,k)}\n", "exports.stableTopK=function(scores,k){if(k<0)return null;return [...scores].sort((a,b)=>a-b).slice(0,k)}\n", "const {stableTopK}=require('./solution');const x=[4,1,1,3];if(JSON.stringify(stableTopK(x,3))!=='[1,2,3]'||JSON.stringify(stableTopK(x,9))!=='[1,2,3,0]'||stableTopK(x,-1)!==null||x[0]!==4)throw Error('top');\n", "returns-sorted-values"),
}
LANG["typescript"] = {
"cap-per-key": sample("export function capPerKey(keys: readonly string[],limit: number): number[]|null {if(!Number.isInteger(limit)||limit<0)return null;const out:number[]=[],c=new Map<string,number>();keys.forEach((x,i)=>{const n=c.get(x)??0;if(n<limit)out.push(i);c.set(x,n+1)});return out}\n", "export function capPerKey(keys: readonly string[],limit: number): number[]|null {if(limit<0)return null;const out:number[]=[],c=new Map<string,number>();keys.forEach((x,i)=>{const n=(c.get(x)??0)+1;c.set(x,n);if(n<limit)out.push(i)});return out}\n", "import {capPerKey} from './solution';const eq=(a:unknown,b:unknown)=>JSON.stringify(a)===JSON.stringify(b);if(!eq(capPerKey(['a','b','a','a','b'],2),[0,1,2,4])||!eq(capPerKey([],0),[])||capPerKey([],-1)!==null)throw Error('cap');\n", "off-by-one-cap"),
"multiset-overlap": sample("export function multisetOverlap(left: readonly number[],right: readonly number[]): number[]{const c=new Map<number,number>();for(const x of right)c.set(x,(c.get(x)??0)+1);const out:number[]=[];for(const x of left){const n=c.get(x)??0;if(n>0){out.push(x);c.set(x,n-1)}}return out}\n", "export function multisetOverlap(left: readonly number[],right: readonly number[]): number[]{const s=new Set(right);return left.filter(x=>s.has(x))}\n", "import {multisetOverlap} from './solution';const a=[3,1,3,2,3],b=[3,3,2];if(JSON.stringify(multisetOverlap(a,b))!=='[3,3,2]'||JSON.stringify(multisetOverlap([],[]))!=='[]'||a.length!==5||b.length!==3)throw Error('overlap');\n", "set-instead-of-multiset"),
"first-min-per-key": sample("export function firstMinPerKey(keys: readonly string[],scores: readonly number[]): number[]|null {if(keys.length!==scores.length)return null;const order:string[]=[],best=new Map<string,number>();keys.forEach((key,i)=>{const old=best.get(key);if(old===undefined){order.push(key);best.set(key,i)}else if(scores[i]<scores[old])best.set(key,i)});return order.map(k=>best.get(k)!)}\n", "export function firstMinPerKey(keys: readonly string[],scores: readonly number[]): number[]|null {if(keys.length!==scores.length)return null;const best=new Map<string,number>();keys.forEach((k,i)=>best.set(k,i));return [...best.values()]}\n", "import {firstMinPerKey} from './solution';const eq=(a:unknown,b:unknown)=>JSON.stringify(a)===JSON.stringify(b);if(!eq(firstMinPerKey(['b','a','b','a','c'],[5,4,3,3,9]),[2,3,4])||!eq(firstMinPerKey(['x','x'],[1,1]),[0])||firstMinPerKey(['x'],[])!==null)throw Error('min');\n", "last-index-selection"),
"first-frequency-counts": sample("export function firstFrequencyCounts(values: readonly string[]): number[]{const c=new Map<string,number>();for(const v of values)c.set(v,(c.get(v)??0)+1);return [...c.values()]}\n", "export function firstFrequencyCounts(values: readonly string[]): number[]{const c:Record<string,number>={};for(const v of values)c[v]=(c[v]??0)+1;return Object.keys(c).sort().map(k=>c[k])}\n", "import {firstFrequencyCounts} from './solution';const x=['b','a','a','c','c','c'];if(JSON.stringify(firstFrequencyCounts(x))!=='[1,2,3]'||JSON.stringify(firstFrequencyCounts([]))!=='[]'||x.length!==6)throw Error('counts');\n", "sorts-keys"),
"stable-top-k": sample("export function stableTopK(scores: readonly number[],k: number): number[]|null {if(!Number.isInteger(k)||k<0)return null;return scores.map((_,i)=>i).sort((a,b)=>scores[a]-scores[b]||a-b).slice(0,k)}\n", "export function stableTopK(scores: readonly number[],k: number): number[]|null {if(k<0)return null;return [...scores].sort((a,b)=>a-b).slice(0,k)}\n", "import {stableTopK} from './solution';const x=[4,1,1,3];if(JSON.stringify(stableTopK(x,3))!=='[1,2,3]'||JSON.stringify(stableTopK(x,9))!=='[1,2,3,0]'||stableTopK(x,-1)!==null||x[0]!==4)throw Error('top');\n", "returns-sorted-values"),
}
LANG["python"] = {
"cap-per-key": sample("def cap_per_key(keys: list[str], limit: int) -> list[int] | None:\n    if type(limit) is not int or limit < 0: return None\n    out=[]; counts={}\n    for i,key in enumerate(keys):\n        n=counts.get(key,0)\n        if n < limit: out.append(i)\n        counts[key]=n+1\n    return out\n", "def cap_per_key(keys: list[str], limit: int) -> list[int] | None:\n    if limit < 0: return None\n    out=[]; counts={}\n    for i,key in enumerate(keys):\n        counts[key]=counts.get(key,0)+1\n        if counts[key] < limit: out.append(i)\n    return out\n", "from solution import cap_per_key\nassert cap_per_key(['a','b','a','a','b'],2)==[0,1,2,4]\nassert cap_per_key([],0)==[]\nassert cap_per_key([],-1) is None\n", "off-by-one-cap"),
"multiset-overlap": sample("def multiset_overlap(left: list[int], right: list[int]) -> list[int]:\n    counts={}\n    for x in right: counts[x]=counts.get(x,0)+1\n    out=[]\n    for x in left:\n        if counts.get(x,0)>0: out.append(x);counts[x]-=1\n    return out\n", "def multiset_overlap(left: list[int], right: list[int]) -> list[int]:\n    allowed=set(right)\n    return [x for x in left if x in allowed]\n", "from solution import multiset_overlap\na=[3,1,3,2,3];b=[3,3,2]\nassert multiset_overlap(a,b)==[3,3,2]\nassert multiset_overlap([],[])==[]\nassert a==[3,1,3,2,3] and b==[3,3,2]\n", "set-instead-of-multiset"),
"first-min-per-key": sample("def first_min_per_key(keys: list[str], scores: list[int]) -> list[int] | None:\n    if len(keys)!=len(scores): return None\n    order=[];best={}\n    for i,key in enumerate(keys):\n        if key not in best: order.append(key);best[key]=i\n        elif scores[i] < scores[best[key]]: best[key]=i\n    return [best[key] for key in order]\n", "def first_min_per_key(keys: list[str], scores: list[int]) -> list[int] | None:\n    if len(keys)!=len(scores): return None\n    return list({key:i for i,key in enumerate(keys)}.values())\n", "from solution import first_min_per_key\nassert first_min_per_key(['b','a','b','a','c'],[5,4,3,3,9])==[2,3,4]\nassert first_min_per_key(['x','x'],[1,1])==[0]\nassert first_min_per_key(['x'],[]) is None\n", "last-index-selection"),
"first-frequency-counts": sample("def first_frequency_counts(values: list[str]) -> list[int]:\n    counts={}\n    for value in values: counts[value]=counts.get(value,0)+1\n    return list(counts.values())\n", "def first_frequency_counts(values: list[str]) -> list[int]:\n    counts={}\n    for value in values: counts[value]=counts.get(value,0)+1\n    return [counts[k] for k in sorted(counts)]\n", "from solution import first_frequency_counts\nx=['b','a','a','c','c','c']\nassert first_frequency_counts(x)==[1,2,3]\nassert first_frequency_counts([])==[] and len(x)==6\n", "sorts-keys"),
"stable-top-k": sample("def stable_top_k(scores: list[int], k: int) -> list[int] | None:\n    if type(k) is not int or k < 0: return None\n    return sorted(range(len(scores)),key=lambda i:(scores[i],i))[:k]\n", "def stable_top_k(scores: list[int], k: int) -> list[int] | None:\n    if k < 0: return None\n    return sorted(scores)[:k]\n", "from solution import stable_top_k\nx=[4,1,1,3]\nassert stable_top_k(x,3)==[1,2,3]\nassert stable_top_k(x,9)==[1,2,3,0]\nassert stable_top_k(x,-1) is None and x==[4,1,1,3]\n", "returns-sorted-values"),
}
LANG["rust"] = {
"cap-per-key": sample("use std::collections::HashMap;\npub fn cap_per_key(keys:&[String],limit:isize)->Option<Vec<usize>>{if limit<0{return None}let mut c=HashMap::new();let mut out=Vec::new();for(i,k)in keys.iter().enumerate(){let n=*c.get(k).unwrap_or(&0);if n<limit as usize{out.push(i)}c.insert(k,n+1);}Some(out)}\n", "use std::collections::HashMap;\npub fn cap_per_key(keys:&[String],limit:isize)->Option<Vec<usize>>{if limit<0{return None}let mut c=HashMap::new();let mut out=Vec::new();for(i,k)in keys.iter().enumerate(){let n=c.entry(k).or_insert(0);*n+=1;if *n<limit as usize{out.push(i)}}Some(out)}\n", "#[path=\"solution.rs\"]mod solution;#[test]fn test(){let k:Vec<String>=[\"a\",\"b\",\"a\",\"a\",\"b\"].map(String::from).to_vec();assert_eq!(solution::cap_per_key(&k,2),Some(vec![0,1,2,4]));assert_eq!(solution::cap_per_key(&[],0),Some(vec![]));assert_eq!(solution::cap_per_key(&[],-1),None);}\n", "off-by-one-cap"),
"multiset-overlap": sample("use std::collections::HashMap;\npub fn multiset_overlap(left:&[i32],right:&[i32])->Vec<i32>{let mut c=HashMap::new();for &x in right{*c.entry(x).or_insert(0)+=1}let mut out=Vec::new();for &x in left{let n=c.entry(x).or_insert(0);if *n>0{out.push(x);*n-=1}}out}\n", "use std::collections::HashSet;\npub fn multiset_overlap(left:&[i32],right:&[i32])->Vec<i32>{let s:HashSet<_>=right.iter().copied().collect();left.iter().copied().filter(|x|s.contains(x)).collect()}\n", "#[path=\"solution.rs\"]mod solution;#[test]fn test(){let a=[3,1,3,2,3];let b=[3,3,2];assert_eq!(solution::multiset_overlap(&a,&b),vec![3,3,2]);assert!(solution::multiset_overlap(&[],&[]).is_empty());assert_eq!(a,[3,1,3,2,3]);}\n", "set-instead-of-multiset"),
"first-min-per-key": sample("use std::collections::HashMap;\npub fn first_min_per_key(keys:&[String],scores:&[i32])->Option<Vec<usize>>{if keys.len()!=scores.len(){return None}let mut order=Vec::new();let mut best=HashMap::new();for(i,k)in keys.iter().enumerate(){match best.get(k).copied(){None=>{order.push(k.clone());best.insert(k.clone(),i);},Some(j)=>if scores[i]<scores[j]{best.insert(k.clone(),i);}}}Some(order.iter().map(|k|best[k]).collect())}\n", "use std::collections::HashMap;\npub fn first_min_per_key(keys:&[String],scores:&[i32])->Option<Vec<usize>>{if keys.len()!=scores.len(){return None}let mut best=HashMap::new();for(i,k)in keys.iter().enumerate(){best.insert(k,i);}Some(best.values().copied().collect())}\n", "#[path=\"solution.rs\"]mod solution;#[test]fn test(){let k:Vec<String>=[\"b\",\"a\",\"b\",\"a\",\"c\"].map(String::from).to_vec();assert_eq!(solution::first_min_per_key(&k,&[5,4,3,3,9]),Some(vec![2,3,4]));let x=vec![String::from(\"x\"),String::from(\"x\")];assert_eq!(solution::first_min_per_key(&x,&[1,1]),Some(vec![0]));assert_eq!(solution::first_min_per_key(&x[..1],&[]),None);}\n", "last-index-and-map-order"),
"first-frequency-counts": sample("use std::collections::HashMap;\npub fn first_frequency_counts(values:&[String])->Vec<usize>{let mut order=Vec::new();let mut c=HashMap::new();for v in values{if !c.contains_key(v){order.push(v.clone());}*c.entry(v.clone()).or_insert(0)+=1;}order.iter().map(|v|c[v]).collect()}\n", "use std::collections::BTreeMap;\npub fn first_frequency_counts(values:&[String])->Vec<usize>{let mut c=BTreeMap::new();for v in values{*c.entry(v.clone()).or_insert(0)+=1;}c.values().copied().collect()}\n", "#[path=\"solution.rs\"]mod solution;#[test]fn test(){let x:Vec<String>=[\"b\",\"a\",\"a\",\"c\",\"c\",\"c\"].map(String::from).to_vec();assert_eq!(solution::first_frequency_counts(&x),vec![1,2,3]);assert!(solution::first_frequency_counts(&[]).is_empty());assert_eq!(x.len(),6);}\n", "sorts-keys"),
"stable-top-k": sample("pub fn stable_top_k(scores:&[i32],k:isize)->Option<Vec<usize>>{if k<0{return None}let mut idx:Vec<usize>=(0..scores.len()).collect();idx.sort_by_key(|&i|(scores[i],i));idx.truncate(k as usize);Some(idx)}\n", "pub fn stable_top_k(scores:&[i32],k:isize)->Option<Vec<usize>>{if k<0{return None}let mut x=scores.to_vec();x.sort();x.truncate(k as usize);Some(x.into_iter().map(|n|n as usize).collect())}\n", "#[path=\"solution.rs\"]mod solution;#[test]fn test(){let x=[4,1,1,3];assert_eq!(solution::stable_top_k(&x,3),Some(vec![1,2,3]));assert_eq!(solution::stable_top_k(&x,9),Some(vec![1,2,3,0]));assert_eq!(solution::stable_top_k(&x,-1),None);assert_eq!(x,[4,1,1,3]);}\n", "returns-sorted-values"),
}

API = {
"go": {"cap-per-key":"func CapPerKey(keys []string, limit int) ([]int, bool)","multiset-overlap":"func MultisetOverlap(left []int, right []int) []int","first-min-per-key":"func FirstMinPerKey(keys []string, scores []int) ([]int, bool)","first-frequency-counts":"func FirstFrequencyCounts(values []string) []int","stable-top-k":"func StableTopK(scores []int, k int) ([]int, bool)"},
"java": {"cap-per-key":"public static List<Integer> capPerKey(List<String> keys, int limit)","multiset-overlap":"public static List<Integer> multisetOverlap(List<Integer> left, List<Integer> right)","first-min-per-key":"public static List<Integer> firstMinPerKey(List<String> keys, List<Integer> scores)","first-frequency-counts":"public static List<Integer> firstFrequencyCounts(List<String> values)","stable-top-k":"public static List<Integer> stableTopK(List<Integer> scores, int k)"},
"javascript": {"cap-per-key":"exports.capPerKey = function(keys, limit) returning number[] | null","multiset-overlap":"exports.multisetOverlap = function(left, right) returning number[]","first-min-per-key":"exports.firstMinPerKey = function(keys, scores) returning number[] | null","first-frequency-counts":"exports.firstFrequencyCounts = function(values) returning number[]","stable-top-k":"exports.stableTopK = function(scores, k) returning number[] | null"},
"typescript": {"cap-per-key":"export function capPerKey(keys: readonly string[], limit: number): number[] | null","multiset-overlap":"export function multisetOverlap(left: readonly number[], right: readonly number[]): number[]","first-min-per-key":"export function firstMinPerKey(keys: readonly string[], scores: readonly number[]): number[] | null","first-frequency-counts":"export function firstFrequencyCounts(values: readonly string[]): number[]","stable-top-k":"export function stableTopK(scores: readonly number[], k: number): number[] | null"},
"python": {"cap-per-key":"def cap_per_key(keys: list[str], limit: int) -> list[int] | None","multiset-overlap":"def multiset_overlap(left: list[int], right: list[int]) -> list[int]","first-min-per-key":"def first_min_per_key(keys: list[str], scores: list[int]) -> list[int] | None","first-frequency-counts":"def first_frequency_counts(values: list[str]) -> list[int]","stable-top-k":"def stable_top_k(scores: list[int], k: int) -> list[int] | None"},
"rust": {"cap-per-key":"pub fn cap_per_key(keys: &[String], limit: isize) -> Option<Vec<usize>>","multiset-overlap":"pub fn multiset_overlap(left: &[i32], right: &[i32]) -> Vec<i32>","first-min-per-key":"pub fn first_min_per_key(keys: &[String], scores: &[i32]) -> Option<Vec<usize>>","first-frequency-counts":"pub fn first_frequency_counts(values: &[String]) -> Vec<usize>","stable-top-k":"pub fn stable_top_k(scores: &[i32], k: isize) -> Option<Vec<usize>>"},
}
FILE_CONTRACT = {
    "go":"Write package solution in solution.go with the function at package scope.",
    "java":"Write final class Solution in Solution.java with the static method shown; java.util types may be imported.",
    "javascript":"Write CommonJS module solution.js and export the named function.",
    "typescript":"Write strict TypeScript module solution.ts and export the named function.",
    "python":"Write solution.py with the function at module scope.",
    "rust":"Write solution.rs with the public function at module scope; use only the standard library.",
}


def make_task(language: str, slug: str, kind: str) -> dict[str, Any]:
    item = LANG[language][slug]
    lead = "Implement the following API." if kind == "generation" else "Repair the buggy source below without changing the required API."
    prompt = f"{lead}\n\nFile contract: {FILE_CONTRACT[language]}\nRequired API: {API[language][slug]}\nBehavior: {BEHAVIOR[slug]}\nVisible example: {EXAMPLE[slug]}\n"
    if kind == "repair": prompt += f"\nBuggy source to repair:\n\n{item['bad']}"
    prompt += "\nReturn only the complete source file; do not include Markdown fences or prose."
    files=[]
    if language=="go":
        module="module private.invalid/ganesh/development/tranche3\n\ngo 1.22\n"
        files.append({"path":"go.mod","role":"support","content":module,"sha256":sha256_text(module)})
    test_path={"go":"solution_test.go","java":"SolutionTest.java","javascript":"solution.test.js","typescript":"solution.test.ts","python":"test_solution.py","rust":"solution_test.rs"}[language]
    files.append({"path":test_path,"role":"test","content":item["test"],"sha256":sha256_text(item["test"])})
    task={"schema_version":"1.0","task_id":f"dev-t3-{language}-{slug}","surface":"development","language":language,"family":LANGUAGE_FAMILY[language],"task_type":kind,"prompt":{"text":prompt,"sha256":sha256_text(prompt)},"rendered_prompt":{"text":prompt,"sha256":sha256_text(prompt)},"candidate_path":CANDIDATE_PATH[language],"files":files,"runtime_id":RUNTIME[language],"limits":{"timeout_seconds":60 if language in {"go","java","rust"} else 30,"memory_mb":512,"cpus":1,"pids":64,"output_bytes":65536},"validation":{"reference":{"label":"author-reference","code":item["reference"],"sha256":sha256_text(item["reference"])},"known_bad":[{"label":item["bad_label"],"code":item["bad"],"sha256":sha256_text(item["bad"])}]}}
    return validate_task(task)


def comparison_fingerprints() -> tuple[set[str],set[str],int,int,list[str]]:
    exact:set[str]=set(); norm:set[str]=set(); seed_count=0; private_count=0; sources=[]
    for relative in ("data/seed/ganesh_v01/train.jsonl","data/seed/ganesh_v01/validation.jsonl"):
        sources.append(relative)
        for line in (ROOT/relative).read_text(encoding="utf-8").splitlines():
            text=json.loads(line)["messages"][0]["content"]; exact.add(sha256_text(text));norm.add(sha256_text(normalized(text)));seed_count+=1
    for tranche in COMPARISON_TRANCHES:
        for path in sorted((ROOT/"eval/private/development"/tranche).glob("*.task.json")):
            text=json.loads(path.read_text(encoding="utf-8"))["prompt"]["text"]
            exact.add(sha256_text(text));norm.add(sha256_text(normalized(text)));private_count+=1
    return exact,norm,seed_count,private_count,sources


def build() -> tuple[dict[str,Any],dict[str,Any]]:
    OUT.mkdir(parents=True,exist_ok=True)
    tasks=[make_task(language,slug,kind) for language,kinds in KINDS.items() for slug,kind in zip(SLUGS,kinds)]
    exact,norm,seed_count,private_count,sources=comparison_fingerprints()
    exact_hits=[t["task_id"] for t in tasks if t["prompt"]["sha256"] in exact]
    norm_hits=[t["task_id"] for t in tasks if sha256_text(normalized(t["prompt"]["text"])) in norm]
    if exact_hits or norm_hits: raise RuntimeError("tranche-3 prompt overlaps seed or another private development tranche")
    entries=[]
    for task in tasks:
        path=OUT/f"{task['task_id']}.task.json";write_json(path,task)
        entries.append({"task_id":task["task_id"],"language":task["language"],"task_type":task["task_type"],"path":str(path.relative_to(ROOT)),"sha256":sha256_object(task),"prompt_sha256":task["prompt"]["sha256"],"rendered_prompt_sha256":task["rendered_prompt"]["sha256"]})
    counts=Counter((t["language"],t["task_type"]) for t in tasks)
    manifest={"schema_version":"ganesh-mini-private-eval-manifest/v1","surface":"development","tranche":"tranche3","status":"authored","task_count":len(tasks),"counts_by_lane":{l:{k:counts[(l,k)] for k in ("generation","repair")} for l in RUNTIME},"runtime_config":"configs/eval/runtimes.json","tasks":entries}
    manifest["manifest_sha256"]=sha256_object(manifest)
    overlap={"schema_version":"ganesh-mini-evaluation-overlap/v1","evaluation_manifest":str(MANIFEST.relative_to(ROOT)),"evaluation_manifest_sha256":manifest["manifest_sha256"],"seed_sources":sources,"seed_records_inspected":seed_count,"other_private_development_prompts_inspected":private_count,"evaluation_prompts_inspected":len(tasks),"normalization":"NFKC + Unicode casefold + whitespace collapse","exact_prompt_overlaps":exact_hits,"normalized_prompt_overlaps":norm_hits,"status":"passed"}
    overlap["report_sha256"]=sha256_object(overlap);write_json(MANIFEST,manifest);write_json(OVERLAP,overlap)
    return manifest,overlap


if __name__=="__main__":
    manifest,overlap=build();print(json.dumps({"tasks":manifest["task_count"],"manifest_sha256":manifest["manifest_sha256"],"overlap_sha256":overlap["report_sha256"]},sort_keys=True))
