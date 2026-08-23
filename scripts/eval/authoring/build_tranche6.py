#!/usr/bin/env python3
"""Build and audit private development tranche 6 deterministically."""

from __future__ import annotations

import json
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.eval.contracts import CANDIDATE_PATH, LANGUAGE_FAMILY, sha256_object, sha256_text, validate_task, write_json

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "eval/private/development/tranche6"
MANIFEST = ROOT / "manifests/evaluation/private/development-tranche6.json"
OVERLAP = ROOT / "manifests/evaluation/private/development-tranche6-overlap.json"
RUNTIME = {"go":"go-1.22.12","java":"java-21.0.11","javascript":"javascript-node-22.23.2","typescript":"typescript-5.5.4-node-22","python":"python-3.11.15","rust":"rust-1.85.0"}
KINDS = {
    "go": ("generation","generation","generation","repair","repair"),
    "java": ("generation","generation","repair","repair","repair"),
    "javascript": ("generation","generation","generation","repair","repair"),
    "typescript": ("generation","generation","repair","repair","repair"),
    "python": ("generation","generation","generation","repair","repair"),
    "rust": ("generation","generation","repair","repair","repair"),
}
SLUGS = ("configuration-patch","ledger-reconciliation","permission-inheritance","bounded-window-summary","version-change-order")


def s(reference: str, bad: str, test: str, label: str) -> dict[str, str]:
    return {"reference": reference, "bad": bad, "test": test, "bad_label": label}


