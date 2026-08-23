#!/usr/bin/env python3
"""Build and audit private development tranche 4 deterministically."""

from __future__ import annotations

import json
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.eval.contracts import CANDIDATE_PATH, LANGUAGE_FAMILY, sha256_object, sha256_text, validate_task, write_json

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "eval/private/development/tranche4"
MANIFEST = ROOT / "manifests/evaluation/private/development-tranche4.json"
OVERLAP = ROOT / "manifests/evaluation/private/development-tranche4-overlap.json"
COMPARISON_TRANCHES = ("tranche1", "tranche2", "tranche3")
RUNTIME = {"go":"go-1.22.12","java":"java-21.0.11","javascript":"javascript-node-22.23.2","typescript":"typescript-5.5.4-node-22","python":"python-3.11.15","rust":"rust-1.85.0"}
KINDS = {
    "go": ("generation","generation","generation","repair","repair"),
    "java": ("generation","generation","repair","repair","repair"),
    "javascript": ("generation","generation","generation","repair","repair"),
    "typescript": ("generation","generation","repair","repair","repair"),
    "python": ("generation","generation","generation","repair","repair"),
    "rust": ("generation","generation","repair","repair","repair"),
}
SLUGS = ("session-machine","dependency-cycle","coalesce-ranges","retry-schedule","framed-checksum")


def s(reference: str, bad: str, test: str, label: str) -> dict[str, str]:
    return {"reference": reference, "bad": bad, "test": test, "bad_label": label}


