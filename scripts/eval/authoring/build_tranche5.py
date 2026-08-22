#!/usr/bin/env python3
"""Build and audit private development tranche 5 deterministically."""

from __future__ import annotations

import json
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.eval.contracts import CANDIDATE_PATH, LANGUAGE_FAMILY, sha256_object, sha256_text, validate_task, write_json

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "eval/private/development/tranche5"
MANIFEST = ROOT / "manifests/evaluation/private/development-tranche5.json"
OVERLAP = ROOT / "manifests/evaluation/private/development-tranche5-overlap.json"
RUNTIME = {"go":"go-1.22.12","java":"java-21.0.11","javascript":"javascript-node-22.23.2","typescript":"typescript-5.5.4-node-22","python":"python-3.11.15","rust":"rust-1.85.0"}
KINDS = {
    "go": ("generation","generation","generation","repair","repair"),
    "java": ("generation","generation","repair","repair","repair"),
    "javascript": ("generation","generation","generation","repair","repair"),
    "typescript": ("generation","generation","repair","repair","repair"),
    "python": ("generation","generation","generation","repair","repair"),
    "rust": ("generation","generation","repair","repair","repair"),
}
SLUGS = ("ring-buffer-trace","idempotency-batches","token-bucket-trace","rolling-checksums","ordered-event-compaction")


def sample(reference: str, bad: str, test: str, label: str) -> dict[str, str]:
    return {"reference": reference, "bad": bad, "test": test, "bad_label": label}