LANG: dict[str, dict[str, dict[str, str]]] = {
"go": {
"configuration-patch": s(r'''package solution
import "sort"
func PatchConfig(base map[string]string, patches [][3]string)([]string,bool){m:=map[string]string{};for k,v:=range base{if k==""{return nil,false};m[k]=v};for _,p:=range patches{if p[1]==""{return nil,false};switch p[0]{case "set":m[p[1]]=p[2];case "unset":delete(m,p[1]);default:return nil,false}};o:=make([]string,0,len(m));for k,v:=range m{o=append(o,k+"="+v)};sort.Strings(o);return o,true}
''', r'''package solution
import "sort"
func PatchConfig(base map[string]string, patches [][3]string)([]string,bool){m:=map[string]string{};for k,v:=range base{m[k]=v};for _,p:=range patches{if p[0]=="set"{m[p[1]]=p[2]}};o:=[]string{};for k,v:=range m{o=append(o,k+"="+v)};sort.Strings(o);return o,true}
''', r'''package solution
import("reflect";"testing")
func TestPatch(t *testing.T){b:=map[string]string{"mode":"safe","zone":"in"};g,ok:=PatchConfig(b,[][3]string{{"unset","zone","ignored"},{"set","mode","fast"},{"set","new",""}});if !ok||!reflect.DeepEqual(g,[]string{"mode=fast","new="})||b["mode"]!="safe"{t.Fatal(g,ok,b)};if _,ok:=PatchConfig(b,[][3]string{{"merge","x","y"}});ok{t.Fatal("op")};if _,ok:=PatchConfig(b,[][3]string{{"set","","y"}});ok{t.Fatal("key")}}
''', "ignores-unset-and-validation"),
"ledger-reconciliation": s(r'''package solution
func ReconcileLedger(opening int64,entries [][3]int64)(int64,bool){seen:=map[int64]bool{};b:=opening;for _,e:=range entries{if seen[e[0]]||e[2]<=0||(e[1]!=1&&e[1]!=-1){return 0,false};seen[e[0]]=true;if e[1]==1{b+=e[2]}else{b-=e[2]}};return b,true}
''', r'''package solution
func ReconcileLedger(opening int64,entries [][3]int64)(int64,bool){b:=opening;for _,e:=range entries{b+=e[1]*e[2]};return b,true}
''', r'''package solution
import "testing"
func TestLedger(t *testing.T){if g,ok:=ReconcileLedger(100,[][3]int64{{7,1,25},{8,-1,40}});!ok||g!=85{t.Fatal(g,ok)};for _,x:=range [][][3]int64{{{7,1,2},{7,-1,1}},{{1,0,4}},{{1,1,0}}}{if _,ok:=ReconcileLedger(0,x);ok{t.Fatal(x)}};if g,ok:=ReconcileLedger(-2,nil);!ok||g!=-2{t.Fatal(g,ok)}}
''', "accepts-duplicate-and-invalid-entries"),
"permission-inheritance": s(r'''package solution
import "sort"
func ResolvePermissions(role string,parents map[string]string,grants map[string][]string)([]string,bool){known:=func(x string)bool{_,a:=parents[x];_,b:=grants[x];return a||b};if !known(role){return nil,false};seen:=map[string]bool{};perms:=map[string]bool{};for role!=""{if seen[role]||!known(role){return nil,false};seen[role]=true;for _,p:=range grants[role]{perms[p]=true};role=parents[role]};o:=make([]string,0,len(perms));for p:=range perms{o=append(o,p)};sort.Strings(o);return o,true}
''', r'''package solution
import "sort"
func ResolvePermissions(role string,parents map[string]string,grants map[string][]string)([]string,bool){o:=append([]string(nil),grants[role]...);sort.Strings(o);return o,true}
''', r'''package solution
import("reflect";"testing")
func TestPerms(t *testing.T){p:=map[string]string{"editor":"viewer","viewer":""};g:=map[string][]string{"editor":{"write","read"},"viewer":{"read","view"}};x,ok:=ResolvePermissions("editor",p,g);if !ok||!reflect.DeepEqual(x,[]string{"read","view","write"}){t.Fatal(x,ok)};if _,ok:=ResolvePermissions("missing",p,g);ok{t.Fatal("unknown")};if _,ok:=ResolvePermissions("a",map[string]string{"a":"b","b":"a"},map[string][]string{"a":{},"b":{}});ok{t.Fatal("cycle")}}
''', "returns-direct-grants-only"),
"bounded-window-summary": s(r'''package solution
import "sort"
func WindowSummary(events [][2]int64,start,end int64,limit int)([2]int64,bool){if start>end||limit<0{return [2]int64{},false};type x struct{t,v int64;i int};a:=[]x{};for i,e:=range events{if e[0]>=start&&e[0]<end{a=append(a,x{e[0],e[1],i})}};sort.SliceStable(a,func(i,j int)bool{return a[i].t<a[j].t});if len(a)>limit{a=a[len(a)-limit:]};var sum int64;for _,e:=range a{sum+=e.v};return [2]int64{int64(len(a)),sum},true}
''', r'''package solution
func WindowSummary(events [][2]int64,start,end int64,limit int)([2]int64,bool){var r [2]int64;for _,e:=range events{if e[0]>=start&&e[0]<=end&&r[0]<int64(limit){r[0]++;r[1]+=e[1]}};return r,true}
''', r'''package solution
import "testing"
func TestWindow(t *testing.T){g,ok:=WindowSummary([][2]int64{{8,5},{3,2},{8,7},{10,99},{6,4}},3,10,3);if !ok||g!=[2]int64{3,16}{t.Fatal(g,ok)};if g,ok:=WindowSummary([][2]int64{{3,9}},3,3,2);!ok||g!=[2]int64{}{t.Fatal(g,ok)};if g,ok:=WindowSummary([][2]int64{{4,9}},0,5,0);!ok||g!=[2]int64{}{t.Fatal(g,ok)};if _,ok:=WindowSummary(nil,5,4,1);ok{t.Fatal("bounds")}}
''', "uses-inclusive-end-and-first-events"),
"version-change-order": s(r'''package solution
import "sort"
func OrderChanges(changes [][5]int)([]int,bool){a:=append([][5]int(nil),changes...);seen:=map[int]bool{};for _,c:=range a{if seen[c[0]]||c[1]<0||c[2]<0||c[3]<0||c[4]<0{return nil,false};seen[c[0]]=true};sort.Slice(a,func(i,j int)bool{for _,k:=range []int{1,2,3,4,0}{if a[i][k]!=a[j][k]{return a[i][k]<a[j][k]}};return false});o:=make([]int,len(a));for i,c:=range a{o[i]=c[0]};return o,true}
''', r'''package solution
import "sort"
func OrderChanges(changes [][5]int)([]int,bool){sort.Slice(changes,func(i,j int)bool{return changes[i][4]<changes[j][4]});o:=[]int{};for _,c:=range changes{o=append(o,c[0])};return o,true}
''', r'''package solution
import("reflect";"testing")
func TestOrder(t *testing.T){in:=[][5]int{{9,1,10,0,1},{4,1,2,0,5},{3,1,2,0,1},{2,1,2,0,1}};g,ok:=OrderChanges(in);if !ok||!reflect.DeepEqual(g,[]int{2,3,4,9})||in[0][0]!=9{t.Fatal(g,ok,in)};if _,ok:=OrderChanges([][5]int{{1,1,0,0,0},{1,2,0,0,0}});ok{t.Fatal("id")};if _,ok:=OrderChanges([][5]int{{1,-1,0,0,0}});ok{t.Fatal("version")}}
''', "orders-by-sequence-only-and-mutates"),
},
"java": {
"configuration-patch": s('''import java.util.*;public final class Solution{public static List<String> patchConfig(Map<String,String>b,List<String[]>p){var m=new HashMap<>(b);if(m.containsKey(""))return null;for(var x:p){if(x.length!=3||x[1].isEmpty())return null;if(x[0].equals("set"))m.put(x[1],x[2]);else if(x[0].equals("unset"))m.remove(x[1]);else return null;}var o=new ArrayList<String>();m.forEach((k,v)->o.add(k+"="+v));Collections.sort(o);return o;}}\n''','''import java.util.*;public final class Solution{public static List<String> patchConfig(Map<String,String>b,List<String[]>p){var m=new HashMap<>(b);for(var x:p)if(x[0].equals("set"))m.put(x[1],x[2]);var o=new ArrayList<String>();m.forEach((k,v)->o.add(k+"="+v));Collections.sort(o);return o;}}\n''','''import java.util.*;public final class SolutionTest{public static void main(String[]z){var b=new HashMap<String,String>(Map.of("mode","safe","zone","in"));var g=Solution.patchConfig(b,List.of(new String[]{"unset","zone","x"},new String[]{"set","mode","fast"},new String[]{"set","new",""}));assert g.equals(List.of("mode=fast","new="))&&b.get("mode").equals("safe");assert Solution.patchConfig(b,List.<String[]>of(new String[]{"merge","x","y"}))==null;assert Solution.patchConfig(b,List.<String[]>of(new String[]{"set","","y"}))==null;}}\n''',"ignores-unset-and-validation"),
"ledger-reconciliation": s('''import java.util.*;public final class Solution{public static Long reconcileLedger(long opening,List<long[]>e){var seen=new HashSet<Long>();long b=opening;for(var x:e){if(x.length!=3||!seen.add(x[0])||x[2]<=0||(x[1]!=1&&x[1]!=-1))return null;b+=x[1]*x[2];}return b;}}\n''','''import java.util.*;public final class Solution{public static Long reconcileLedger(long opening,List<long[]>e){long b=opening;for(var x:e)b+=x[1]*x[2];return b;}}\n''','''import java.util.*;public final class SolutionTest{public static void main(String[]z){assert Solution.reconcileLedger(100,List.of(new long[]{7,1,25},new long[]{8,-1,40}))==85;assert Solution.reconcileLedger(0,List.of(new long[]{7,1,2},new long[]{7,-1,1}))==null;assert Solution.reconcileLedger(0,List.of(new long[]{1,0,4}))==null;assert Solution.reconcileLedger(0,List.of(new long[]{1,1,0}))==null;assert Solution.reconcileLedger(-2,List.of())==-2;}}\n''',"accepts-duplicate-and-invalid-entries"),
"permission-inheritance": s('''import java.util.*;public final class Solution{public static List<String> resolvePermissions(String role,Map<String,String>parents,Map<String,List<String>>grants){var seen=new HashSet<String>();var out=new TreeSet<String>();while(!role.isEmpty()){if(!parents.containsKey(role)&&!grants.containsKey(role)||!seen.add(role))return null;out.addAll(grants.getOrDefault(role,List.of()));role=parents.getOrDefault(role,"");}return new ArrayList<>(out);}}\n''','''import java.util.*;public final class Solution{public static List<String> resolvePermissions(String role,Map<String,String>parents,Map<String,List<String>>grants){var o=new ArrayList<>(grants.getOrDefault(role,List.of()));Collections.sort(o);return o;}}\n''','''import java.util.*;public final class SolutionTest{public static void main(String[]z){var p=Map.of("editor","viewer","viewer","");var g=Map.of("editor",List.of("write","read"),"viewer",List.of("read","view"));assert Solution.resolvePermissions("editor",p,g).equals(List.of("read","view","write"));assert Solution.resolvePermissions("missing",p,g)==null;assert Solution.resolvePermissions("a",Map.of("a","b","b","a"),Map.of("a",List.of(),"b",List.of()))==null;}}\n''',"returns-direct-grants-only"),
"bounded-window-summary": s('''import java.util.*;public final class Solution{public static long[] windowSummary(List<long[]>e,long start,long end,int limit){if(start>end||limit<0)return null;var a=new ArrayList<long[]>();for(int i=0;i<e.size();i++){var x=e.get(i);if(x[0]>=start&&x[0]<end)a.add(new long[]{x[0],x[1],i});}a.sort(Comparator.comparingLong(x->x[0]));if(a.size()>limit)a=new ArrayList<>(a.subList(a.size()-limit,a.size()));long s=0;for(var x:a)s+=x[1];return new long[]{a.size(),s};}}\n''','''import java.util.*;public final class Solution{public static long[] windowSummary(List<long[]>e,long start,long end,int limit){long n=0,s=0;for(var x:e)if(x[0]>=start&&x[0]<=end&&n<limit){n++;s+=x[1];}return new long[]{n,s};}}\n''','''import java.util.*;public final class SolutionTest{static boolean q(long[]a,long...b){return Arrays.equals(a,b);}public static void main(String[]z){assert q(Solution.windowSummary(List.of(new long[]{8,5},new long[]{3,2},new long[]{8,7},new long[]{10,99},new long[]{6,4}),3,10,3),3,16);assert q(Solution.windowSummary(List.of(new long[]{3,9}),3,3,2),0,0);assert q(Solution.windowSummary(List.of(new long[]{4,9}),0,5,0),0,0);assert Solution.windowSummary(List.of(),5,4,1)==null;}}\n''',"uses-inclusive-end-and-first-events"),
"version-change-order": s('''import java.util.*;public final class Solution{public static List<Integer> orderChanges(List<int[]>v){var a=new ArrayList<int[]>();var seen=new HashSet<Integer>();for(var x:v){if(x.length!=5||!seen.add(x[0])||x[1]<0||x[2]<0||x[3]<0||x[4]<0)return null;a.add(x.clone());}a.sort((x,y)->{for(int k:new int[]{1,2,3,4,0}){int c=Integer.compare(x[k],y[k]);if(c!=0)return c;}return 0;});var o=new ArrayList<Integer>();for(var x:a)o.add(x[0]);return o;}}\n''','''import java.util.*;public final class Solution{public static List<Integer> orderChanges(List<int[]>v){v.sort(Comparator.comparingInt(x->x[4]));var o=new ArrayList<Integer>();for(var x:v)o.add(x[0]);return o;}}\n''','''import java.util.*;public final class SolutionTest{public static void main(String[]z){var first=new int[]{9,1,10,0,1};var in=new ArrayList<int[]>(List.of(first,new int[]{4,1,2,0,5},new int[]{3,1,2,0,1},new int[]{2,1,2,0,1}));assert Solution.orderChanges(in).equals(List.of(2,3,4,9))&&in.get(0)==first;assert Solution.orderChanges(List.of(new int[]{1,1,0,0,0},new int[]{1,2,0,0,0}))==null;assert Solution.orderChanges(List.of(new int[]{1,-1,0,0,0}))==null;}}\n''',"orders-by-sequence-only-and-mutates"),
},
"javascript": {
"configuration-patch": s("exports.patchConfig=(b,p)=>{const m={...b};if(Object.hasOwn(m,''))return null;for(const x of p){if(!Array.isArray(x)||x.length!==3||x[1]==='')return null;if(x[0]==='set')m[x[1]]=x[2];else if(x[0]==='unset')delete m[x[1]];else return null}return Object.keys(m).sort().map(k=>k+'='+m[k])}\n","exports.patchConfig=(b,p)=>{const m={...b};for(const x of p)if(x[0]==='set')m[x[1]]=x[2];return Object.keys(m).sort().map(k=>k+'='+m[k])}\n","const{patchConfig:f}=require('./solution');const b={mode:'safe',zone:'in'};if(JSON.stringify(f(b,[['unset','zone','x'],['set','mode','fast'],['set','new','']]))!=='[\"mode=fast\",\"new=\"]'||b.mode!=='safe'||f(b,[['merge','x','y']])!==null||f(b,[['set','','y']])!==null)throw Error('patch');\n","ignores-unset-and-validation"),
"ledger-reconciliation": s("exports.reconcileLedger=(o,e)=>{const seen=new Set;let b=o;for(const x of e){if(x.length!==3||seen.has(x[0])||x[2]<=0||(x[1]!==1&&x[1]!==-1)||!x.every(Number.isSafeInteger))return null;seen.add(x[0]);b+=x[1]*x[2]}return Number.isSafeInteger(b)?b:null}\n","exports.reconcileLedger=(o,e)=>e.reduce((b,x)=>b+x[1]*x[2],o)\n","const{reconcileLedger:f}=require('./solution');if(f(100,[[7,1,25],[8,-1,40]])!==85||f(0,[[7,1,2],[7,-1,1]])!==null||f(0,[[1,0,4]])!==null||f(0,[[1,1,0]])!==null||f(-2,[])!==-2)throw Error('ledger');\n","accepts-duplicate-and-invalid-entries"),
"permission-inheritance": s("exports.resolvePermissions=(role,parents,grants)=>{const seen=new Set,out=new Set;while(role!==''){if(!(role in parents)&&!(role in grants)||seen.has(role))return null;seen.add(role);for(const p of grants[role]||[])out.add(p);role=parents[role]||''}return[...out].sort()}\n","exports.resolvePermissions=(r,p,g)=>(g[r]||[]).slice().sort()\n","const{resolvePermissions:f}=require('./solution');const p={editor:'viewer',viewer:''},g={editor:['write','read'],viewer:['read','view']};if(JSON.stringify(f('editor',p,g))!=='[\"read\",\"view\",\"write\"]'||f('missing',p,g)!==null||f('a',{a:'b',b:'a'},{a:[],b:[]})!==null)throw Error('perms');\n","returns-direct-grants-only"),
"bounded-window-summary": s("exports.windowSummary=(e,start,end,limit)=>{if(![start,end,limit].every(Number.isSafeInteger)||start>end||limit<0)return null;const a=e.map((x,i)=>[x[0],x[1],i]).filter(x=>x[0]>=start&&x[0]<end).sort((x,y)=>x[0]-y[0]||x[2]-y[2]).slice(-limit||e.length+1);if(limit===0)return[0,0];return[a.length,a.reduce((s,x)=>s+x[1],0)]}\n","exports.windowSummary=(e,s,n,l)=>{const a=e.filter(x=>x[0]>=s&&x[0]<=n).slice(0,l);return[a.length,a.reduce((q,x)=>q+x[1],0)]}\n","const{windowSummary:f}=require('./solution');if(JSON.stringify(f([[8,5],[3,2],[8,7],[10,99],[6,4]],3,10,3))!=='[3,16]'||JSON.stringify(f([[3,9]],3,3,2))!=='[0,0]'||JSON.stringify(f([[4,9]],0,5,0))!=='[0,0]'||f([],5,4,1)!==null)throw Error('window');\n","uses-inclusive-end-and-first-events"),
"version-change-order": s("exports.orderChanges=v=>{const a=v.map(x=>x.slice()),seen=new Set;for(const x of a){if(x.length!==5||seen.has(x[0])||x.some(y=>!Number.isSafeInteger(y))||x.slice(1).some(y=>y<0))return null;seen.add(x[0])}a.sort((x,y)=>x[1]-y[1]||x[2]-y[2]||x[3]-y[3]||x[4]-y[4]||x[0]-y[0]);return a.map(x=>x[0])}\n","exports.orderChanges=v=>v.sort((a,b)=>a[4]-b[4]).map(x=>x[0])\n","const{orderChanges:f}=require('./solution');const v=[[9,1,10,0,1],[4,1,2,0,5],[3,1,2,0,1],[2,1,2,0,1]],copy=JSON.stringify(v);if(JSON.stringify(f(v))!=='[2,3,4,9]'||JSON.stringify(v)!==copy||f([[1,1,0,0,0],[1,2,0,0,0]])!==null||f([[1,-1,0,0,0]])!==null)throw Error('order');\n","orders-by-sequence-only-and-mutates"),
},
"typescript": {}, "python": {}, "rust": {},
}