LANG: dict[str, dict[str, dict[str, str]]] = {
"go": {
"session-machine": s(r'''package solution
func RunSession(events []string)(string,bool){state:="closed";for _,e:=range events{switch state+":"+e{case "closed:open":state="open";case "open:authenticate":state="ready";case "open:close","ready:close":state="closed";case "ready:ping":default:return "",false}};return state,true}
''', r'''package solution
func RunSession(events []string)(string,bool){state:="closed";for _,e:=range events{if e=="open"{state="open"}else if e=="authenticate"{state="ready"}else if e=="close"{state="closed"}};return state,true}
''', r'''package solution
import "testing"
func TestSession(t *testing.T){if s,ok:=RunSession([]string{"open","authenticate","ping","close"});!ok||s!="closed"{t.Fatal(s,ok)};if _,ok:=RunSession([]string{"authenticate"});ok{t.Fatal("illegal")};if _,ok:=RunSession([]string{"open","ping"});ok{t.Fatal("early ping")};if s,ok:=RunSession(nil);!ok||s!="closed"{t.Fatal(s,ok)}}
''', "ignores-illegal-transitions"),
"dependency-cycle": s(r'''package solution
func DependenciesValid(nodes []string,edges [][2]string)bool{m:=map[string]int{};for _,n:=range nodes{if _,ok:=m[n];ok{return false};m[n]=0};g:=map[string][]string{};for _,e:=range edges{if _,ok:=m[e[0]];!ok{return false};if _,ok:=m[e[1]];!ok{return false};g[e[0]]=append(g[e[0]],e[1]);m[e[1]]++};q:=[]string{};for n,d:=range m{if d==0{q=append(q,n)}};seen:=0;for len(q)>0{x:=q[len(q)-1];q=q[:len(q)-1];seen++;for _,y:=range g[x]{m[y]--;if m[y]==0{q=append(q,y)}}};return seen==len(nodes)}
''', r'''package solution
func DependenciesValid(nodes []string,edges [][2]string)bool{known:=map[string]bool{};for _,n:=range nodes{known[n]=true};for _,e:=range edges{if !known[e[0]]||!known[e[1]]{return false}};return true}
''', r'''package solution
import "testing"
func TestDeps(t *testing.T){if !DependenciesValid([]string{"parse","build","ship"},[][2]string{{"parse","build"},{"build","ship"}}){t.Fatal("dag")};if DependenciesValid([]string{"a","b"},[][2]string{{"a","b"},{"b","a"}}){t.Fatal("cycle")};if DependenciesValid([]string{"a","a"},nil){t.Fatal("duplicate")};if DependenciesValid([]string{"a"},[][2]string{{"a","x"}}){t.Fatal("unknown")}}
''', "does-not-detect-cycles-or-duplicates"),
"coalesce-ranges": s(r'''package solution
import "sort"
func CoalesceRanges(v [][2]int)([][2]int,bool){a:=append([][2]int(nil),v...);for _,r:=range a{if r[0]>=r[1]{return nil,false}};sort.Slice(a,func(i,j int)bool{return a[i][0]<a[j][0]||(a[i][0]==a[j][0]&&a[i][1]<a[j][1])});out:=[][2]int{};for _,r:=range a{if len(out)==0||r[0]>out[len(out)-1][1]{out=append(out,r)}else if r[1]>out[len(out)-1][1]{out[len(out)-1][1]=r[1]}};return out,true}
''', r'''package solution
import "sort"
func CoalesceRanges(v [][2]int)([][2]int,bool){sort.Slice(v,func(i,j int)bool{return v[i][0]<v[j][0]});return v,true}
''', r'''package solution
import "testing"
func TestRanges(t *testing.T){in:=[][2]int{{5,8},{1,3},{3,5},{10,12}};g,ok:=CoalesceRanges(in);if !ok||len(g)!=2||g[0]!=[2]int{1,8}||g[1]!=[2]int{10,12}{t.Fatal(g,ok)};if in[0]!=[2]int{5,8}{t.Fatal("mutated")};if _,ok:=CoalesceRanges([][2]int{{2,2}});ok{t.Fatal("empty")};g,ok=CoalesceRanges(nil);if !ok||g==nil{t.Fatal("nil")}}
''', "sorts-only-and-mutates"),
"retry-schedule": s(r'''package solution
func RetrySchedule(initial,maximum uint64,attempts int)([]uint64,bool){if attempts<0||initial>maximum{return nil,false};out:=make([]uint64,attempts);d:=initial;for i:=range out{out[i]=d;if d>maximum-d{d=maximum}else{d*=2;if d>maximum{d=maximum}}};return out,true}
''', r'''package solution
func RetrySchedule(initial,maximum uint64,attempts int)([]uint64,bool){out:=make([]uint64,attempts);d:=initial;for i:=range out{out[i]=d;d*=2};return out,true}
''', r'''package solution
import "testing"
func TestRetry(t *testing.T){g,ok:=RetrySchedule(3,10,5);w:=[]uint64{3,6,10,10,10};if !ok||len(g)!=len(w){t.Fatal(g,ok)};for i:=range w{if g[i]!=w[i]{t.Fatal(g)}};if _,ok:=RetrySchedule(5,4,1);ok{t.Fatal("bounds")};if _,ok:=RetrySchedule(1,2,-1);ok{t.Fatal("attempts")};g,ok=RetrySchedule(^uint64(0)-1,^uint64(0),2);if !ok||g[1]!=^uint64(0){t.Fatal(g)}}
''', "uncapped-overflowing-doubling"),
"framed-checksum": s(r'''package solution
func DecodeFrames(data []byte)([][]byte,bool){out:=[][]byte{};for i:=0;i<len(data);{n:=int(data[i]);i++;if len(data)-i<n+1{return nil,false};p:=append([]byte(nil),data[i:i+n]...);var sum byte;for _,b:=range p{sum+=b};i+=n;if data[i]!=sum{return nil,false};i++;out=append(out,p)};return out,true}
''', r'''package solution
func DecodeFrames(data []byte)([][]byte,bool){out:=[][]byte{};for i:=0;i<len(data);{n:=int(data[i]);i++;out=append(out,data[i:i+n]);i+=n+1};return out,true}
''', r'''package solution
import "testing"
func TestFrames(t *testing.T){g,ok:=DecodeFrames([]byte{2,1,2,3,0,0,1,255,255});if !ok||len(g)!=3||len(g[1])!=0||g[2][0]!=255{t.Fatal(g,ok)};for _,x:=range [][]byte{{2,1},{1,7,8},{0}}{if _,ok:=DecodeFrames(x);ok{t.Fatal(x)}};g,ok=DecodeFrames(nil);if !ok||g==nil{t.Fatal("empty")}}
''', "skips-checksum-and-bounds"),
},
"java": {
"session-machine": s('''public final class Solution{public static String runSession(String[]e){String s="closed";for(String x:e){String k=s+":"+x;s=switch(k){case "closed:open"->"open";case "open:authenticate"->"ready";case "open:close","ready:close"->"closed";case "ready:ping"->"ready";default->null;};if(s==null)return null;}return s;}}\n''','''public final class Solution{public static String runSession(String[]e){String s="closed";for(String x:e){if(x.equals("open"))s="open";else if(x.equals("authenticate"))s="ready";else if(x.equals("close"))s="closed";}return s;}}\n''','''public final class SolutionTest{public static void main(String[]z){assert Solution.runSession(new String[]{"open","authenticate","ping","close"}).equals("closed");assert Solution.runSession(new String[]{"authenticate"})==null;assert Solution.runSession(new String[]{"open","ping"})==null;assert Solution.runSession(new String[]{}).equals("closed");}}\n''',"ignores-illegal-transitions"),
"dependency-cycle": s('''import java.util.*;public final class Solution{public static boolean dependenciesValid(List<String>n,List<String[]>e){var d=new HashMap<String,Integer>();for(String x:n)if(d.put(x,0)!=null)return false;var g=new HashMap<String,List<String>>();for(var x:e){if(!d.containsKey(x[0])||!d.containsKey(x[1]))return false;g.computeIfAbsent(x[0],k->new ArrayList<>()).add(x[1]);d.put(x[1],d.get(x[1])+1);}var q=new ArrayDeque<String>();d.forEach((x,v)->{if(v==0)q.add(x);});int seen=0;while(!q.isEmpty()){String x=q.remove();seen++;for(String y:g.getOrDefault(x,List.of())){d.put(y,d.get(y)-1);if(d.get(y)==0)q.add(y);}}return seen==n.size();}}\n''','''import java.util.*;public final class Solution{public static boolean dependenciesValid(List<String>n,List<String[]>e){var k=new HashSet<>(n);for(var x:e)if(!k.contains(x[0])||!k.contains(x[1]))return false;return true;}}\n''','''import java.util.*;public final class SolutionTest{public static void main(String[]z){assert Solution.dependenciesValid(List.of("parse","build","ship"),List.of(new String[]{"parse","build"},new String[]{"build","ship"}));assert !Solution.dependenciesValid(List.of("a","b"),List.of(new String[]{"a","b"},new String[]{"b","a"}));assert !Solution.dependenciesValid(List.of("a","a"),List.of());assert !Solution.dependenciesValid(List.of("a"),Collections.singletonList(new String[]{"a","x"}));}}\n''',"does-not-detect-cycles-or-duplicates"),
"coalesce-ranges": s('''import java.util.*;public final class Solution{public static List<long[]> coalesceRanges(List<long[]>v){var a=new ArrayList<long[]>();for(var r:v){if(r.length!=2||r[0]>=r[1])return null;a.add(r.clone());}a.sort(Comparator.<long[]>comparingLong(r->r[0]).thenComparingLong(r->r[1]));var o=new ArrayList<long[]>();for(var r:a){if(o.isEmpty()||r[0]>o.get(o.size()-1)[1])o.add(r);else o.get(o.size()-1)[1]=Math.max(o.get(o.size()-1)[1],r[1]);}return o;}}\n''','''import java.util.*;public final class Solution{public static List<long[]> coalesceRanges(List<long[]>v){v.sort(Comparator.comparingLong(r->r[0]));return v;}}\n''','''import java.util.*;public final class SolutionTest{public static void main(String[]z){var a=new long[]{5,8};var in=new ArrayList<long[]>(List.of(a,new long[]{1,3},new long[]{3,5},new long[]{10,12}));var g=Solution.coalesceRanges(in);assert g.size()==2&&Arrays.equals(g.get(0),new long[]{1,8})&&Arrays.equals(g.get(1),new long[]{10,12});assert Arrays.equals(a,new long[]{5,8})&&in.get(0)==a;assert Solution.coalesceRanges(List.of(new long[]{2,2}))==null;assert Solution.coalesceRanges(List.of()).isEmpty();}}\n''',"sorts-only-and-mutates"),
"retry-schedule": s('''import java.util.*;public final class Solution{public static List<Long> retrySchedule(long initial,long maximum,int attempts){if(initial<0||maximum<initial||attempts<0)return null;var o=new ArrayList<Long>();long d=initial;for(int i=0;i<attempts;i++){o.add(d);d=d>maximum-d?maximum:Math.min(maximum,d*2);}return o;}}\n''','''import java.util.*;public final class Solution{public static List<Long> retrySchedule(long initial,long maximum,int attempts){var o=new ArrayList<Long>();long d=initial;for(int i=0;i<attempts;i++){o.add(d);d*=2;}return o;}}\n''','''import java.util.*;public final class SolutionTest{public static void main(String[]z){assert Solution.retrySchedule(3,10,5).equals(List.of(3L,6L,10L,10L,10L));assert Solution.retrySchedule(5,4,1)==null;assert Solution.retrySchedule(1,2,-1)==null;assert Solution.retrySchedule(Long.MAX_VALUE-1,Long.MAX_VALUE,2).equals(List.of(Long.MAX_VALUE-1,Long.MAX_VALUE));}}\n''',"uncapped-overflowing-doubling"),
"framed-checksum": s('''import java.util.*;public final class Solution{public static List<byte[]> decodeFrames(byte[]d){var o=new ArrayList<byte[]>();for(int i=0;i<d.length;){int n=d[i++]&255;if(d.length-i<n+1)return null;byte[]p=Arrays.copyOfRange(d,i,i+n);int s=0;for(byte b:p)s=(s+(b&255))&255;i+=n;if((d[i++]&255)!=s)return null;o.add(p);}return o;}}\n''','''import java.util.*;public final class Solution{public static List<byte[]> decodeFrames(byte[]d){var o=new ArrayList<byte[]>();for(int i=0;i<d.length;){int n=d[i++]&255;o.add(Arrays.copyOfRange(d,i,i+n));i+=n+1;}return o;}}\n''','''public final class SolutionTest{public static void main(String[]z){var g=Solution.decodeFrames(new byte[]{2,1,2,3,0,0,1,-1,-1});assert g.size()==3&&g.get(1).length==0&&(g.get(2)[0]&255)==255;assert Solution.decodeFrames(new byte[]{2,1})==null;assert Solution.decodeFrames(new byte[]{1,7,8})==null;assert Solution.decodeFrames(new byte[]{0})==null;assert Solution.decodeFrames(new byte[]{}).isEmpty();}}\n''',"skips-checksum-and-bounds"),
},
"javascript": {
"session-machine": s("exports.runSession=e=>{let s='closed';for(const x of e){const k=s+':'+x;if(k==='closed:open')s='open';else if(k==='open:authenticate')s='ready';else if(k==='open:close'||k==='ready:close')s='closed';else if(k!=='ready:ping')return null}return s}\n","exports.runSession=e=>{let s='closed';for(const x of e){if(x==='open')s='open';else if(x==='authenticate')s='ready';else if(x==='close')s='closed'}return s}\n","const {runSession}=require('./solution');if(runSession(['open','authenticate','ping','close'])!=='closed'||runSession(['authenticate'])!==null||runSession(['open','ping'])!==null||runSession([])!=='closed')throw Error('session');\n","ignores-illegal-transitions"),
"dependency-cycle": s("exports.dependenciesValid=(n,e)=>{const d=new Map;for(const x of n){if(d.has(x))return false;d.set(x,0)}const g=new Map;for(const [a,b]of e){if(!d.has(a)||!d.has(b))return false;(g.get(a)||g.set(a,[]).get(a)).push(b);d.set(b,d.get(b)+1)}const q=[...d].filter(x=>x[1]===0).map(x=>x[0]);let seen=0;while(q.length){const x=q.pop();seen++;for(const y of g.get(x)||[]){d.set(y,d.get(y)-1);if(d.get(y)===0)q.push(y)}}return seen===n.length}\n","exports.dependenciesValid=(n,e)=>{const k=new Set(n);return e.every(([a,b])=>k.has(a)&&k.has(b))}\n","const {dependenciesValid:f}=require('./solution');if(!f(['parse','build','ship'],[['parse','build'],['build','ship']])||f(['a','b'],[['a','b'],['b','a']])||f(['a','a'],[])||f(['a'],[['a','x']]))throw Error('deps');\n","does-not-detect-cycles-or-duplicates"),
"coalesce-ranges": s("exports.coalesceRanges=v=>{const a=v.map(r=>r.slice());if(a.some(r=>r.length!==2||!Number.isSafeInteger(r[0])||!Number.isSafeInteger(r[1])||r[0]>=r[1]))return null;a.sort((x,y)=>x[0]-y[0]||x[1]-y[1]);const o=[];for(const r of a){if(!o.length||r[0]>o.at(-1)[1])o.push(r);else o.at(-1)[1]=Math.max(o.at(-1)[1],r[1])}return o}\n","exports.coalesceRanges=v=>v.sort((a,b)=>a[0]-b[0])\n","const {coalesceRanges:f}=require('./solution');const x=[[5,8],[1,3],[3,5],[10,12]],copy=JSON.stringify(x);if(JSON.stringify(f(x))!=='[[1,8],[10,12]]'||JSON.stringify(x)!==copy||f([[2,2]])!==null||JSON.stringify(f([]))!=='[]')throw Error('ranges');\n","sorts-only-and-mutates"),
"retry-schedule": s("exports.retrySchedule=(i,m,n)=>{if(!Number.isSafeInteger(i)||!Number.isSafeInteger(m)||!Number.isSafeInteger(n)||i<0||i>m||n<0)return null;const o=[];let d=i;while(o.length<n){o.push(d);d=d>m-d?m:Math.min(m,d*2)}return o}\n","exports.retrySchedule=(i,m,n)=>{const o=[];while(o.length<n){o.push(i);i*=2}return o}\n","const {retrySchedule:f}=require('./solution');if(JSON.stringify(f(3,10,5))!=='[3,6,10,10,10]'||f(5,4,1)!==null||f(1,2,-1)!==null||JSON.stringify(f(Number.MAX_SAFE_INTEGER-1,Number.MAX_SAFE_INTEGER,2))!==`[${Number.MAX_SAFE_INTEGER-1},${Number.MAX_SAFE_INTEGER}]`)throw Error('retry');\n","uncapped-unsafe-doubling"),
"framed-checksum": s("exports.decodeFrames=d=>{if(!Array.isArray(d)||d.some(x=>!Number.isInteger(x)||x<0||x>255))return null;const o=[];for(let i=0;i<d.length;){const n=d[i++];if(d.length-i<n+1)return null;const p=d.slice(i,i+n);i+=n;if(d[i++]!==p.reduce((a,b)=>(a+b)&255,0))return null;o.push(p)}return o}\n","exports.decodeFrames=d=>{const o=[];for(let i=0;i<d.length;){const n=d[i++];o.push(d.slice(i,i+n));i+=n+1}return o}\n","const {decodeFrames:f}=require('./solution');const g=f([2,1,2,3,0,0,1,255,255]);if(JSON.stringify(g)!=='[[1,2],[],[255]]'||f([2,1])!==null||f([1,7,8])!==null||f([0])!==null||JSON.stringify(f([]))!=='[]'||f([256])!==null)throw Error('frames');\n","skips-checksum-and-bounds"),
},
"typescript": {}, "python": {}, "rust": {},
}