LANG: dict[str, dict[str, dict[str, str]]] = {
"go": {
"ring-buffer-trace": sample('''package solution
func RingBufferTrace(capacity int, values []int)([]int,bool){if capacity<=0{return nil,false};out:=make([]int,len(values));q:=[]int{};for i,v:=range values{if v==-1{return nil,false};out[i]=-1;if len(q)==capacity{out[i]=q[0];q=q[1:]};q=append(q,v)};return out,true}
''','''package solution
func RingBufferTrace(capacity int,values []int)([]int,bool){if capacity<=0{return nil,false};out:=make([]int,len(values));for i:=range out{out[i]=-1};return out,true}
''','''package solution
import "testing"
func TestRing(t *testing.T){g,ok:=RingBufferTrace(2,[]int{4,7,9,1});w:=[]int{-1,-1,4,7};if !ok||len(g)!=4{t.Fatal(g,ok)};for i:=range w{if g[i]!=w[i]{t.Fatal(g)}};if _,ok:=RingBufferTrace(0,nil);ok{t.Fatal("capacity")};if _,ok:=RingBufferTrace(2,[]int{-1});ok{t.Fatal("reserved")};g,ok=RingBufferTrace(3,nil);if !ok||g==nil{t.Fatal("empty")}}
''',"never-evicts"),
"idempotency-batches": sample('''package solution
func IdempotencyBatchTrace(keys []string,amounts []int)([]int,bool){if len(keys)!=len(amounts){return nil,false};seen:=map[string]bool{};out:=make([]int,len(keys));total:=0;for i,k:=range keys{if k==""{return nil,false};if !seen[k]{seen[k]=true;total+=amounts[i]};out[i]=total};return out,true}
''','''package solution
func IdempotencyBatchTrace(keys []string,amounts []int)([]int,bool){if len(keys)!=len(amounts){return nil,false};out:=make([]int,len(keys));total:=0;for i,v:=range amounts{total+=v;out[i]=total};return out,true}
''','''package solution
import "testing"
func TestIdempotency(t *testing.T){g,ok:=IdempotencyBatchTrace([]string{"a","b","a","c"},[]int{5,2,99,-1});w:=[]int{5,7,7,6};if !ok||len(g)!=4{t.Fatal(g,ok)};for i:=range w{if g[i]!=w[i]{t.Fatal(g)}};if _,ok:=IdempotencyBatchTrace([]string{"a"},nil);ok{t.Fatal("length")};if _,ok:=IdempotencyBatchTrace([]string{""},[]int{1});ok{t.Fatal("key")};g,ok=IdempotencyBatchTrace(nil,nil);if !ok||g==nil{t.Fatal("empty")}}
''',"reapplies-duplicate-keys"),
"token-bucket-trace": sample('''package solution
func TokenBucketTrace(capacity,initial,refill int,costs []int)([]int,bool){if capacity<0||initial<0||initial>capacity||refill<0{return nil,false};tokens:=initial;out:=make([]int,len(costs));for i,c:=range costs{if c<0{return nil,false};if i>0{tokens+=refill;if tokens>capacity{tokens=capacity}};if c<=tokens{tokens-=c;out[i]=tokens}else{out[i]=-tokens-1}};return out,true}
''','''package solution
func TokenBucketTrace(capacity,initial,refill int,costs []int)([]int,bool){tokens:=initial;out:=[]int{};for _,c:=range costs{tokens+=refill;if tokens>capacity{tokens=capacity};tokens-=c;out=append(out,tokens)};return out,true}
''','''package solution
import "testing"
func TestBucket(t *testing.T){g,ok:=TokenBucketTrace(5,3,2,[]int{2,5,1,4});w:=[]int{1,-4,4,1};if !ok||len(g)!=4{t.Fatal(g,ok)};for i:=range w{if g[i]!=w[i]{t.Fatal(g)}};if _,ok:=TokenBucketTrace(2,3,0,nil);ok{t.Fatal("initial")};if _,ok:=TokenBucketTrace(2,1,0,[]int{-1});ok{t.Fatal("cost")};g,ok=TokenBucketTrace(0,0,0,nil);if !ok||g==nil{t.Fatal("empty")}}
''',"refills-before-first-and-spends-on-rejection"),
"rolling-checksums": sample('''package solution
func RollingChecksums(values []int,window int)([]int,bool){if window<=0{return nil,false};out:=[]int{};for i:=0;i+window<=len(values);i++{sum:=0;for j:=0;j<window;j++{sum+=(j+1)*values[i+j]};out=append(out,sum)};return out,true}
''','''package solution
func RollingChecksums(values []int,window int)([]int,bool){if window<=0{return nil,false};out:=[]int{};for i:=0;i+window<=len(values);i++{sum:=0;for j:=i;j<i+window;j++{sum+=values[j]};out=append(out,sum)};return out,true}
''','''package solution
import "testing"
func TestRolling(t *testing.T){g,ok:=RollingChecksums([]int{2,4,1,3},3);w:=[]int{13,15};if !ok||len(g)!=2{t.Fatal(g,ok)};for i:=range w{if g[i]!=w[i]{t.Fatal(g)}};if _,ok:=RollingChecksums(nil,0);ok{t.Fatal("window")};g,ok=RollingChecksums([]int{1},2);if !ok||g==nil||len(g)!=0{t.Fatal(g,ok)}}
''',"uses-unweighted-window-sum"),
"ordered-event-compaction": sample('''package solution
func CompactOrderedEvents(seq []int,keys []string,values []int)([]int,bool){if len(seq)!=len(keys)||len(seq)!=len(values){return nil,false};last:=map[string]int{};for i:=range seq{if i>0&&seq[i]<=seq[i-1]||keys[i]==""{return nil,false};last[keys[i]]=i};out:=[]int{};for i,k:=range keys{if last[k]==i{out=append(out,values[i])}};return out,true}
''','''package solution
func CompactOrderedEvents(seq []int,keys []string,values []int)([]int,bool){if len(seq)!=len(keys)||len(seq)!=len(values){return nil,false};seen:=map[string]bool{};out:=[]int{};for i,k:=range keys{if !seen[k]{seen[k]=true;out=append(out,values[i])}};return out,true}
''','''package solution
import "testing"
func TestCompact(t *testing.T){g,ok:=CompactOrderedEvents([]int{1,2,3,8},[]string{"a","b","a","c"},[]int{4,7,9,2});w:=[]int{7,9,2};if !ok||len(g)!=3{t.Fatal(g,ok)};for i:=range w{if g[i]!=w[i]{t.Fatal(g)}};if _,ok:=CompactOrderedEvents([]int{2,2},[]string{"a","b"},[]int{1,2});ok{t.Fatal("order")};if _,ok:=CompactOrderedEvents([]int{1},nil,nil);ok{t.Fatal("length")};g,ok=CompactOrderedEvents(nil,nil,nil);if !ok||g==nil{t.Fatal("empty")}}
''',"keeps-first-occurrence"),
},
"java": {
"ring-buffer-trace": sample('''import java.util.*;public final class Solution{public static List<Integer> ringBufferTrace(int capacity,List<Integer> values){if(capacity<=0)return null;var q=new ArrayDeque<Integer>();var o=new ArrayList<Integer>();for(int v:values){if(v==-1)return null;o.add(q.size()==capacity?q.removeFirst():-1);q.addLast(v);}return o;}}
''','''import java.util.*;public final class Solution{public static List<Integer> ringBufferTrace(int capacity,List<Integer> values){if(capacity<=0)return null;return new ArrayList<>(Collections.nCopies(values.size(),-1));}}
''','''import java.util.*;public final class SolutionTest{public static void main(String[]z){assert Solution.ringBufferTrace(2,List.of(4,7,9,1)).equals(List.of(-1,-1,4,7));assert Solution.ringBufferTrace(0,List.of())==null;assert Solution.ringBufferTrace(2,List.of(-1))==null;assert Solution.ringBufferTrace(3,List.of()).isEmpty();}}
''',"never-evicts"),
"idempotency-batches": sample('''import java.util.*;public final class Solution{public static List<Integer> idempotencyBatchTrace(List<String>keys,List<Integer>amounts){if(keys.size()!=amounts.size())return null;var seen=new HashSet<String>();var out=new ArrayList<Integer>();int total=0;for(int i=0;i<keys.size();i++){if(keys.get(i).isEmpty())return null;if(seen.add(keys.get(i)))total+=amounts.get(i);out.add(total);}return out;}}
''','''import java.util.*;public final class Solution{public static List<Integer> idempotencyBatchTrace(List<String>keys,List<Integer>amounts){if(keys.size()!=amounts.size())return null;var out=new ArrayList<Integer>();int total=0;for(int x:amounts){total+=x;out.add(total);}return out;}}
''','''import java.util.*;public final class SolutionTest{public static void main(String[]z){assert Solution.idempotencyBatchTrace(List.of("a","b","a","c"),List.of(5,2,99,-1)).equals(List.of(5,7,7,6));assert Solution.idempotencyBatchTrace(List.of("a"),List.of())==null;assert Solution.idempotencyBatchTrace(List.of(""),List.of(1))==null;assert Solution.idempotencyBatchTrace(List.of(),List.of()).isEmpty();}}
''',"reapplies-duplicate-keys"),
"token-bucket-trace": sample('''import java.util.*;public final class Solution{public static List<Integer> tokenBucketTrace(int capacity,int initial,int refill,List<Integer>costs){if(capacity<0||initial<0||initial>capacity||refill<0)return null;int tokens=initial;var out=new ArrayList<Integer>();for(int i=0;i<costs.size();i++){int c=costs.get(i);if(c<0)return null;if(i>0)tokens=Math.min(capacity,tokens+refill);if(c<=tokens){tokens-=c;out.add(tokens);}else out.add(-tokens-1);}return out;}}
''','''import java.util.*;public final class Solution{public static List<Integer> tokenBucketTrace(int capacity,int initial,int refill,List<Integer>costs){int tokens=initial;var out=new ArrayList<Integer>();for(int c:costs){tokens=Math.min(capacity,tokens+refill);tokens-=c;out.add(tokens);}return out;}}
''','''import java.util.*;public final class SolutionTest{public static void main(String[]z){assert Solution.tokenBucketTrace(5,3,2,List.of(2,5,1,4)).equals(List.of(1,-4,4,1));assert Solution.tokenBucketTrace(2,3,0,List.of())==null;assert Solution.tokenBucketTrace(2,1,0,List.of(-1))==null;assert Solution.tokenBucketTrace(0,0,0,List.of()).isEmpty();}}
''',"refills-before-first-and-spends-on-rejection"),
"rolling-checksums": sample('''import java.util.*;public final class Solution{public static List<Integer> rollingChecksums(List<Integer>values,int window){if(window<=0)return null;var out=new ArrayList<Integer>();for(int i=0;i+window<=values.size();i++){int sum=0;for(int j=0;j<window;j++)sum+=(j+1)*values.get(i+j);out.add(sum);}return out;}}
''','''import java.util.*;public final class Solution{public static List<Integer> rollingChecksums(List<Integer>values,int window){if(window<=0)return null;var out=new ArrayList<Integer>();for(int i=0;i+window<=values.size();i++){int sum=0;for(int j=i;j<i+window;j++)sum+=values.get(j);out.add(sum);}return out;}}
''','''import java.util.*;public final class SolutionTest{public static void main(String[]z){assert Solution.rollingChecksums(List.of(2,4,1,3),3).equals(List.of(13,15));assert Solution.rollingChecksums(List.of(),0)==null;assert Solution.rollingChecksums(List.of(1),2).isEmpty();}}
''',"uses-unweighted-window-sum"),
"ordered-event-compaction": sample('''import java.util.*;public final class Solution{public static List<Integer> compactOrderedEvents(List<Integer>seq,List<String>keys,List<Integer>values){if(seq.size()!=keys.size()||seq.size()!=values.size())return null;var last=new HashMap<String,Integer>();for(int i=0;i<seq.size();i++){if(i>0&&seq.get(i)<=seq.get(i-1)||keys.get(i).isEmpty())return null;last.put(keys.get(i),i);}var out=new ArrayList<Integer>();for(int i=0;i<keys.size();i++)if(last.get(keys.get(i))==i)out.add(values.get(i));return out;}}
''','''import java.util.*;public final class Solution{public static List<Integer> compactOrderedEvents(List<Integer>seq,List<String>keys,List<Integer>values){if(seq.size()!=keys.size()||seq.size()!=values.size())return null;var seen=new HashSet<String>();var out=new ArrayList<Integer>();for(int i=0;i<keys.size();i++)if(seen.add(keys.get(i)))out.add(values.get(i));return out;}}
''','''import java.util.*;public final class SolutionTest{public static void main(String[]z){assert Solution.compactOrderedEvents(List.of(1,2,3,8),List.of("a","b","a","c"),List.of(4,7,9,2)).equals(List.of(7,9,2));assert Solution.compactOrderedEvents(List.of(2,2),List.of("a","b"),List.of(1,2))==null;assert Solution.compactOrderedEvents(List.of(1),List.of(),List.of())==null;assert Solution.compactOrderedEvents(List.of(),List.of(),List.of()).isEmpty();}}
''',"keeps-first-occurrence"),
},
"javascript": {}, "typescript": {}, "python": {}, "rust": {},
}