LANG["typescript"] = {
"configuration-patch":s("export function patchConfig(b:Record<string,string>,p:Array<[string,string,string]>):string[]|null{const m={...b};if(Object.hasOwn(m,''))return null;for(const x of p){if(x[1]==='')return null;if(x[0]==='set')m[x[1]]=x[2];else if(x[0]==='unset')delete m[x[1]];else return null}return Object.keys(m).sort().map(k=>k+'='+m[k])}\n","export function patchConfig(b:Record<string,string>,p:Array<[string,string,string]>):string[]|null{const m={...b};for(const x of p)if(x[0]==='set')m[x[1]]=x[2];return Object.keys(m).sort().map(k=>k+'='+m[k])}\n","import{patchConfig as f}from'./solution';const b={mode:'safe',zone:'in'};if(JSON.stringify(f(b,[['unset','zone','x'],['set','mode','fast'],['set','new','']]))!=='[\"mode=fast\",\"new=\"]'||b.mode!=='safe'||f(b,[['merge','x','y']])!==null||f(b,[['set','','y']])!==null)throw Error('patch');\n","ignores-unset-and-validation"),
"ledger-reconciliation":s("export function reconcileLedger(o:number,e:Array<[number,number,number]>):number|null{const seen=new Set<number>();let b=o;for(const x of e){if(seen.has(x[0])||x[2]<=0||(x[1]!==1&&x[1]!==-1)||!x.every(Number.isSafeInteger))return null;seen.add(x[0]);b+=x[1]*x[2]}return Number.isSafeInteger(b)?b:null}\n","export function reconcileLedger(o:number,e:Array<[number,number,number]>):number|null{return e.reduce((b,x)=>b+x[1]*x[2],o)}\n","import{reconcileLedger as f}from'./solution';if(f(100,[[7,1,25],[8,-1,40]])!==85||f(0,[[7,1,2],[7,-1,1]])!==null||f(0,[[1,0,4]])!==null||f(0,[[1,1,0]])!==null||f(-2,[])!==-2)throw Error('ledger');\n","accepts-duplicate-and-invalid-entries"),
"permission-inheritance":s("export function resolvePermissions(role:string,parents:Record<string,string>,grants:Record<string,string[]>):string[]|null{const seen=new Set<string>(),out=new Set<string>();while(role!==''){if(!(role in parents)&&!(role in grants)||seen.has(role))return null;seen.add(role);for(const p of grants[role]??[])out.add(p);role=parents[role]??''}return[...out].sort()}\n","export function resolvePermissions(r:string,p:Record<string,string>,g:Record<string,string[]>):string[]|null{return(g[r]??[]).slice().sort()}\n","import{resolvePermissions as f}from'./solution';const p={editor:'viewer',viewer:''},g={editor:['write','read'],viewer:['read','view']};if(JSON.stringify(f('editor',p,g))!=='[\"read\",\"view\",\"write\"]'||f('missing',p,g)!==null||f('a',{a:'b',b:'a'},{a:[],b:[]})!==null)throw Error('perms');\n","returns-direct-grants-only"),
"bounded-window-summary":s("export function windowSummary(e:Array<[number,number]>,start:number,end:number,limit:number):[number,number]|null{if(![start,end,limit].every(Number.isSafeInteger)||start>end||limit<0)return null;if(limit===0)return[0,0];const a=e.map((x,i)=>[x[0],x[1],i]as[number,number,number]).filter(x=>x[0]>=start&&x[0]<end).sort((x,y)=>x[0]-y[0]||x[2]-y[2]).slice(-limit);return[a.length,a.reduce((s,x)=>s+x[1],0)]}\n","export function windowSummary(e:Array<[number,number]>,s:number,n:number,l:number):[number,number]|null{const a=e.filter(x=>x[0]>=s&&x[0]<=n).slice(0,l);return[a.length,a.reduce((q,x)=>q+x[1],0)]}\n","import{windowSummary as f}from'./solution';if(JSON.stringify(f([[8,5],[3,2],[8,7],[10,99],[6,4]],3,10,3))!=='[3,16]'||JSON.stringify(f([[3,9]],3,3,2))!=='[0,0]'||JSON.stringify(f([[4,9]],0,5,0))!=='[0,0]'||f([],5,4,1)!==null)throw Error('window');\n","uses-inclusive-end-and-first-events"),
"version-change-order":s("export function orderChanges(v:Array<[number,number,number,number,number]>):number[]|null{const a=v.map(x=>[...x]as[number,number,number,number,number]),seen=new Set<number>();for(const x of a){if(seen.has(x[0])||x.some(y=>!Number.isSafeInteger(y))||x.slice(1).some(y=>y<0))return null;seen.add(x[0])}a.sort((x,y)=>x[1]-y[1]||x[2]-y[2]||x[3]-y[3]||x[4]-y[4]||x[0]-y[0]);return a.map(x=>x[0])}\n","export function orderChanges(v:Array<[number,number,number,number,number]>):number[]|null{return v.sort((a,b)=>a[4]-b[4]).map(x=>x[0])}\n","import{orderChanges as f}from'./solution';const v:Array<[number,number,number,number,number]>=[[9,1,10,0,1],[4,1,2,0,5],[3,1,2,0,1],[2,1,2,0,1]],copy=JSON.stringify(v);if(JSON.stringify(f(v))!=='[2,3,4,9]'||JSON.stringify(v)!==copy||f([[1,1,0,0,0],[1,2,0,0,0]])!==null||f([[1,-1,0,0,0]])!==null)throw Error('order');\n","orders-by-sequence-only-and-mutates"),
}