# TypeScript deliberately has typed APIs and tests.
LANG["typescript"] = {
"session-machine":s("export function runSession(e:string[]):string|null{let s='closed';for(const x of e){const k=s+':'+x;if(k==='closed:open')s='open';else if(k==='open:authenticate')s='ready';else if(k==='open:close'||k==='ready:close')s='closed';else if(k!=='ready:ping')return null}return s}\n","export function runSession(e:string[]):string|null{let s='closed';for(const x of e){if(x==='open')s='open';else if(x==='authenticate')s='ready';else if(x==='close')s='closed'}return s}\n","import{runSession}from'./solution';if(runSession(['open','authenticate','ping','close'])!=='closed'||runSession(['authenticate'])!==null||runSession(['open','ping'])!==null||runSession([])!=='closed')throw Error('session');\n","ignores-illegal-transitions"),
"dependency-cycle":s("export function dependenciesValid(n:string[],e:Array<[string,string]>):boolean{const d=new Map<string,number>();for(const x of n){if(d.has(x))return false;d.set(x,0)}const g=new Map<string,string[]>();for(const[a,b]of e){if(!d.has(a)||!d.has(b))return false;if(!g.has(a))g.set(a,[]);g.get(a)!.push(b);d.set(b,d.get(b)!+1)}const q=[...d].filter(x=>x[1]===0).map(x=>x[0]);let seen=0;while(q.length){const x=q.pop()!;seen++;for(const y of g.get(x)??[]){d.set(y,d.get(y)!-1);if(d.get(y)===0)q.push(y)}}return seen===n.length}\n","export function dependenciesValid(n:string[],e:Array<[string,string]>):boolean{const k=new Set(n);return e.every(([a,b])=>k.has(a)&&k.has(b))}\n","import{dependenciesValid as f}from'./solution';if(!f(['parse','build','ship'],[['parse','build'],['build','ship']])||f(['a','b'],[['a','b'],['b','a']])||f(['a','a'],[])||f(['a'],[['a','x']]))throw Error('deps');\n","does-not-detect-cycles-or-duplicates"),
"coalesce-ranges":s("export function coalesceRanges(v:Array<[number,number]>):Array<[number,number]>|null{const a=v.map(r=>[...r]as[number,number]);if(a.some(r=>!Number.isSafeInteger(r[0])||!Number.isSafeInteger(r[1])||r[0]>=r[1]))return null;a.sort((x,y)=>x[0]-y[0]||x[1]-y[1]);const o:Array<[number,number]>=[];for(const r of a){if(!o.length||r[0]>o[o.length-1][1])o.push(r);else o[o.length-1][1]=Math.max(o[o.length-1][1],r[1])}return o}\n","export function coalesceRanges(v:Array<[number,number]>):Array<[number,number]>|null{return v.sort((a,b)=>a[0]-b[0])}\n","import{coalesceRanges as f}from'./solution';const x:Array<[number,number]>=[[5,8],[1,3],[3,5],[10,12]],copy=JSON.stringify(x);if(JSON.stringify(f(x))!=='[[1,8],[10,12]]'||JSON.stringify(x)!==copy||f([[2,2]])!==null||JSON.stringify(f([]))!=='[]')throw Error('ranges');\n","sorts-only-and-mutates"),
"retry-schedule":s("export function retrySchedule(i:number,m:number,n:number):number[]|null{if(!Number.isSafeInteger(i)||!Number.isSafeInteger(m)||!Number.isSafeInteger(n)||i<0||i>m||n<0)return null;const o:number[]=[];let d=i;while(o.length<n){o.push(d);d=d>m-d?m:Math.min(m,d*2)}return o}\n","export function retrySchedule(i:number,m:number,n:number):number[]|null{const o:number[]=[];while(o.length<n){o.push(i);i*=2}return o}\n","import{retrySchedule as f}from'./solution';if(JSON.stringify(f(3,10,5))!=='[3,6,10,10,10]'||f(5,4,1)!==null||f(1,2,-1)!==null||JSON.stringify(f(Number.MAX_SAFE_INTEGER-1,Number.MAX_SAFE_INTEGER,2))!==`[${Number.MAX_SAFE_INTEGER-1},${Number.MAX_SAFE_INTEGER}]`)throw Error('retry');\n","uncapped-unsafe-doubling"),
"framed-checksum":s("export function decodeFrames(d:number[]):number[][]|null{if(d.some(x=>!Number.isInteger(x)||x<0||x>255))return null;const o:number[][]=[];for(let i=0;i<d.length;){const n=d[i++];if(d.length-i<n+1)return null;const p=d.slice(i,i+n);i+=n;if(d[i++]!==p.reduce((a,b)=>(a+b)&255,0))return null;o.push(p)}return o}\n","export function decodeFrames(d:number[]):number[][]|null{const o:number[][]=[];for(let i=0;i<d.length;){const n=d[i++];o.push(d.slice(i,i+n));i+=n+1}return o}\n","import{decodeFrames as f}from'./solution';const g=f([2,1,2,3,0,0,1,255,255]);if(JSON.stringify(g)!=='[[1,2],[],[255]]'||f([2,1])!==null||f([1,7,8])!==null||f([0])!==null||JSON.stringify(f([]))!=='[]'||f([256])!==null)throw Error('frames');\n","skips-checksum-and-bounds"),
}