# JavaScript and TypeScript use the same state machines but keep distinct module/type contracts.
LANG["javascript"] = {
"ring-buffer-trace": sample("exports.ringBufferTrace=(capacity,values)=>{if(!Number.isInteger(capacity)||capacity<=0)return null;const q=[],out=[];for(const v of values){if(!Number.isSafeInteger(v)||v===-1)return null;out.push(q.length===capacity?q.shift():-1);q.push(v)}return out}\n","exports.ringBufferTrace=(capacity,values)=>capacity<=0?null:values.map(()=>-1)\n","const{ringBufferTrace:f}=require('./solution');if(JSON.stringify(f(2,[4,7,9,1]))!=='[-1,-1,4,7]'||f(0,[])!==null||f(2,[-1])!==null||JSON.stringify(f(3,[]))!=='[]')throw Error('ring');\n","never-evicts"),
"idempotency-batches": sample("exports.idempotencyBatchTrace=(keys,amounts)=>{if(keys.length!==amounts.length)return null;const seen=new Set,out=[];let total=0;for(let i=0;i<keys.length;i++){if(keys[i]==='')return null;if(!seen.has(keys[i])){seen.add(keys[i]);total+=amounts[i]}out.push(total)}return out}\n","exports.idempotencyBatchTrace=(keys,amounts)=>{if(keys.length!==amounts.length)return null;let total=0;return amounts.map(x=>total+=x)}\n","const{idempotencyBatchTrace:f}=require('./solution');if(JSON.stringify(f(['a','b','a','c'],[5,2,99,-1]))!=='[5,7,7,6]'||f(['a'],[])!==null||f([''],[1])!==null||JSON.stringify(f([],[]))!=='[]')throw Error('keys');\n","reapplies-duplicate-keys"),
"token-bucket-trace": sample("exports.tokenBucketTrace=(capacity,initial,refill,costs)=>{if([capacity,initial,refill,...costs].some(x=>!Number.isSafeInteger(x))||capacity<0||initial<0||initial>capacity||refill<0||costs.some(x=>x<0))return null;let tokens=initial;return costs.map((c,i)=>{if(i)tokens=Math.min(capacity,tokens+refill);if(c<=tokens){tokens-=c;return tokens}return -tokens-1})}\n","exports.tokenBucketTrace=(capacity,initial,refill,costs)=>{let t=initial;return costs.map(c=>(t=Math.min(capacity,t+refill)-c))}\n","const{tokenBucketTrace:f}=require('./solution');if(JSON.stringify(f(5,3,2,[2,5,1,4]))!=='[1,-4,4,1]'||f(2,3,0,[])!==null||f(2,1,0,[-1])!==null||JSON.stringify(f(0,0,0,[]))!=='[]')throw Error('bucket');\n","refills-before-first-and-spends-on-rejection"),
"rolling-checksums": sample("exports.rollingChecksums=(values,window)=>{if(!Number.isInteger(window)||window<=0)return null;const out=[];for(let i=0;i+window<=values.length;i++){let sum=0;for(let j=0;j<window;j++)sum+=(j+1)*values[i+j];out.push(sum)}return out}\n","exports.rollingChecksums=(values,window)=>{if(window<=0)return null;const out=[];for(let i=0;i+window<=values.length;i++)out.push(values.slice(i,i+window).reduce((a,b)=>a+b,0));return out}\n","const{rollingChecksums:f}=require('./solution');if(JSON.stringify(f([2,4,1,3],3))!=='[13,15]'||f([],0)!==null||JSON.stringify(f([1],2))!=='[]')throw Error('rolling');\n","uses-unweighted-window-sum"),
"ordered-event-compaction": sample("exports.compactOrderedEvents=(seq,keys,values)=>{if(seq.length!==keys.length||seq.length!==values.length)return null;const last=new Map;for(let i=0;i<seq.length;i++){if(i&&seq[i]<=seq[i-1]||keys[i]==='')return null;last.set(keys[i],i)}return values.filter((_,i)=>last.get(keys[i])===i)}\n","exports.compactOrderedEvents=(seq,keys,values)=>{if(seq.length!==keys.length||seq.length!==values.length)return null;const seen=new Set;return values.filter((_,i)=>seen.has(keys[i])?false:(seen.add(keys[i]),true))}\n","const{compactOrderedEvents:f}=require('./solution');if(JSON.stringify(f([1,2,3,8],['a','b','a','c'],[4,7,9,2]))!=='[7,9,2]'||f([2,2],['a','b'],[1,2])!==null||f([1],[],[])!==null||JSON.stringify(f([],[],[]))!=='[]')throw Error('compact');\n","keeps-first-occurrence"),
}
LANG["typescript"] = {
"ring-buffer-trace": sample("export function ringBufferTrace(capacity:number,values:readonly number[]):number[]|null{if(!Number.isInteger(capacity)||capacity<=0)return null;const q:number[]=[],out:number[]=[];for(const v of values){if(!Number.isSafeInteger(v)||v===-1)return null;out.push(q.length===capacity?q.shift()!:-1);q.push(v)}return out}\n","export function ringBufferTrace(capacity:number,values:readonly number[]):number[]|null{return capacity<=0?null:values.map(()=>-1)}\n","import{ringBufferTrace as f}from'./solution';if(JSON.stringify(f(2,[4,7,9,1]))!=='[-1,-1,4,7]'||f(0,[])!==null||f(2,[-1])!==null||JSON.stringify(f(3,[]))!=='[]')throw Error('ring');\n","never-evicts"),
"idempotency-batches": sample("export function idempotencyBatchTrace(keys:readonly string[],amounts:readonly number[]):number[]|null{if(keys.length!==amounts.length)return null;const seen=new Set<string>(),out:number[]=[];let total=0;for(let i=0;i<keys.length;i++){if(keys[i]==='')return null;if(!seen.has(keys[i])){seen.add(keys[i]);total+=amounts[i]}out.push(total)}return out}\n","export function idempotencyBatchTrace(keys:readonly string[],amounts:readonly number[]):number[]|null{if(keys.length!==amounts.length)return null;let total=0;return amounts.map(x=>total+=x)}\n","import{idempotencyBatchTrace as f}from'./solution';if(JSON.stringify(f(['a','b','a','c'],[5,2,99,-1]))!=='[5,7,7,6]'||f(['a'],[])!==null||f([''],[1])!==null||JSON.stringify(f([],[]))!=='[]')throw Error('keys');\n","reapplies-duplicate-keys"),
"token-bucket-trace": sample("export function tokenBucketTrace(capacity:number,initial:number,refill:number,costs:readonly number[]):number[]|null{if([capacity,initial,refill,...costs].some(x=>!Number.isSafeInteger(x))||capacity<0||initial<0||initial>capacity||refill<0||costs.some(x=>x<0))return null;let tokens=initial;return costs.map((c,i)=>{if(i)tokens=Math.min(capacity,tokens+refill);if(c<=tokens){tokens-=c;return tokens}return -tokens-1})}\n","export function tokenBucketTrace(capacity:number,initial:number,refill:number,costs:readonly number[]):number[]|null{let tokens=initial;return costs.map(c=>(tokens=Math.min(capacity,tokens+refill)-c))}\n","import{tokenBucketTrace as f}from'./solution';if(JSON.stringify(f(5,3,2,[2,5,1,4]))!=='[1,-4,4,1]'||f(2,3,0,[])!==null||f(2,1,0,[-1])!==null||JSON.stringify(f(0,0,0,[]))!=='[]')throw Error('bucket');\n","refills-before-first-and-spends-on-rejection"),
"rolling-checksums": sample("export function rollingChecksums(values:readonly number[],window:number):number[]|null{if(!Number.isInteger(window)||window<=0)return null;const out:number[]=[];for(let i=0;i+window<=values.length;i++){let sum=0;for(let j=0;j<window;j++)sum+=(j+1)*values[i+j];out.push(sum)}return out}\n","export function rollingChecksums(values:readonly number[],window:number):number[]|null{if(window<=0)return null;const out:number[]=[];for(let i=0;i+window<=values.length;i++)out.push(values.slice(i,i+window).reduce((a,b)=>a+b,0));return out}\n","import{rollingChecksums as f}from'./solution';if(JSON.stringify(f([2,4,1,3],3))!=='[13,15]'||f([],0)!==null||JSON.stringify(f([1],2))!=='[]')throw Error('rolling');\n","uses-unweighted-window-sum"),
"ordered-event-compaction": sample("export function compactOrderedEvents(seq:readonly number[],keys:readonly string[],values:readonly number[]):number[]|null{if(seq.length!==keys.length||seq.length!==values.length)return null;const last=new Map<string,number>();for(let i=0;i<seq.length;i++){if(i&&seq[i]<=seq[i-1]||keys[i]==='')return null;last.set(keys[i],i)}return values.filter((_,i)=>last.get(keys[i])===i)}\n","export function compactOrderedEvents(seq:readonly number[],keys:readonly string[],values:readonly number[]):number[]|null{if(seq.length!==keys.length||seq.length!==values.length)return null;const seen=new Set<string>();return values.filter((_,i)=>seen.has(keys[i])?false:(seen.add(keys[i]),true))}\n","import{compactOrderedEvents as f}from'./solution';if(JSON.stringify(f([1,2,3,8],['a','b','a','c'],[4,7,9,2]))!=='[7,9,2]'||f([2,2],['a','b'],[1,2])!==null||f([1],[],[])!==null||JSON.stringify(f([],[],[]))!=='[]')throw Error('compact');\n","keeps-first-occurrence"),
}
LANG["python"] = {
"ring-buffer-trace": sample("def ring_buffer_trace(capacity: int, values: list[int]) -> list[int] | None:\n    if type(capacity) is not int or capacity<=0:return None\n    q=[];out=[]\n    for value in values:\n        if type(value) is not int or value==-1:return None\n        out.append(q.pop(0) if len(q)==capacity else -1);q.append(value)\n    return out\n","def ring_buffer_trace(capacity: int, values: list[int]) -> list[int] | None:\n    if capacity<=0:return None\n    return [-1 for _ in values]\n","from solution import ring_buffer_trace as f\nassert f(2,[4,7,9,1])==[-1,-1,4,7] and f(0,[]) is None and f(2,[-1]) is None and f(3,[])==[]\n","never-evicts"),
"idempotency-batches": sample("def idempotency_batch_trace(keys: list[str], amounts: list[int]) -> list[int] | None:\n    if len(keys)!=len(amounts):return None\n    seen=set();out=[];total=0\n    for key,amount in zip(keys,amounts):\n        if key=='':return None\n        if key not in seen:seen.add(key);total+=amount\n        out.append(total)\n    return out\n","def idempotency_batch_trace(keys: list[str], amounts: list[int]) -> list[int] | None:\n    if len(keys)!=len(amounts):return None\n    out=[];total=0\n    for amount in amounts:total+=amount;out.append(total)\n    return out\n","from solution import idempotency_batch_trace as f\nassert f(['a','b','a','c'],[5,2,99,-1])==[5,7,7,6] and f(['a'],[]) is None and f([''],[1]) is None and f([],[])==[]\n","reapplies-duplicate-keys"),
"token-bucket-trace": sample("def token_bucket_trace(capacity:int,initial:int,refill:int,costs:list[int])->list[int]|None:\n    if any(type(x) is not int for x in [capacity,initial,refill,*costs]) or capacity<0 or initial<0 or initial>capacity or refill<0 or any(x<0 for x in costs):return None\n    tokens=initial;out=[]\n    for i,cost in enumerate(costs):\n        if i:tokens=min(capacity,tokens+refill)\n        if cost<=tokens:tokens-=cost;out.append(tokens)\n        else:out.append(-tokens-1)\n    return out\n","def token_bucket_trace(capacity:int,initial:int,refill:int,costs:list[int])->list[int]|None:\n    tokens=initial;out=[]\n    for cost in costs:tokens=min(capacity,tokens+refill)-cost;out.append(tokens)\n    return out\n","from solution import token_bucket_trace as f\nassert f(5,3,2,[2,5,1,4])==[1,-4,4,1] and f(2,3,0,[]) is None and f(2,1,0,[-1]) is None and f(0,0,0,[])==[]\n","refills-before-first-and-spends-on-rejection"),
"rolling-checksums": sample("def rolling_checksums(values:list[int],window:int)->list[int]|None:\n    if type(window) is not int or window<=0:return None\n    return [sum((j+1)*values[i+j] for j in range(window)) for i in range(len(values)-window+1)]\n","def rolling_checksums(values:list[int],window:int)->list[int]|None:\n    if window<=0:return None\n    return [sum(values[i:i+window]) for i in range(len(values)-window+1)]\n","from solution import rolling_checksums as f\nassert f([2,4,1,3],3)==[13,15] and f([],0) is None and f([1],2)==[]\n","uses-unweighted-window-sum"),
"ordered-event-compaction": sample("def compact_ordered_events(seq:list[int],keys:list[str],values:list[int])->list[int]|None:\n    if len(seq)!=len(keys) or len(seq)!=len(values):return None\n    last={}\n    for i,(number,key) in enumerate(zip(seq,keys)):\n        if (i and number<=seq[i-1]) or key=='':return None\n        last[key]=i\n    return [value for i,value in enumerate(values) if last[keys[i]]==i]\n","def compact_ordered_events(seq:list[int],keys:list[str],values:list[int])->list[int]|None:\n    if len(seq)!=len(keys) or len(seq)!=len(values):return None\n    seen=set();out=[]\n    for key,value in zip(keys,values):\n        if key not in seen:seen.add(key);out.append(value)\n    return out\n","from solution import compact_ordered_events as f\nassert f([1,2,3,8],['a','b','a','c'],[4,7,9,2])==[7,9,2] and f([2,2],['a','b'],[1,2]) is None and f([1],[],[]) is None and f([],[],[])==[]\n","keeps-first-occurrence"),
}
LANG["rust"] = {
"ring-buffer-trace": sample("use std::collections::VecDeque;pub fn ring_buffer_trace(capacity:usize,values:&[i32])->Option<Vec<i32>>{if capacity==0{return None}let mut q=VecDeque::new();let mut out=Vec::new();for &v in values{if v== -1{return None}out.push(if q.len()==capacity{q.pop_front().unwrap()}else{-1});q.push_back(v)}Some(out)}\n","pub fn ring_buffer_trace(capacity:usize,values:&[i32])->Option<Vec<i32>>{if capacity==0{return None}Some(vec![-1;values.len()])}\n","#[path=\"solution.rs\"]mod solution;#[test]fn test(){assert_eq!(solution::ring_buffer_trace(2,&[4,7,9,1]),Some(vec![-1,-1,4,7]));assert_eq!(solution::ring_buffer_trace(0,&[]),None);assert_eq!(solution::ring_buffer_trace(2,&[-1]),None);assert_eq!(solution::ring_buffer_trace(3,&[]),Some(vec![]));}\n","never-evicts"),
"idempotency-batches": sample("use std::collections::HashSet;pub fn idempotency_batch_trace(keys:&[String],amounts:&[i32])->Option<Vec<i32>>{if keys.len()!=amounts.len(){return None}let mut seen=HashSet::new();let mut out=Vec::new();let mut total=0;for(k,&a)in keys.iter().zip(amounts){if k.is_empty(){return None}if seen.insert(k){total+=a}out.push(total)}Some(out)}\n","pub fn idempotency_batch_trace(keys:&[String],amounts:&[i32])->Option<Vec<i32>>{if keys.len()!=amounts.len(){return None}let mut total=0;Some(amounts.iter().map(|a|{total+=a;total}).collect())}\n","#[path=\"solution.rs\"]mod solution;#[test]fn test(){let k:Vec<String>=[\"a\",\"b\",\"a\",\"c\"].map(String::from).to_vec();assert_eq!(solution::idempotency_batch_trace(&k,&[5,2,99,-1]),Some(vec![5,7,7,6]));assert_eq!(solution::idempotency_batch_trace(&k[..1],&[]),None);assert_eq!(solution::idempotency_batch_trace(&[String::new()],&[1]),None);assert_eq!(solution::idempotency_batch_trace(&[],&[]),Some(vec![]));}\n","reapplies-duplicate-keys"),
"token-bucket-trace": sample("pub fn token_bucket_trace(capacity:i32,initial:i32,refill:i32,costs:&[i32])->Option<Vec<i32>>{if capacity<0||initial<0||initial>capacity||refill<0||costs.iter().any(|&x|x<0){return None}let mut tokens=initial;let mut out=Vec::new();for(i,&cost)in costs.iter().enumerate(){if i>0{tokens=(tokens+refill).min(capacity)}if cost<=tokens{tokens-=cost;out.push(tokens)}else{out.push(-tokens-1)}}Some(out)}\n","pub fn token_bucket_trace(capacity:i32,initial:i32,refill:i32,costs:&[i32])->Option<Vec<i32>>{let mut tokens=initial;Some(costs.iter().map(|&c|{tokens=(tokens+refill).min(capacity)-c;tokens}).collect())}\n","#[path=\"solution.rs\"]mod solution;#[test]fn test(){assert_eq!(solution::token_bucket_trace(5,3,2,&[2,5,1,4]),Some(vec![1,-4,4,1]));assert_eq!(solution::token_bucket_trace(2,3,0,&[]),None);assert_eq!(solution::token_bucket_trace(2,1,0,&[-1]),None);assert_eq!(solution::token_bucket_trace(0,0,0,&[]),Some(vec![]));}\n","refills-before-first-and-spends-on-rejection"),
"rolling-checksums": sample("pub fn rolling_checksums(values:&[i32],window:usize)->Option<Vec<i32>>{if window==0{return None}if window>values.len(){return Some(vec![])}Some((0..=values.len()-window).map(|i|(0..window).map(|j|(j as i32+1)*values[i+j]).sum()).collect())}\n","pub fn rolling_checksums(values:&[i32],window:usize)->Option<Vec<i32>>{if window==0{return None}if window>values.len(){return Some(vec![])}Some(values.windows(window).map(|w|w.iter().sum()).collect())}\n","#[path=\"solution.rs\"]mod solution;#[test]fn test(){assert_eq!(solution::rolling_checksums(&[2,4,1,3],3),Some(vec![13,15]));assert_eq!(solution::rolling_checksums(&[],0),None);assert_eq!(solution::rolling_checksums(&[1],2),Some(vec![]));}\n","uses-unweighted-window-sum"),
"ordered-event-compaction": sample("use std::collections::HashMap;pub fn compact_ordered_events(seq:&[i32],keys:&[String],values:&[i32])->Option<Vec<i32>>{if seq.len()!=keys.len()||seq.len()!=values.len(){return None}let mut last=HashMap::new();for i in 0..seq.len(){if i>0&&seq[i]<=seq[i-1]||keys[i].is_empty(){return None}last.insert(&keys[i],i);}Some((0..values.len()).filter(|&i|last[&keys[i]]==i).map(|i|values[i]).collect())}\n","use std::collections::HashSet;pub fn compact_ordered_events(seq:&[i32],keys:&[String],values:&[i32])->Option<Vec<i32>>{if seq.len()!=keys.len()||seq.len()!=values.len(){return None}let mut seen=HashSet::new();Some((0..values.len()).filter(|&i|seen.insert(&keys[i])).map(|i|values[i]).collect())}\n","#[path=\"solution.rs\"]mod solution;#[test]fn test(){let k:Vec<String>=[\"a\",\"b\",\"a\",\"c\"].map(String::from).to_vec();assert_eq!(solution::compact_ordered_events(&[1,2,3,8],&k,&[4,7,9,2]),Some(vec![7,9,2]));assert_eq!(solution::compact_ordered_events(&[2,2],&k[..2],&[1,2]),None);assert_eq!(solution::compact_ordered_events(&[1],&[],&[]),None);assert_eq!(solution::compact_ordered_events(&[],&[],&[]),Some(vec![]));}\n","keeps-first-occurrence"),
}