LANG["python"] = {
"configuration-patch":s("def patch_config(base: dict[str,str], patches: list[tuple[str,str,str]]) -> list[str] | None:\n    m=base.copy()\n    if '' in m: return None\n    for op,key,value in patches:\n        if not key: return None\n        if op=='set': m[key]=value\n        elif op=='unset': m.pop(key,None)\n        else: return None\n    return [f'{k}={m[k]}' for k in sorted(m)]\n","def patch_config(base,patches):\n m=base.copy()\n for op,k,v in patches:\n  if op=='set':m[k]=v\n return [f'{k}={m[k]}' for k in sorted(m)]\n","from solution import patch_config as f\nb={'mode':'safe','zone':'in'}\nassert f(b,[('unset','zone','x'),('set','mode','fast'),('set','new','')])==['mode=fast','new='] and b['mode']=='safe'\nassert f(b,[('merge','x','y')]) is None and f(b,[('set','','y')]) is None\n","ignores-unset-and-validation"),
"ledger-reconciliation":s("def reconcile_ledger(opening: int, entries: list[tuple[int,int,int]]) -> int | None:\n    seen=set(); balance=opening\n    for ident,kind,amount in entries:\n        if ident in seen or amount<=0 or kind not in (-1,1): return None\n        seen.add(ident); balance += kind*amount\n    return balance\n","def reconcile_ledger(opening,entries):\n return opening+sum(kind*amount for _,kind,amount in entries)\n","from solution import reconcile_ledger as f\nassert f(100,[(7,1,25),(8,-1,40)])==85 and f(0,[(7,1,2),(7,-1,1)]) is None\nassert f(0,[(1,0,4)]) is None and f(0,[(1,1,0)]) is None and f(-2,[])==-2\n","accepts-duplicate-and-invalid-entries"),
"permission-inheritance":s("def resolve_permissions(role: str, parents: dict[str,str], grants: dict[str,list[str]]) -> list[str] | None:\n    seen=set(); out=set()\n    while role:\n        if role not in parents and role not in grants or role in seen: return None\n        seen.add(role); out.update(grants.get(role,[])); role=parents.get(role,'')\n    return sorted(out)\n","def resolve_permissions(role,parents,grants):\n return sorted(grants.get(role,[]))\n","from solution import resolve_permissions as f\np={'editor':'viewer','viewer':''};g={'editor':['write','read'],'viewer':['read','view']}\nassert f('editor',p,g)==['read','view','write'] and f('missing',p,g) is None\nassert f('a',{'a':'b','b':'a'},{'a':[],'b':[]}) is None\n","returns-direct-grants-only"),
"bounded-window-summary":s("def window_summary(events: list[tuple[int,int]], start: int, end: int, limit: int) -> tuple[int,int] | None:\n    if start>end or limit<0: return None\n    a=sorted(((t,v,i) for i,(t,v) in enumerate(events) if start<=t<end),key=lambda x:(x[0],x[2]))\n    a=a[-limit:] if limit else []\n    return len(a),sum(x[1] for x in a)\n","def window_summary(events,start,end,limit):\n a=[x for x in events if start<=x[0]<=end][:limit]\n return len(a),sum(x[1] for x in a)\n","from solution import window_summary as f\nassert f([(8,5),(3,2),(8,7),(10,99),(6,4)],3,10,3)==(3,16)\nassert f([(3,9)],3,3,2)==(0,0) and f([(4,9)],0,5,0)==(0,0) and f([],5,4,1) is None\n","uses-inclusive-end-and-first-events"),
"version-change-order":s("def order_changes(changes: list[tuple[int,int,int,int,int]]) -> list[int] | None:\n    seen=set()\n    for c in changes:\n        if c[0] in seen or any(x<0 for x in c[1:]): return None\n        seen.add(c[0])\n    return [c[0] for c in sorted(changes,key=lambda c:(c[1],c[2],c[3],c[4],c[0]))]\n","def order_changes(changes):\n changes.sort(key=lambda c:c[4]);return [c[0] for c in changes]\n","from solution import order_changes as f\nv=[(9,1,10,0,1),(4,1,2,0,5),(3,1,2,0,1),(2,1,2,0,1)];copy=v.copy()\nassert f(v)==[2,3,4,9] and v==copy\nassert f([(1,1,0,0,0),(1,2,0,0,0)]) is None and f([(1,-1,0,0,0)]) is None\n","orders-by-sequence-only-and-mutates"),
}