LANG["python"] = {
"session-machine":s("def run_session(events: list[str]) -> str | None:\n    state='closed'\n    for event in events:\n        key=(state,event)\n        if key==('closed','open'): state='open'\n        elif key==('open','authenticate'): state='ready'\n        elif key in (('open','close'),('ready','close')): state='closed'\n        elif key!=('ready','ping'): return None\n    return state\n","def run_session(events: list[str]) -> str | None:\n    state='closed'\n    for event in events:\n        if event=='open': state='open'\n        elif event=='authenticate': state='ready'\n        elif event=='close': state='closed'\n    return state\n","from solution import run_session as f\nassert f(['open','authenticate','ping','close'])=='closed'\nassert f(['authenticate']) is None and f(['open','ping']) is None and f([])=='closed'\n","ignores-illegal-transitions"),
"dependency-cycle":s("def dependencies_valid(nodes: list[str], edges: list[tuple[str,str]]) -> bool:\n    if len(set(nodes))!=len(nodes): return False\n    degree={x:0 for x in nodes}; graph={x:[] for x in nodes}\n    for a,b in edges:\n        if a not in degree or b not in degree: return False\n        graph[a].append(b);degree[b]+=1\n    queue=[x for x in nodes if degree[x]==0];seen=0\n    while queue:\n        x=queue.pop();seen+=1\n        for y in graph[x]:\n            degree[y]-=1\n            if degree[y]==0:queue.append(y)\n    return seen==len(nodes)\n","def dependencies_valid(nodes: list[str], edges: list[tuple[str,str]]) -> bool:\n    known=set(nodes)\n    return all(a in known and b in known for a,b in edges)\n","from solution import dependencies_valid as f\nassert f(['parse','build','ship'],[('parse','build'),('build','ship')])\nassert not f(['a','b'],[('a','b'),('b','a')]) and not f(['a','a'],[]) and not f(['a'],[('a','x')])\n","does-not-detect-cycles-or-duplicates"),
"coalesce-ranges":s("def coalesce_ranges(values: list[tuple[int,int]]) -> list[tuple[int,int]] | None:\n    if any(type(a) is not int or type(b) is not int or a>=b for a,b in values): return None\n    out=[]\n    for a,b in sorted(values):\n        if not out or a>out[-1][1]:out.append((a,b))\n        else:out[-1]=(out[-1][0],max(out[-1][1],b))\n    return out\n","def coalesce_ranges(values: list[tuple[int,int]]) -> list[tuple[int,int]] | None:\n    values.sort()\n    return values\n","from solution import coalesce_ranges as f\nx=[(5,8),(1,3),(3,5),(10,12)];copy=x.copy()\nassert f(x)==[(1,8),(10,12)] and x==copy and f([(2,2)]) is None and f([])==[]\n","sorts-only-and-mutates"),
"retry-schedule":s("def retry_schedule(initial: int, maximum: int, attempts: int) -> list[int] | None:\n    if any(type(x) is not int for x in (initial,maximum,attempts)) or initial<0 or initial>maximum or attempts<0:return None\n    out=[];delay=initial\n    for _ in range(attempts):out.append(delay);delay=min(maximum,delay*2)\n    return out\n","def retry_schedule(initial: int, maximum: int, attempts: int) -> list[int] | None:\n    return [initial*2**i for i in range(attempts)]\n","from solution import retry_schedule as f\nassert f(3,10,5)==[3,6,10,10,10] and f(5,4,1) is None and f(1,2,-1) is None and f(True,2,1) is None\n","uncapped-unvalidated-doubling"),
"framed-checksum":s("def decode_frames(data: bytes) -> list[bytes] | None:\n    out=[];i=0\n    while i<len(data):\n        n=data[i];i+=1\n        if len(data)-i<n+1:return None\n        payload=data[i:i+n];i+=n\n        if data[i]!=sum(payload)%256:return None\n        i+=1;out.append(payload)\n    return out\n","def decode_frames(data: bytes) -> list[bytes] | None:\n    out=[];i=0\n    while i<len(data):\n        n=data[i];i+=1;out.append(data[i:i+n]);i+=n+1\n    return out\n","from solution import decode_frames as f\nassert f(bytes([2,1,2,3,0,0,1,255,255]))==[bytes([1,2]),b'',bytes([255])]\nassert f(bytes([2,1])) is None and f(bytes([1,7,8])) is None and f(bytes([0])) is None and f(b'')==[]\n","skips-checksum-and-bounds"),
}