API = {
"go":{"ring-buffer-trace":"func RingBufferTrace(capacity int, values []int) ([]int, bool)","idempotency-batches":"func IdempotencyBatchTrace(keys []string, amounts []int) ([]int, bool)","token-bucket-trace":"func TokenBucketTrace(capacity, initial, refill int, costs []int) ([]int, bool)","rolling-checksums":"func RollingChecksums(values []int, window int) ([]int, bool)","ordered-event-compaction":"func CompactOrderedEvents(seq []int, keys []string, values []int) ([]int, bool)"},
"java":{"ring-buffer-trace":"public static List<Integer> ringBufferTrace(int capacity, List<Integer> values)","idempotency-batches":"public static List<Integer> idempotencyBatchTrace(List<String> keys, List<Integer> amounts)","token-bucket-trace":"public static List<Integer> tokenBucketTrace(int capacity, int initial, int refill, List<Integer> costs)","rolling-checksums":"public static List<Integer> rollingChecksums(List<Integer> values, int window)","ordered-event-compaction":"public static List<Integer> compactOrderedEvents(List<Integer> seq, List<String> keys, List<Integer> values)"},
"javascript":{"ring-buffer-trace":"exports.ringBufferTrace = function(capacity, values) returning number[] | null","idempotency-batches":"exports.idempotencyBatchTrace = function(keys, amounts) returning number[] | null","token-bucket-trace":"exports.tokenBucketTrace = function(capacity, initial, refill, costs) returning number[] | null","rolling-checksums":"exports.rollingChecksums = function(values, window) returning number[] | null","ordered-event-compaction":"exports.compactOrderedEvents = function(seq, keys, values) returning number[] | null"},
"typescript":{"ring-buffer-trace":"export function ringBufferTrace(capacity: number, values: readonly number[]): number[] | null","idempotency-batches":"export function idempotencyBatchTrace(keys: readonly string[], amounts: readonly number[]): number[] | null","token-bucket-trace":"export function tokenBucketTrace(capacity: number, initial: number, refill: number, costs: readonly number[]): number[] | null","rolling-checksums":"export function rollingChecksums(values: readonly number[], window: number): number[] | null","ordered-event-compaction":"export function compactOrderedEvents(seq: readonly number[], keys: readonly string[], values: readonly number[]): number[] | null"},
"python":{"ring-buffer-trace":"def ring_buffer_trace(capacity: int, values: list[int]) -> list[int] | None","idempotency-batches":"def idempotency_batch_trace(keys: list[str], amounts: list[int]) -> list[int] | None","token-bucket-trace":"def token_bucket_trace(capacity: int, initial: int, refill: int, costs: list[int]) -> list[int] | None","rolling-checksums":"def rolling_checksums(values: list[int], window: int) -> list[int] | None","ordered-event-compaction":"def compact_ordered_events(seq: list[int], keys: list[str], values: list[int]) -> list[int] | None"},
"rust":{"ring-buffer-trace":"pub fn ring_buffer_trace(capacity: usize, values: &[i32]) -> Option<Vec<i32>>","idempotency-batches":"pub fn idempotency_batch_trace(keys: &[String], amounts: &[i32]) -> Option<Vec<i32>>","token-bucket-trace":"pub fn token_bucket_trace(capacity: i32, initial: i32, refill: i32, costs: &[i32]) -> Option<Vec<i32>>","rolling-checksums":"pub fn rolling_checksums(values: &[i32], window: usize) -> Option<Vec<i32>>","ordered-event-compaction":"pub fn compact_ordered_events(seq: &[i32], keys: &[String], values: &[i32]) -> Option<Vec<i32>>"},
}
FILE_CONTRACT={"go":"Write package solution in solution.go with the function at package scope.","java":"Write final class Solution in Solution.java with the static method shown; java.util types may be imported.","javascript":"Write CommonJS module solution.js and export the named function.","typescript":"Write strict TypeScript module solution.ts and export the named function.","python":"Write solution.py with the function at module scope.","rust":"Write solution.rs with the public function at module scope; use only the standard library."}
BEHAVIOR={
"ring-buffer-trace":"Simulate a fixed-capacity FIFO ring. Each value is pushed; emit the evicted oldest value, or -1 when no eviction occurs. Reject non-positive capacity and input value -1, which is reserved as the sentinel. Do not mutate input; empty input succeeds.",
"idempotency-batches":"Process aligned idempotency keys and signed amounts in arrival order. Apply only the first amount for each key and emit the cumulative total after every arrival. Reject unequal lengths or an empty key; empty input succeeds.",
"token-bucket-trace":"Start with initial tokens. Before every request except the first, refill and cap at capacity. If cost is affordable, spend it and emit remaining tokens; otherwise keep state and emit -(available+1). Reject invalid negative settings/costs or initial above capacity; empty costs succeeds.",
"rolling-checksums":"For every complete window, emit the position-weighted checksum sum((offset+1)*value). Reject a zero window (and negative where representable). A window longer than input returns a non-null empty result; do not mutate input.",
"ordered-event-compaction":"The three arrays encode events with strictly increasing sequence numbers. Reject unequal lengths, non-increasing sequence numbers, or empty keys. Keep only the final event for each key and return its value, ordered by the final events' positions; empty input succeeds.",
}
EXAMPLE={
"ring-buffer-trace":"capacity 2 with values [4,7,9,1] returns [-1,-1,4,7].",
"idempotency-batches":"keys [a,b,a,c] and amounts [5,2,99,-1] return [5,7,7,6].",
"token-bucket-trace":"capacity 5, initial 3, refill 2, costs [2,5,1,4] return [1,-4,4,1]; -4 records rejection with 3 available tokens.",
"rolling-checksums":"values [2,4,1,3] with window 3 return [13,15].",
"ordered-event-compaction":"seq [1,2,3,8], keys [a,b,a,c], values [4,7,9,2] return [7,9,2].",
}


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def make_task(language: str, slug: str, kind: str) -> dict[str, Any]:
    item=LANG[language][slug]
    lead="Implement the following API." if kind=="generation" else "Repair the buggy source below without changing the required API."
    prompt=f"{lead}\n\nFile contract: {FILE_CONTRACT[language]}\nRequired API: {API[language][slug]}\nBehavior: {BEHAVIOR[slug]}\nVisible example: {EXAMPLE[slug]}\n"
    if kind=="repair":prompt+=f"\nBuggy source to repair:\n\n{item['bad']}"
    prompt+="\nReturn only the complete source file; do not include Markdown fences or prose."
    files=[]
    if language=="go":
        module="module private.invalid/ganesh/development/tranche5\n\ngo 1.22\n";files.append({"path":"go.mod","role":"support","content":module,"sha256":sha256_text(module)});test_path="solution_test.go"
    else:test_path={"java":"SolutionTest.java","javascript":"solution.test.js","typescript":"solution.test.ts","python":"test_solution.py","rust":"solution_test.rs"}[language]
    files.append({"path":test_path,"role":"test","content":item["test"],"sha256":sha256_text(item["test"])})
    task={"schema_version":"1.0","task_id":f"dev-t5-{language}-{slug}","surface":"development","language":language,"family":LANGUAGE_FAMILY[language],"task_type":kind,"prompt":{"text":prompt,"sha256":sha256_text(prompt)},"rendered_prompt":{"text":prompt,"sha256":sha256_text(prompt)},"candidate_path":CANDIDATE_PATH[language],"files":files,"runtime_id":RUNTIME[language],"limits":{"timeout_seconds":30,"memory_mb":512,"cpus":1,"pids":64,"output_bytes":65536},"validation":{"reference":{"label":"author-reference","code":item["reference"],"sha256":sha256_text(item["reference"])},"known_bad":[{"label":item["bad_label"],"code":item["bad"],"sha256":sha256_text(item["bad"])}]}}
    return validate_task(task)