LANG["rust"] = {
"configuration-patch":s(r'''use std::collections::BTreeMap;
pub fn patch_config(base:&[(&str,&str)],patches:&[(&str,&str,&str)])->Option<Vec<String>>{let mut m=BTreeMap::new();for &(k,v) in base{if k.is_empty(){return None}m.insert(k,v);}for &(op,k,v) in patches{if k.is_empty(){return None}match op{"set"=>{m.insert(k,v);},"unset"=>{m.remove(k);},_=>return None}}Some(m.into_iter().map(|(k,v)|format!("{k}={v}")).collect())}
''', r'''use std::collections::BTreeMap;
pub fn patch_config(base:&[(&str,&str)],patches:&[(&str,&str,&str)])->Option<Vec<String>>{let mut m:BTreeMap<_,_>=base.iter().copied().collect();for &(op,k,v) in patches{if op=="set"{m.insert(k,v);}}Some(m.into_iter().map(|(k,v)|format!("{k}={v}")).collect())}
''', r'''mod solution;use solution::patch_config as f;#[test]fn check(){let b=[("mode","safe"),("zone","in")];assert_eq!(f(&b,&[("unset","zone","x"),("set","mode","fast"),("set","new","")]),Some(vec!["mode=fast".into(),"new=".into()]));assert_eq!(b[0],("mode","safe"));assert_eq!(f(&b,&[("merge","x","y")]),None);assert_eq!(f(&b,&[("set","","y")]),None);}
''',"ignores-unset-and-validation"),
"ledger-reconciliation":s(r'''use std::collections::HashSet;
pub fn reconcile_ledger(opening:i64,entries:&[(i64,i64,i64)])->Option<i64>{let mut seen=HashSet::new();let mut b=opening;for &(id,kind,amount) in entries{if !seen.insert(id)||amount<=0||(kind!=1&&kind != -1){return None}b=b.checked_add(kind.checked_mul(amount)?)?;}Some(b)}
''', r'''pub fn reconcile_ledger(opening:i64,entries:&[(i64,i64,i64)])->Option<i64>{Some(entries.iter().fold(opening,|b,x|b+x.1*x.2))}
''', r'''mod solution;use solution::reconcile_ledger as f;#[test]fn check(){assert_eq!(f(100,&[(7,1,25),(8,-1,40)]),Some(85));assert_eq!(f(0,&[(7,1,2),(7,-1,1)]),None);assert_eq!(f(0,&[(1,0,4)]),None);assert_eq!(f(0,&[(1,1,0)]),None);assert_eq!(f(-2,&[]),Some(-2));}
''',"accepts-duplicate-and-invalid-entries"),
"permission-inheritance":s(r'''use std::collections::{BTreeSet,HashMap,HashSet};
pub fn resolve_permissions(role:&str,parents:&[(&str,&str)],grants:&[(&str,&[&str])])->Option<Vec<String>>{let p:HashMap<_,_>=parents.iter().copied().collect();let g:HashMap<_,_>=grants.iter().copied().collect();let mut r=role;let mut seen=HashSet::new();let mut out=BTreeSet::new();while !r.is_empty(){if (!p.contains_key(r)&&!g.contains_key(r))||!seen.insert(r){return None}for &x in g.get(r).copied().unwrap_or(&[]){out.insert(x.to_string());}r=p.get(r).copied().unwrap_or("");}Some(out.into_iter().collect())}
''', r'''pub fn resolve_permissions(role:&str,_parents:&[(&str,&str)],grants:&[(&str,&[&str])])->Option<Vec<String>>{let mut o=grants.iter().find(|x|x.0==role).map(|x|x.1.iter().map(|s|s.to_string()).collect::<Vec<_>>()).unwrap_or_default();o.sort();Some(o)}
''', r'''mod solution;use solution::resolve_permissions as f;#[test]fn check(){let p=[("editor","viewer"),("viewer","")];let e=["write","read"];let v=["read","view"];let g=[("editor",e.as_slice()),("viewer",v.as_slice())];assert_eq!(f("editor",&p,&g),Some(vec!["read".into(),"view".into(),"write".into()]));assert_eq!(f("missing",&p,&g),None);let q=[("a","b"),("b","a")];let empty:[&str;0]=[];let z=[("a",empty.as_slice()),("b",empty.as_slice())];assert_eq!(f("a",&q,&z),None);}
''',"returns-direct-grants-only"),
"bounded-window-summary":s(r'''pub fn window_summary(events:&[(i64,i64)],start:i64,end:i64,limit:i32)->Option<(usize,i64)>{if start>end||limit<0{return None}let mut a:Vec<_>=events.iter().enumerate().filter(|(_,x)|x.0>=start&&x.0<end).map(|(i,x)|(x.0,x.1,i)).collect();a.sort_by_key(|x|(x.0,x.2));let keep=limit as usize;if a.len()>keep{a.drain(..a.len()-keep);}Some((a.len(),a.iter().map(|x|x.1).sum()))}
''', r'''pub fn window_summary(events:&[(i64,i64)],start:i64,end:i64,limit:i32)->Option<(usize,i64)>{let a:Vec<_>=events.iter().filter(|x|x.0>=start&&x.0<=end).take(limit as usize).collect();Some((a.len(),a.iter().map(|x|x.1).sum()))}
''', r'''mod solution;use solution::window_summary as f;#[test]fn check(){assert_eq!(f(&[(8,5),(3,2),(8,7),(10,99),(6,4)],3,10,3),Some((3,16)));assert_eq!(f(&[(3,9)],3,3,2),Some((0,0)));assert_eq!(f(&[(4,9)],0,5,0),Some((0,0)));assert_eq!(f(&[],5,4,1),None);}
''',"uses-inclusive-end-and-first-events"),
"version-change-order":s(r'''use std::collections::HashSet;
pub fn order_changes(changes:&[(i32,i32,i32,i32,i32)])->Option<Vec<i32>>{let mut seen=HashSet::new();for c in changes{if !seen.insert(c.0)||c.1<0||c.2<0||c.3<0||c.4<0{return None}}let mut a=changes.to_vec();a.sort_by_key(|c|(c.1,c.2,c.3,c.4,c.0));Some(a.iter().map(|c|c.0).collect())}
''', r'''pub fn order_changes(changes:&[(i32,i32,i32,i32,i32)])->Option<Vec<i32>>{let mut a=changes.to_vec();a.sort_by_key(|c|c.4);Some(a.iter().map(|c|c.0).collect())}
''', r'''mod solution;use solution::order_changes as f;#[test]fn check(){let v=[(9,1,10,0,1),(4,1,2,0,5),(3,1,2,0,1),(2,1,2,0,1)];assert_eq!(f(&v),Some(vec![2,3,4,9]));assert_eq!(v[0].0,9);assert_eq!(f(&[(1,1,0,0,0),(1,2,0,0,0)]),None);assert_eq!(f(&[(1,-1,0,0,0)]),None);}
''',"orders-by-sequence-only"),
}