LANG["rust"] = {
"session-machine":s("pub fn run_session(e:&[&str])->Option<String>{let mut s=\"closed\";for x in e{match(s,*x){(\"closed\",\"open\")=>s=\"open\",(\"open\",\"authenticate\")=>s=\"ready\",(\"open\",\"close\")|(\"ready\",\"close\")=>s=\"closed\",(\"ready\",\"ping\")=>{},_=>return None}}Some(s.into())}\n","pub fn run_session(e:&[&str])->Option<String>{let mut s=\"closed\";for x in e{if *x==\"open\"{s=\"open\"}else if *x==\"authenticate\"{s=\"ready\"}else if *x==\"close\"{s=\"closed\"}}Some(s.into())}\n","#[path=\"solution.rs\"]mod solution;#[test]fn t(){assert_eq!(solution::run_session(&[\"open\",\"authenticate\",\"ping\",\"close\"]),Some(\"closed\".into()));assert_eq!(solution::run_session(&[\"authenticate\"]),None);assert_eq!(solution::run_session(&[\"open\",\"ping\"]),None);assert_eq!(solution::run_session(&[]),Some(\"closed\".into()));}\n","ignores-illegal-transitions"),
"dependency-cycle":s("use std::collections::{HashMap,HashSet};pub fn dependencies_valid(n:&[&str],e:&[(&str,&str)])->bool{let k:HashSet<_>=n.iter().copied().collect();if k.len()!=n.len(){return false}let mut d:HashMap<&str,usize>=n.iter().map(|x|(*x,0)).collect();let mut g:HashMap<&str,Vec<&str>>=HashMap::new();for &(a,b)in e{if !k.contains(a)||!k.contains(b){return false}g.entry(a).or_default().push(b);*d.get_mut(b).unwrap()+=1}let mut q:Vec<_>=d.iter().filter(|x|*x.1==0).map(|x|*x.0).collect();let mut seen=0;while let Some(x)=q.pop(){seen+=1;for y in g.get(x).into_iter().flatten(){let z=d.get_mut(y).unwrap();*z-=1;if *z==0{q.push(y)}}}seen==n.len()}\n","use std::collections::HashSet;pub fn dependencies_valid(n:&[&str],e:&[(&str,&str)])->bool{let k:HashSet<_>=n.iter().copied().collect();e.iter().all(|(a,b)|k.contains(a)&&k.contains(b))}\n","#[path=\"solution.rs\"]mod solution;#[test]fn t(){assert!(solution::dependencies_valid(&[\"parse\",\"build\",\"ship\"],&[(\"parse\",\"build\"),(\"build\",\"ship\")]));assert!(!solution::dependencies_valid(&[\"a\",\"b\"],&[(\"a\",\"b\"),(\"b\",\"a\")]));assert!(!solution::dependencies_valid(&[\"a\",\"a\"],&[]));assert!(!solution::dependencies_valid(&[\"a\"],&[(\"a\",\"x\")]));}\n","does-not-detect-cycles-or-duplicates"),
"coalesce-ranges":s("pub fn coalesce_ranges(v:&[(i64,i64)])->Option<Vec<(i64,i64)>>{if v.iter().any(|(a,b)|a>=b){return None}let mut a=v.to_vec();a.sort();let mut o:Vec<(i64,i64)>=Vec::new();for r in a{if o.last().map_or(true,|x|r.0>x.1){o.push(r)}else{let z=o.last_mut().unwrap();z.1=z.1.max(r.1)}}Some(o)}\n","pub fn coalesce_ranges(v:&[(i64,i64)])->Option<Vec<(i64,i64)>>{let mut a=v.to_vec();a.sort();Some(a)}\n","#[path=\"solution.rs\"]mod solution;#[test]fn t(){let x=[(5,8),(1,3),(3,5),(10,12)];assert_eq!(solution::coalesce_ranges(&x),Some(vec![(1,8),(10,12)]));assert_eq!(x,[(5,8),(1,3),(3,5),(10,12)]);assert_eq!(solution::coalesce_ranges(&[(2,2)]),None);assert_eq!(solution::coalesce_ranges(&[]),Some(vec![]));}\n","sorts-only"),
"retry-schedule":s("pub fn retry_schedule(i:u64,m:u64,n:i32)->Option<Vec<u64>>{if i>m||n<0{return None}let mut o=Vec::new();let mut d=i;for _ in 0..n{o.push(d);d=d.checked_mul(2).unwrap_or(m).min(m)}Some(o)}\n","pub fn retry_schedule(i:u64,_m:u64,n:i32)->Option<Vec<u64>>{Some((0..n).map(|x|i.wrapping_mul(2u64.pow(x as u32))).collect())}\n","#[path=\"solution.rs\"]mod solution;#[test]fn t(){assert_eq!(solution::retry_schedule(3,10,5),Some(vec![3,6,10,10,10]));assert_eq!(solution::retry_schedule(5,4,1),None);assert_eq!(solution::retry_schedule(1,2,-1),None);assert_eq!(solution::retry_schedule(u64::MAX-1,u64::MAX,2),Some(vec![u64::MAX-1,u64::MAX]));}\n","uncapped-wrapping-doubling"),
"framed-checksum":s("pub fn decode_frames(d:&[u8])->Option<Vec<Vec<u8>>>{let mut o=Vec::new();let mut i=0;while i<d.len(){let n=d[i]as usize;i+=1;if d.len()-i<n+1{return None}let p=d[i..i+n].to_vec();i+=n;if d[i]!=p.iter().fold(0u8,|a,b|a.wrapping_add(*b)){return None}i+=1;o.push(p)}Some(o)}\n","pub fn decode_frames(d:&[u8])->Option<Vec<Vec<u8>>>{let mut o=Vec::new();let mut i=0;while i<d.len(){let n=d[i]as usize;i+=1;o.push(d[i..i+n].to_vec());i+=n+1}Some(o)}\n","#[path=\"solution.rs\"]mod solution;#[test]fn t(){assert_eq!(solution::decode_frames(&[2,1,2,3,0,0,1,255,255]),Some(vec![vec![1,2],vec![],vec![255]]));assert_eq!(solution::decode_frames(&[2,1]),None);assert_eq!(solution::decode_frames(&[1,7,8]),None);assert_eq!(solution::decode_frames(&[0]),None);assert_eq!(solution::decode_frames(&[]),Some(vec![]));}\n","skips-checksum-and-bounds"),
}