def comparison_fingerprints()->tuple[set[str],set[str],int,dict[str,int]]:
    exact:set[str]=set();norm:set[str]=set();counts={"seed":0,"private_development":0}
    for relative in ("data/seed/ganesh_v01/train.jsonl","data/seed/ganesh_v01/validation.jsonl"):
        for line in (ROOT/relative).read_text(encoding="utf-8").splitlines():
            text=json.loads(line)["messages"][0]["content"];exact.add(sha256_text(text));norm.add(sha256_text(normalized(text)));counts["seed"]+=1
    # This tranche is bound to the four surfaces sealed before authoring began.
    # A concurrently authored later tranche must not change this manifest's hash.
    for tranche in ("tranche1", "tranche2", "tranche3", "tranche4"):
        for path in sorted((ROOT/"eval/private/development"/tranche).glob("*.task.json")):
            text=json.loads(path.read_text(encoding="utf-8"))["prompt"]["text"];exact.add(sha256_text(text));norm.add(sha256_text(normalized(text)));counts["private_development"]+=1
    return exact,norm,sum(counts.values()),counts


def build()->tuple[dict[str,Any],dict[str,Any]]:
    OUT.mkdir(parents=True,exist_ok=True)
    tasks=[make_task(language,slug,kind) for language,kinds in KINDS.items() for slug,kind in zip(SLUGS,kinds)]
    exact,norm,total,counts=comparison_fingerprints()
    exact_hits=[t["task_id"] for t in tasks if t["prompt"]["sha256"] in exact];norm_hits=[t["task_id"] for t in tasks if sha256_text(normalized(t["prompt"]["text"])) in norm]
    own_exact=[t["task_id"] for t in tasks if sum(x["prompt"]["sha256"]==t["prompt"]["sha256"] for x in tasks)>1];own_norm=[t["task_id"] for t in tasks if sum(normalized(x["prompt"]["text"])==normalized(t["prompt"]["text"]) for x in tasks)>1]
    if exact_hits or norm_hits or own_exact or own_norm:raise RuntimeError("tranche5 prompt overlap detected")
    entries=[]
    for task in tasks:
        path=OUT/f"{task['task_id']}.task.json";write_json(path,task);entries.append({"task_id":task["task_id"],"language":task["language"],"task_type":task["task_type"],"path":str(path.relative_to(ROOT)),"sha256":sha256_object(task),"prompt_sha256":task["prompt"]["sha256"],"rendered_prompt_sha256":task["rendered_prompt"]["sha256"]})
    counter=Counter((t["language"],t["task_type"])for t in tasks)
    manifest={"schema_version":"ganesh-mini-private-eval-manifest/v1","surface":"development","tranche":"tranche5","status":"authored","task_count":len(tasks),"counts_by_lane":{l:{k:counter[(l,k)]for k in("generation","repair")}for l in RUNTIME},"runtime_config":"configs/eval/runtimes.json","tasks":entries};manifest["manifest_sha256"]=sha256_object(manifest)
    overlap={"schema_version":"ganesh-mini-evaluation-overlap/v1","evaluation_manifest":str(MANIFEST.relative_to(ROOT)),"evaluation_manifest_sha256":manifest["manifest_sha256"],"seed_manifest":"manifests/datasets/ganesh_v01_seed.json","seed_records_inspected":counts["seed"],"other_private_development_prompts_inspected":counts["private_development"],"comparison_prompts_inspected":total,"evaluation_prompts_inspected":len(tasks),"normalization":"NFKC + Unicode casefold + whitespace collapse","exact_prompt_overlaps":exact_hits,"normalized_prompt_overlaps":norm_hits,"within_tranche_exact_overlaps":own_exact,"within_tranche_normalized_overlaps":own_norm,"status":"passed"};overlap["report_sha256"]=sha256_object(overlap)
    write_json(MANIFEST,manifest);write_json(OVERLAP,overlap);return manifest,overlap


if __name__=="__main__":
    manifest,overlap=build();print(json.dumps({"tasks":manifest["task_count"],"manifest_sha256":manifest["manifest_sha256"],"overlap_sha256":overlap["report_sha256"]},sort_keys=True))