FILE_CONTRACT={"go":"Return solution.go in package solution.","java":"Return Solution.java defining public final class Solution.","javascript":"Return CommonJS module solution.js.","typescript":"Return strict TypeScript module solution.ts.","python":"Return solution.py with the function at module scope.","rust":"Return solution.rs with the public function at module scope."}
API={
"go":{"configuration-patch":"func PatchConfig(base map[string]string, patches [][3]string) ([]string, bool)","ledger-reconciliation":"func ReconcileLedger(opening int64, entries [][3]int64) (int64, bool)","permission-inheritance":"func ResolvePermissions(role string, parents map[string]string, grants map[string][]string) ([]string, bool)","bounded-window-summary":"func WindowSummary(events [][2]int64, start, end int64, limit int) ([2]int64, bool)","version-change-order":"func OrderChanges(changes [][5]int) ([]int, bool)"},
"java":{"configuration-patch":"public static List<String> patchConfig(Map<String,String> base, List<String[]> patches)","ledger-reconciliation":"public static Long reconcileLedger(long opening, List<long[]> entries)","permission-inheritance":"public static List<String> resolvePermissions(String role, Map<String,String> parents, Map<String,List<String>> grants)","bounded-window-summary":"public static long[] windowSummary(List<long[]> events, long start, long end, int limit)","version-change-order":"public static List<Integer> orderChanges(List<int[]> changes)"},
"javascript":{"configuration-patch":"exports.patchConfig = function(base, patches)","ledger-reconciliation":"exports.reconcileLedger = function(opening, entries)","permission-inheritance":"exports.resolvePermissions = function(role, parents, grants)","bounded-window-summary":"exports.windowSummary = function(events, start, end, limit)","version-change-order":"exports.orderChanges = function(changes)"},
"typescript":{"configuration-patch":"export function patchConfig(base: Record<string,string>, patches: Array<[string,string,string]>): string[] | null","ledger-reconciliation":"export function reconcileLedger(opening: number, entries: Array<[number,number,number]>): number | null","permission-inheritance":"export function resolvePermissions(role: string, parents: Record<string,string>, grants: Record<string,string[]>): string[] | null","bounded-window-summary":"export function windowSummary(events: Array<[number,number]>, start: number, end: number, limit: number): [number,number] | null","version-change-order":"export function orderChanges(changes: Array<[number,number,number,number,number]>): number[] | null"},
"python":{"configuration-patch":"def patch_config(base: dict[str,str], patches: list[tuple[str,str,str]]) -> list[str] | None","ledger-reconciliation":"def reconcile_ledger(opening: int, entries: list[tuple[int,int,int]]) -> int | None","permission-inheritance":"def resolve_permissions(role: str, parents: dict[str,str], grants: dict[str,list[str]]) -> list[str] | None","bounded-window-summary":"def window_summary(events: list[tuple[int,int]], start: int, end: int, limit: int) -> tuple[int,int] | None","version-change-order":"def order_changes(changes: list[tuple[int,int,int,int,int]]) -> list[int] | None"},
"rust":{"configuration-patch":"pub fn patch_config(base: &[(&str,&str)], patches: &[(&str,&str,&str)]) -> Option<Vec<String>>","ledger-reconciliation":"pub fn reconcile_ledger(opening: i64, entries: &[(i64,i64,i64)]) -> Option<i64>","permission-inheritance":"pub fn resolve_permissions(role: &str, parents: &[(&str,&str)], grants: &[(&str,&[&str])]) -> Option<Vec<String>>","bounded-window-summary":"pub fn window_summary(events: &[(i64,i64)], start: i64, end: i64, limit: i32) -> Option<(usize,i64)>","version-change-order":"pub fn order_changes(changes: &[(i32,i32,i32,i32,i32)]) -> Option<Vec<i32>>"},
}
BEHAVIOR={
"configuration-patch":"Copy the base configuration, then apply patches in order. Each patch is (operation,key,value): set overwrites, unset removes even when absent and ignores value. Reject an empty key or unknown operation. Return sorted key=value strings without mutating base.",
"ledger-reconciliation":"Each entry is (unique id, kind, positive amount), where kind 1 credits and -1 debits. Reject duplicate ids, other kinds, non-positive amounts, and unsafe arithmetic where applicable; otherwise return opening plus all signed amounts.",
"permission-inheritance":"Collect the named role's grants and every parent role's grants, deduplicate, and sort. Reject an unknown role, unknown parent reached in the chain, or inheritance cycle. Empty parent marks the root.",
"bounded-window-summary":"Reject start greater than end or a negative limit. Select events with timestamps in [start,end), order by timestamp with original order breaking ties, keep only the latest limit, and return (kept count,value sum). Limit zero returns zeros.",
"version-change-order":"Each change is (id,major,minor,patch,sequence). Reject duplicate ids or negative version/sequence fields. Without mutating input, return ids ordered by numeric major, minor, patch, sequence, then id.",
}
EXAMPLE={
"configuration-patch":"base {mode=safe, zone=in} patched by unset zone then set mode=fast returns [mode=fast].",
"ledger-reconciliation":"opening 100 with (7,credit,25) and (8,debit,40) reconciles to 85; repeating id 7 is rejected.",
"permission-inheritance":"editor granting write and inheriting viewer granting read resolves to [read,write].",
"bounded-window-summary":"events (8,5),(3,2),(8,7),(10,99),(6,4), window [3,10), limit 3 returns (3,16).",
"version-change-order":"changes ids 9 at 1.10.0/1 and 4 at 1.2.0/5 order as [4,9], using numeric versions.",
}


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def make_task(language: str, slug: str, kind: str) -> dict[str, Any]:
    item=LANG[language][slug]
    lead="Implement the following API." if kind=="generation" else "Repair the buggy source below without changing the required API."
    prompt=f"{lead}\n\nFile contract: {FILE_CONTRACT[language]}\nRequired API: {API[language][slug]}\nBehavior: {BEHAVIOR[slug]}\nVisible example: {EXAMPLE[slug]}\n"
    if kind=="repair": prompt+=f"\nBuggy source to repair:\n\n{item['bad']}"
    prompt+="\nReturn only the complete source file; do not include Markdown fences or prose."
    files=[]
    if language=="go":
        module="module private.invalid/ganesh/development/tranche6\n\ngo 1.22\n"
        files.append({"path":"go.mod","role":"support","content":module,"sha256":sha256_text(module)})
        test_path="solution_test.go"
    else:
        test_path={"java":"SolutionTest.java","javascript":"solution.test.js","typescript":"solution.test.ts","python":"test_solution.py","rust":"solution_test.rs"}[language]
    files.append({"path":test_path,"role":"test","content":item["test"],"sha256":sha256_text(item["test"])})
    task={"schema_version":"1.0","task_id":f"dev-t6-{language}-{slug}","surface":"development","language":language,"family":LANGUAGE_FAMILY[language],"task_type":kind,"prompt":{"text":prompt,"sha256":sha256_text(prompt)},"rendered_prompt":{"text":prompt,"sha256":sha256_text(prompt)},"candidate_path":CANDIDATE_PATH[language],"files":files,"runtime_id":RUNTIME[language],"limits":{"timeout_seconds":60 if language in {"go","java","rust"} else 30,"memory_mb":512,"cpus":1,"pids":64,"output_bytes":65536},"validation":{"reference":{"label":"author-reference","code":item["reference"],"sha256":sha256_text(item["reference"])},"known_bad":[{"label":item["bad_label"],"code":item["bad"],"sha256":sha256_text(item["bad"])}]}}
    return validate_task(task)