FILE_CONTRACT={"go":"Return solution.go in package solution.","java":"Return Solution.java defining public final class Solution.","javascript":"Return CommonJS module solution.js.","typescript":"Return strict TypeScript module solution.ts.","python":"Return solution.py with the function at module scope.","rust":"Return solution.rs with the public function at module scope."}
API={
"go":{"session-machine":"func RunSession(events []string) (string, bool)","dependency-cycle":"func DependenciesValid(nodes []string, edges [][2]string) bool", "coalesce-ranges":"func CoalesceRanges(values [][2]int) ([][2]int, bool)","retry-schedule":"func RetrySchedule(initial, maximum uint64, attempts int) ([]uint64, bool)","framed-checksum":"func DecodeFrames(data []byte) ([][]byte, bool)"},
"java":{"session-machine":"public static String runSession(String[] events)","dependency-cycle":"public static boolean dependenciesValid(List<String> nodes, List<String[]> edges)","coalesce-ranges":"public static List<long[]> coalesceRanges(List<long[]> values)","retry-schedule":"public static List<Long> retrySchedule(long initial, long maximum, int attempts)","framed-checksum":"public static List<byte[]> decodeFrames(byte[] data)"},
"javascript":{"session-machine":"exports.runSession = function(events)","dependency-cycle":"exports.dependenciesValid = function(nodes, edges)","coalesce-ranges":"exports.coalesceRanges = function(values)","retry-schedule":"exports.retrySchedule = function(initial, maximum, attempts)","framed-checksum":"exports.decodeFrames = function(data)"},
"typescript":{"session-machine":"export function runSession(events: string[]): string | null", "dependency-cycle":"export function dependenciesValid(nodes: string[], edges: Array<[string,string]>): boolean","coalesce-ranges":"export function coalesceRanges(values: Array<[number,number]>): Array<[number,number]> | null","retry-schedule":"export function retrySchedule(initial: number, maximum: number, attempts: number): number[] | null","framed-checksum":"export function decodeFrames(data: number[]): number[][] | null"},
"python":{"session-machine":"def run_session(events: list[str]) -> str | None", "dependency-cycle":"def dependencies_valid(nodes: list[str], edges: list[tuple[str,str]]) -> bool","coalesce-ranges":"def coalesce_ranges(values: list[tuple[int,int]]) -> list[tuple[int,int]] | None","retry-schedule":"def retry_schedule(initial: int, maximum: int, attempts: int) -> list[int] | None","framed-checksum":"def decode_frames(data: bytes) -> list[bytes] | None"},
"rust":{"session-machine":"pub fn run_session(events: &[&str]) -> Option<String>", "dependency-cycle":"pub fn dependencies_valid(nodes: &[&str], edges: &[(&str,&str)]) -> bool","coalesce-ranges":"pub fn coalesce_ranges(values: &[(i64,i64)]) -> Option<Vec<(i64,i64)>>","retry-schedule":"pub fn retry_schedule(initial: u64, maximum: u64, attempts: i32) -> Option<Vec<u64>>","framed-checksum":"pub fn decode_frames(data: &[u8]) -> Option<Vec<Vec<u8>>>"},
}
BEHAVIOR={
"session-machine":"Start in closed. Legal transitions are closed/open -> open, open/authenticate -> ready, ready/ping -> ready, and open or ready/close -> closed. Reject the whole sequence on any other event/state pair; otherwise return the final state.",
"dependency-cycle":"Return true exactly when node names are unique, every directed edge endpoint is declared, and the directed dependency graph is acyclic. Empty input is valid.",
"coalesce-ranges":"Treat pairs as half-open ranges. Reject a range unless start is strictly less than end. Without mutating input, sort and merge overlapping or touching ranges; empty input succeeds with a non-null empty result.",
"retry-schedule":"Reject negative attempts or an initial delay above the maximum. Return exactly attempts delays, starting at initial and doubling each time but saturating at maximum without arithmetic overflow.",
"framed-checksum":"Decode concatenated frames encoded as one unsigned length byte, that many payload bytes, and one checksum byte equal to payload-byte sum modulo 256. Reject truncation, bad checksum, trailing partial data, and invalid byte values where applicable. Empty input succeeds with a non-null empty result.",
}
EXAMPLE={
"session-machine":"[open, authenticate, ping, close] returns closed; [open, ping] is rejected.",
"dependency-cycle":"nodes [parse, build, ship] with parse->build and build->ship is valid; adding ship->parse makes it invalid.",
"coalesce-ranges":"[(5,8),(1,3),(3,5),(10,12)] becomes [(1,8),(10,12)].",
"retry-schedule":"initial 3, maximum 10, attempts 5 returns [3,6,10,10,10].",
"framed-checksum":"bytes [2,1,2,3,0,0] decode to payloads [[1,2],[]], because 1+2=3 and the empty checksum is 0.",
}

def normalized(text:str)->str:
    return " ".join(unicodedata.normalize("NFKC",text).casefold().split())

def make_task(language:str,slug:str,kind:str)->dict[str,Any]:
    item=LANG[language][slug]
    lead="Implement the following API." if kind=="generation" else "Repair the buggy source below without changing the required API."
    prompt=f"{lead}\n\nFile contract: {FILE_CONTRACT[language]}\nRequired API: {API[language][slug]}\nBehavior: {BEHAVIOR[slug]}\nVisible example: {EXAMPLE[slug]}\n"
    if kind=="repair":prompt+=f"\nBuggy source to repair:\n\n{item['bad']}"
    prompt+="\nReturn only the complete source file; do not include Markdown fences or prose."
    files=[]
    if language=="go":
        module="module private.invalid/ganesh/development/tranche4\n\ngo 1.22\n"
        files.append({"path":"go.mod","role":"support","content":module,"sha256":sha256_text(module)})
        test_path="solution_test.go"
    else:test_path={"java":"SolutionTest.java","javascript":"solution.test.js","typescript":"solution.test.ts","python":"test_solution.py","rust":"solution_test.rs"}[language]
    files.append({"path":test_path,"role":"test","content":item["test"],"sha256":sha256_text(item["test"])})
    task={"schema_version":"1.0","task_id":f"dev-t4-{language}-{slug}","surface":"development","language":language,"family":LANGUAGE_FAMILY[language],"task_type":kind,"prompt":{"text":prompt,"sha256":sha256_text(prompt)},"rendered_prompt":{"text":prompt,"sha256":sha256_text(prompt)},"candidate_path":CANDIDATE_PATH[language],"files":files,"runtime_id":RUNTIME[language],"limits":{"timeout_seconds":60 if language in {"go","java","rust"} else 30,"memory_mb":512,"cpus":1,"pids":64,"output_bytes":65536},"validation":{"reference":{"label":"author-reference","code":item["reference"],"sha256":sha256_text(item["reference"])},"known_bad":[{"label":item["bad_label"],"code":item["bad"],"sha256":sha256_text(item["bad"])}]}}
    return validate_task(task)