def comparison_fingerprints()->tuple[set[str],set[str],int,dict[str,int]]:
    exact:set[str]=set();norm:set[str]=set();counts={"seed":0,"private_development":0}
    for relative in ("data/seed/ganesh_v01/train.jsonl","data/seed/ganesh_v01/validation.jsonl"):
        for line in (ROOT/relative).read_text(encoding="utf-8").splitlines():
            text=json.loads(line)["messages"][0]["content"];exact.add(sha256_text(text));norm.add(sha256_text(normalized(text)));counts["seed"]+=1
    for path in sorted((ROOT/"eval/private/development").glob("tranche*/**/*.task.json")):
        if "tranche6" in path.parts: continue
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
    if exact_hits or norm_hits or own_exact or own_norm: raise RuntimeError("tranche6 prompt overlap detected")
    entries=[]
    for task in tasks:
        path=OUT/f"{task['task_id']}.task.json";write_json(path,task)
        entries.append({"task_id":task["task_id"],"language":task["language"],"task_type":task["task_type"],"path":str(path.relative_to(ROOT)),"sha256":sha256_object(task),"prompt_sha256":task["prompt"]["sha256"],"rendered_prompt_sha256":task["rendered_prompt"]["sha256"]})
    counter=Counter((t["language"],t["task_type"]) for t in tasks)
    manifest={"schema_version":"ganesh-mini-private-eval-manifest/v1","surface":"development","tranche":"tranche6","status":"authored","task_count":len(tasks),"counts_by_lane":{l:{k:counter[(l,k)] for k in ("generation","repair")}for l in RUNTIME},"runtime_config":"configs/eval/runtimes.json","tasks":entries};manifest["manifest_sha256"]=sha256_object(manifest)
    overlap={"schema_version":"ganesh-mini-evaluation-overlap/v1","evaluation_manifest":str(MANIFEST.relative_to(ROOT)),"evaluation_manifest_sha256":manifest["manifest_sha256"],"seed_manifest":"manifests/datasets/ganesh_v01_seed.json","seed_records_inspected":counts_seen["seed"],"other_private_development_prompts_inspected":counts_seen["private_development"],"comparison_prompts_inspected":total,"evaluation_prompts_inspected":len(tasks),"normalization":"NFKC + Unicode casefold + whitespace collapse","exact_prompt_overlaps":exact_hits,"normalized_prompt_overlaps":norm_hits,"within_tranche_exact_overlaps":own_exact,"within_tranche_normalized_overlaps":own_norm,"status":"passed"};overlap["report_sha256"]=sha256_object(overlap)
    write_json(MANIFEST,manifest);write_json(OVERLAP,overlap);return manifest,overlap


if __name__=="__main__":
    manifest,overlap=build();print(json.dumps({"tasks":manifest["task_count"],"manifest_sha256":manifest["manifest_sha256"],"overlap_sha256":overlap["report_sha256"]},sort_keys=True))