def comparison_fingerprints()->tuple[set[str],set[str],int,dict[str,int]]:
    exact:set[str]=set();norm:set[str]=set();counts={"seed":0,"private_development":0}
    for relative in ("data/seed/ganesh_v01/train.jsonl","data/seed/ganesh_v01/validation.jsonl"):
        for line in (ROOT/relative).read_text(encoding="utf-8").splitlines():
            text=json.loads(line)["messages"][0]["content"];exact.add(sha256_text(text));norm.add(sha256_text(normalized(text)));counts["seed"]+=1
    for tranche in COMPARISON_TRANCHES:
        for path in sorted((ROOT/"eval/private/development"/tranche).glob("*.task.json")):
            text=json.loads(path.read_text(encoding="utf-8"))["prompt"]["text"];exact.add(sha256_text(text));norm.add(sha256_text(normalized(text)));counts["private_development"]+=1
    return exact,norm,sum(counts.values()),counts

def build()->tuple[dict[str,Any],dict[str,Any]]:
    OUT.mkdir(parents=True,exist_ok=True)
    tasks=[make_task(language,slug,kind) for language,kinds in KINDS.items() for slug,kind in zip(SLUGS,kinds)]
    exact,norm,total,counts_seen=comparison_fingerprints()
    exact_hits=[t["task_id"] for t in tasks if t["prompt"]["sha256"] in exact]
    norm_hits=[t["task_id"] for t in tasks if sha256_text(normalized(t["prompt"]["text"])) in norm]
    own_exact=[t["task_id"] for t in tasks if sum(x["prompt"]["sha256"]==t["prompt"]["sha256"] for x in tasks)>1]
    own_norm=[t["task_id"] for t in tasks if sum(normalized(x["prompt"]["text"])==normalized(t["prompt"]["text"]) for x in tasks)>1]
    if exact_hits or norm_hits or own_exact or own_norm:raise RuntimeError("tranche4 prompt overlap detected")
    entries=[]
    for task in tasks:
        path=OUT/f"{task['task_id']}.task.json";write_json(path,task)
        entries.append({"task_id":task["task_id"],"language":task["language"],"task_type":task["task_type"],"path":str(path.relative_to(ROOT)),"sha256":sha256_object(task),"prompt_sha256":task["prompt"]["sha256"],"rendered_prompt_sha256":task["rendered_prompt"]["sha256"]})
    counter=Counter((t["language"],t["task_type"]) for t in tasks)
    manifest={"schema_version":"ganesh-mini-private-eval-manifest/v1","surface":"development","tranche":"tranche4","status":"authored","task_count":len(tasks),"counts_by_lane":{l:{k:counter[(l,k)] for k in("generation","repair")}for l in RUNTIME},"runtime_config":"configs/eval/runtimes.json","tasks":entries};manifest["manifest_sha256"]=sha256_object(manifest)
    overlap={"schema_version":"ganesh-mini-evaluation-overlap/v1","evaluation_manifest":str(MANIFEST.relative_to(ROOT)),"evaluation_manifest_sha256":manifest["manifest_sha256"],"seed_manifest":"manifests/datasets/ganesh_v01_seed.json","seed_records_inspected":counts_seen["seed"],"other_private_development_prompts_inspected":counts_seen["private_development"],"comparison_prompts_inspected":total,"evaluation_prompts_inspected":len(tasks),"normalization":"NFKC + Unicode casefold + whitespace collapse","exact_prompt_overlaps":exact_hits,"normalized_prompt_overlaps":norm_hits,"within_tranche_exact_overlaps":own_exact,"within_tranche_normalized_overlaps":own_norm,"status":"passed"};overlap["report_sha256"]=sha256_object(overlap)
    write_json(MANIFEST,manifest);write_json(OVERLAP,overlap);return manifest,overlap

if __name__=="__main__":
    manifest,overlap=build();print(json.dumps({"tasks":manifest["task_count"],"manifest_sha256":manifest["manifest_sha256"],"overlap_sha256":overlap["report_sha256"]},sort_keys=True))
