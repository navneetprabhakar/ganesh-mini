#!/usr/bin/env python3
"""Author and seal the final private decision tranche (tranche 6)."""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

from scripts.eval.contracts import CANDIDATE_PATH, LANGUAGE_FAMILY, load_json, sha256_object, sha256_text, validate_task, write_json

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "eval/private/decision/tranche6"
MANIFEST = ROOT / "manifests/evaluation/private/decision-tranche6.json"
OVERLAP = ROOT / "manifests/evaluation/private/decision-tranche6-overlap.json"
SEED_PATHS = ("data/seed/ganesh_v01/train.jsonl", "data/seed/ganesh_v01/validation.jsonl")
DEVELOPMENT_MANIFESTS = tuple(f"manifests/evaluation/private/development-tranche{i}.json" for i in range(1, 7))
PRIOR_DECISION_MANIFESTS = tuple(f"manifests/evaluation/private/decision-tranche{i}.json" for i in range(1, 6))
EXPECTED_TRANCHE5_SHA256 = "ee52d232e2d44411a398ad680def61ffffd54722d8a8fc400ffdd2143d4240e3"
EXPECTED_TRANCHE5_OVERLAP_SHA256 = "251cee5751463ffa76159823b3ec939a6edbd66e328336ca65e7169022186de5"
RUNTIME = {
    "go": "go-1.22.12", "java": "java-21.0.11", "javascript": "javascript-node-22.23.2",
    "typescript": "typescript-5.5.4-node-22", "python": "python-3.11.15", "rust": "rust-1.85.0",
}
SLUGS = (
    "bounded-step-deltas", "prefix-peaks", "suffix-troughs", "rotate-right-count",
    "stable-frequencies", "clamp-band", "neighbor-products", "parity-buckets",
    "alternating-prefixes", "longest-run",
)
KINDS = ("generation",) * 5 + ("repair",) * 5
NAMES = {slug: slug.replace("-", "_") for slug in SLUGS}
BEHAVIOR = {
    "bounded-step-deltas": "Parse a non-empty comma-separated list of canonical signed integers in -1000..1000. Return each next-minus-current difference, clamped to -1000..1000, joined by commas; a singleton returns the empty string.",
    "prefix-peaks": "Parse a non-empty comma-separated list of canonical signed integers in -1000..1000. Return the running maximum after every input position, joined by commas.",
    "suffix-troughs": "Parse a non-empty comma-separated list of canonical signed integers in -1000..1000. Return the minimum from each position through the end, joined by commas.",
    "rotate-right-count": "Parse canonical k;values, where k is an integer in 0..1000 and values is a non-empty comma-separated integer list in -1000..1000. Rotate right by k modulo the list length and return comma-separated values.",
    "stable-frequencies": "Parse a non-empty comma-separated list of canonical signed integers in -1000..1000. For each distinct value in first-occurrence order, return value:count, joined by commas.",
    "clamp-band": "Parse canonical lo;hi;values, where lo and hi are integers in -1000..1000, lo is at most hi, and values is a non-empty comma-separated integer list in that range. Clamp each value into [lo,hi] and return comma-separated values.",
    "neighbor-products": "Parse a non-empty comma-separated list of canonical signed integers in -1000..1000. Return products of adjacent pairs joined by commas; a singleton returns the empty string.",
    "parity-buckets": "Parse a non-empty comma-separated list of canonical signed integers in -1000..1000. Return all even values in original order followed by all odd values in original order, joined by commas. Negative odd values are odd.",
    "alternating-prefixes": "Parse a non-empty comma-separated list of canonical signed integers in -1000..1000. Starting with plus at index zero, alternately add and subtract values and return every running result joined by commas.",
    "longest-run": "Parse a non-empty comma-separated list of canonical signed integers in -1000..1000. Return value:length for the first longest contiguous run of equal values.",
}
EXAMPLE = {
    "bounded-step-deltas": "-1000,1000,-1000 returns 1000,-1000.", "prefix-peaks": "3,1,4,2 returns 3,3,4,4.",
    "suffix-troughs": "3,1,4,2 returns 1,1,2,2.", "rotate-right-count": "2;1,2,3,4 returns 3,4,1,2.",
    "stable-frequencies": "4,2,4,4,2 returns 4:3,2:2.", "clamp-band": "0;5;-2,3,9 returns 0,3,5.",
    "neighbor-products": "2,-3,4 returns -6,-12.", "parity-buckets": "3,2,-1,-4 returns 2,-4,3,-1.",
    "alternating-prefixes": "5,2,3,1 returns 5,3,6,5.", "longest-run": "2,2,1,1,1,2 returns 1:3.",
}
CASES = {
    "bounded-step-deltas": (("-1000,1000,-1000", "1000,-1000"), ("7", ""), ("4,1,9", "-3,8"), ("1, 2", None), ("1001", None)),
    "prefix-peaks": (("3,1,4,2", "3,3,4,4"), ("-3,-5,-1", "-3,-3,-1"), ("0", "0"), ("", None), ("01,2", None)),
    "suffix-troughs": (("3,1,4,2", "1,1,2,2"), (("-1,5,-3"), "-3,-3,-3"), ("7", "7"), ("1,,2", None), ("-0", None)),
    "rotate-right-count": (("2;1,2,3,4", "3,4,1,2"), ("0;-1,2", "-1,2"), ("5;7,8", "8,7"), ("-1;1,2", None), ("1;", None)),
    "stable-frequencies": (("4,2,4,4,2", "4:3,2:2"), ("-1,-1,0", "-1:2,0:1"), ("7", "7:1"), ("1.0", None), ("", None)),
    "clamp-band": (("0;5;-2,3,9", "0,3,5"), ("-2;-1;-3,0", "-2,-1"), ("4;4;1,5", "4,4"), ("5;2;3", None), ("0;1;", None)),
    "neighbor-products": (("2,-3,4", "-6,-12"), ("7", ""), ("-1000,1000", "-1000000"), ("1,+2", None), ("", None)),
    "parity-buckets": (("3,2,-1,-4", "2,-4,3,-1"), ("1,3", "1,3"), ("0,-2,5", "0,-2,5"), ("1,", None), ("1002", None)),
    "alternating-prefixes": (("5,2,3,1", "5,3,6,5"), ("-1,-2,-3", "-1,1,-2"), ("0", "0"), ("--1", None), ("", None)),
    "longest-run": (("2,2,1,1,1,2", "1:3"), ("4,4,3,3", "4:2"), ("-1", "-1:1"), ("01", None), ("1, 1", None)),
}


def camel(slug: str) -> str:
    first, *rest = slug.split("-")
    return first + "".join(word.title() for word in rest)


def parse_py() -> str:
    return "import re\ndef nums(s):\n if not s:return None\n o=[]\n for z in s.split(','):\n  if not re.fullmatch(r'0|-?[1-9][0-9]*',z):return None\n  x=int(z)\n  if x < -1000 or x > 1000:return None\n  o.append(x)\n return o\ndef join(a):return ','.join(map(str,a))\n"


def python_reference(slug: str) -> str:
    name = NAMES[slug]
    setup = " a=nums(s)\n if a is None:return None\n"
    if slug == "rotate-right-count": setup = " q=s.split(';')\n if len(q)!=2:return None\n k=nums(q[0]);a=nums(q[1])\n if k is None or a is None or len(k)!=1 or k[0]<0:return None\n k=k[0]%len(a)\n"
    if slug == "clamp-band": setup = " q=s.split(';')\n if len(q)!=3:return None\n lo=nums(q[0]);hi=nums(q[1]);a=nums(q[2])\n if lo is None or hi is None or a is None or len(lo)!=1 or len(hi)!=1 or lo[0]>hi[0]:return None\n lo,hi=lo[0],hi[0]\n"
    alg = {
        "bounded-step-deltas": "return join([max(-1000,min(1000,a[i]-a[i-1])) for i in range(1,len(a))])",
        "prefix-peaks": "o=[];m=a[0]\nfor x in a:m=max(m,x);o.append(m)\nreturn join(o)",
        "suffix-troughs": "o=[0]*len(a);m=a[-1]\nfor i in range(len(a)-1,-1,-1):m=min(m,a[i]);o[i]=m\nreturn join(o)",
        "rotate-right-count": "return join(a[-k:]+a[:-k] if k else a)",
        "stable-frequencies": "return ','.join(f'{x}:{a.count(x)}' for i,x in enumerate(a) if x not in a[:i])",
        "clamp-band": "return join([max(lo,min(hi,x)) for x in a])",
        "neighbor-products": "return join([a[i-1]*a[i] for i in range(1,len(a))])",
        "parity-buckets": "return join([x for x in a if x%2==0]+[x for x in a if x%2!=0])",
        "alternating-prefixes": "o=[];n=0\nfor i,x in enumerate(a):n+=x if i%2==0 else -x;o.append(n)\nreturn join(o)",
        "longest-run": "best=(a[0],1);cur=(a[0],1)\nfor x in a[1:]:\n cur=(x,cur[1]+1) if x==cur[0] else (x,1)\n if cur[1]>best[1]:best=cur\nreturn f'{best[0]}:{best[1]}'",
    }[slug]
    body = "\n".join(" " + line for line in alg.splitlines())
    return parse_py() + f"def {name}(s: str) -> str | None:\n{setup}{body}\n"


def js_reference(slug: str, ts: bool) -> str:
    name = camel(slug); mode = SLUGS.index(slug)
    if ts:
        parser = "const nums=(s:string):number[]|null=>{if(!s)return null;let o:number[]=[];for(const z of s.split(',')){if(!/^(?:0|-?[1-9][0-9]*)$/.test(z))return null;let x=Number(z);if(x< -1000||x>1000)return null;o.push(x)}return o};"
        head = f"export function {name}(s:string):string|null{{let m={mode},a:number[]=[];let k=0,lo=0,hi=0;if(m===3){{const q=s.split(';'),kp=nums(q[0]),ap=nums(q[1]);if(q.length!==2||kp===null||ap===null||kp.length!==1||kp[0]<0)return null;a=ap;k=kp[0]%a.length}}else if(m===5){{const q=s.split(';'),lp=nums(q[0]),hp=nums(q[1]),ap=nums(q[2]);if(q.length!==3||lp===null||hp===null||ap===null||lp.length!==1||hp.length!==1||lp[0]>hp[0])return null;a=ap;lo=lp[0];hi=hp[0]}}else{{const ap=nums(s);if(ap===null)return null;a=ap}}"
    else:
        parser = "const nums=s=>{if(!s)return null;let o=[];for(const z of s.split(',')){if(!/^(?:0|-?[1-9][0-9]*)$/.test(z))return null;let x=Number(z);if(x< -1000||x>1000)return null;o.push(x)}return o};"
        head = f"exports.{name}=function(s){{let m={mode},a=[],k=0,lo=0,hi=0;if(m===3){{const q=s.split(';'),kp=nums(q[0]),ap=nums(q[1]);if(q.length!==2||kp===null||ap===null||kp.length!==1||kp[0]<0)return null;a=ap;k=kp[0]%a.length}}else if(m===5){{const q=s.split(';'),lp=nums(q[0]),hp=nums(q[1]),ap=nums(q[2]);if(q.length!==3||lp===null||hp===null||ap===null||lp.length!==1||hp.length!==1||lp[0]>hp[0])return null;a=ap;lo=lp[0];hi=hp[0]}}else{{const ap=nums(s);if(ap===null)return null;a=ap}}"
    body = "if(m===0)return a.slice(1).map((x,i)=>Math.max(-1000,Math.min(1000,x-a[i]))).join(',');if(m===1){let z=-Infinity;return a.map(x=>z=Math.max(z,x)).join(',')}if(m===2){let o:number[]=[] as number[],z=Infinity;for(let i=a.length-1;i>=0;i--)o[i]=z=Math.min(z,a[i]);return o.join(',')}if(m===3)return(k?a.slice(-k).concat(a.slice(0,-k)):a).join(',');if(m===4)return a.filter((x,i)=>a.indexOf(x)===i).map(x=>x+':'+a.filter(y=>y===x).length).join(',');if(m===5)return a.map(x=>Math.max(lo,Math.min(hi,x))).join(',');if(m===6)return a.slice(1).map((x,i)=>x*a[i]).join(',');if(m===7)return a.filter(x=>x%2===0).concat(a.filter(x=>x%2!==0)).join(',');if(m===8){let n=0;return a.map((x,i)=>n+=i%2?-x:x).join(',')}let bv=a[0],bl=1,cv=a[0],cl=1;for(const x of a.slice(1)){if(x===cv)cl++;else{cv=x;cl=1}if(cl>bl){bv=cv;bl=cl}}return bv+':'+bl}\n"
    if not ts:
        body = body.replace("let o:number[]=[] as number[]", "let o=[]")
    return parser + head + body


def go_reference(slug: str) -> str:
    name = "".join(x.title() for x in slug.split("-")); mode = SLUGS.index(slug)
    return '''package solution
import("regexp";"strconv";"strings")
func nums(s string)([]int,bool){if s==""{return nil,false};o:=[]int{};r:=regexp.MustCompile(`^(0|-?[1-9][0-9]*)$`);for _,z:=range strings.Split(s,","){if !r.MatchString(z){return nil,false};x,e:=strconv.Atoi(z);if e!=nil||x< -1000||x>1000{return nil,false};o=append(o,x)};return o,true}
func join(a []int)string{o:=[]string{};for _,x:=range a{o=append(o,strconv.Itoa(x))};return strings.Join(o,",")}
func NAME(s string)(string,bool){m:=MODE;a:=[]int{};k,lo,hi:=0,0,0;if m==3{q:=strings.Split(s,";");if len(q)!=2{return "",false};x,o1:=nums(q[0]);var o2 bool;a,o2=nums(q[1]);if !o1||!o2||len(x)!=1||x[0]<0{return "",false};k=x[0]%len(a)}else if m==5{q:=strings.Split(s,";");if len(q)!=3{return "",false};x,o1:=nums(q[0]);y,o2:=nums(q[1]);var o3 bool;a,o3=nums(q[2]);if !o1||!o2||!o3||len(x)!=1||len(y)!=1||x[0]>y[0]{return "",false};lo,hi=x[0],y[0]}else{var ok bool;a,ok=nums(s);if !ok{return "",false}};o:=[]int{};if m==0{for i:=1;i<len(a);i++{d:=a[i]-a[i-1];if d< -1000{d= -1000};if d>1000{d=1000};o=append(o,d)}}else if m==1{z:=a[0];for _,x:=range a{if x>z{z=x};o=append(o,z)}}else if m==2{o=make([]int,len(a));z:=a[len(a)-1];for i:=len(a)-1;i>=0;i--{if a[i]<z{z=a[i]};o[i]=z}}else if m==3{o=append(o,a[len(a)-k:]...);o=append(o,a[:len(a)-k]...)}else if m==4{r:=map[int]int{};for _,x:=range a{r[x]++};seen:=map[int]bool{};z:=[]string{};for _,x:=range a{if !seen[x]{seen[x]=true;z=append(z,strconv.Itoa(x)+":"+strconv.Itoa(r[x]))}};return strings.Join(z,","),true}else if m==5{for _,x:=range a{if x<lo{x=lo};if x>hi{x=hi};o=append(o,x)}}else if m==6{for i:=1;i<len(a);i++{o=append(o,a[i-1]*a[i])}}else if m==7{for _,x:=range a{if x%2==0{o=append(o,x)}};for _,x:=range a{if x%2!=0{o=append(o,x)}}}else if m==8{n:=0;for i,x:=range a{if i%2==0{n+=x}else{n-=x};o=append(o,n)}}else{bv,bl,cv,cl:=a[0],1,a[0],1;for _,x:=range a[1:]{if x==cv{cl++}else{cv=x;cl=1};if cl>bl{bv,bl=cv,cl}};return strconv.Itoa(bv)+":"+strconv.Itoa(bl),true};return join(o),true}
'''.replace("NAME", name).replace("MODE", str(mode))


def java_reference(slug: str) -> str:
    name = camel(slug); mode = SLUGS.index(slug)
    # Keep the implementation self-contained so every task compiles independently.
    return '''import java.util.*;public final class Solution{static List<Integer>n(String s){if(s.isEmpty())return null;var o=new ArrayList<Integer>();for(var z:s.split(",",-1)){if(!z.matches("(?:0|-?[1-9][0-9]*)"))return null;try{int x=Integer.parseInt(z);if(x< -1000||x>1000)return null;o.add(x);}catch(Exception e){return null;}}return o;}static String j(List<?>a){return String.join(",",a.stream().map(Object::toString).toList());}public static String NAME(String s){int m=MODE,k=0,lo=0,hi=0;List<Integer>a;String[]q;if(m==3){q=s.split(";",-1);if(q.length!=2)return null;var x=n(q[0]);a=n(q[1]);if(x==null||a==null||x.size()!=1||x.get(0)<0)return null;k=x.get(0)%a.size();}else if(m==5){q=s.split(";",-1);if(q.length!=3)return null;var x=n(q[0]);var y=n(q[1]);a=n(q[2]);if(x==null||y==null||a==null||x.size()!=1||y.size()!=1||x.get(0)>y.get(0))return null;lo=x.get(0);hi=y.get(0);}else if((a=n(s))==null)return null;var o=new ArrayList<Integer>();if(m==0){for(int i=1;i<a.size();i++)o.add(Math.max(-1000,Math.min(1000,a.get(i)-a.get(i-1))));}else if(m==1){int z=a.get(0);for(int x:a){z=Math.max(z,x);o.add(z);}}else if(m==2){for(int x:a)o.add(0);int z=a.get(a.size()-1);for(int i=a.size()-1;i>=0;i--){z=Math.min(z,a.get(i));o.set(i,z);}}else if(m==3){o.addAll(a.subList(a.size()-k,a.size()));o.addAll(a.subList(0,a.size()-k));}else if(m==4){var c=new LinkedHashMap<Integer,Integer>();for(int x:a)c.put(x,c.getOrDefault(x,0)+1);return String.join(",",c.entrySet().stream().map(e->e.getKey()+":"+e.getValue()).toList());}else if(m==5){for(int x:a)o.add(Math.max(lo,Math.min(hi,x)));}else if(m==6){for(int i=1;i<a.size();i++)o.add(a.get(i-1)*a.get(i));}else if(m==7){for(int x:a)if(x%2==0)o.add(x);for(int x:a)if(x%2!=0)o.add(x);}else if(m==8){int z=0;for(int i=0;i<a.size();i++){z+=i%2==0?a.get(i):-a.get(i);o.add(z);}}else{int bv=a.get(0),bl=1,cv=bv,cl=1;for(int x:a.subList(1,a.size())){if(x==cv)cl++;else{cv=x;cl=1;}if(cl>bl){bv=cv;bl=cl;}}return bv+":"+bl;}return j(o);}}\n'''.replace("NAME", name).replace("MODE", str(mode))


def rust_reference(slug: str) -> str:
    name = NAMES[slug]; mode = SLUGS.index(slug)
    return '''fn nums(s:&str)->Option<Vec<i32>>{if s.is_empty(){return None}let mut o=vec![];for z in s.split(','){let x:i32=z.parse().ok()?;if x.to_string()!=z||x< -1000||x>1000{return None}o.push(x)}Some(o)}fn join(a:&[i32])->String{a.iter().map(|x|x.to_string()).collect::<Vec<_>>().join(",")}pub fn NAME(s:&str)->Option<String>{let m=MODE;let(mut a,mut k,mut lo,mut hi)=(vec![],0usize,0,0);if m==3{let q:Vec<_>=s.split(';').collect();if q.len()!=2{return None}let x=nums(q[0])?;a=nums(q[1])?;if x.len()!=1||x[0]<0{return None}k=x[0]as usize%a.len()}else if m==5{let q:Vec<_>=s.split(';').collect();if q.len()!=3{return None}let x=nums(q[0])?;let y=nums(q[1])?;a=nums(q[2])?;if x.len()!=1||y.len()!=1||x[0]>y[0]{return None}lo=x[0];hi=y[0]}else{a=nums(s)?}let mut o=vec![];if m==0{for i in 1..a.len(){o.push((a[i]-a[i-1]).clamp(-1000,1000))}}else if m==1{let mut z=a[0];for x in a{z=z.max(x);o.push(z)}}else if m==2{o=vec![0;a.len()];let mut z=a[a.len()-1];for i in(0..a.len()).rev(){z=z.min(a[i]);o[i]=z}}else if m==3{o.extend_from_slice(&a[a.len()-k..]);o.extend_from_slice(&a[..a.len()-k])}else if m==4{let mut seen=std::collections::HashSet::new();return Some(a.iter().filter(|x|seen.insert(**x)).map(|x|format!("{}:{}",x,a.iter().filter(|y|*y==x).count())).collect::<Vec<_>>().join(","))}else if m==5{o=a.into_iter().map(|x|x.clamp(lo,hi)).collect()}else if m==6{for i in 1..a.len(){o.push(a[i-1]*a[i])}}else if m==7{o.extend(a.iter().filter(|x|**x%2==0).copied());o.extend(a.iter().filter(|x|**x%2!=0).copied())}else if m==8{let mut z=0;for(i,x)in a.into_iter().enumerate(){if i%2==0{z+=x}else{z-=x}o.push(z)}}else{let(mut bv,mut bl,mut cv,mut cl)=(a[0],1,a[0],1);for x in a.into_iter().skip(1){if x==cv{cl+=1}else{cv=x;cl=1}if cl>bl{bv=cv;bl=cl}}return Some(format!("{}:{}",bv,bl))}Some(join(&o))}\n'''.replace("NAME", name).replace("MODE", str(mode))


def test_source(language: str, slug: str) -> str:
    name, cam = NAMES[slug], camel(slug); cases = CASES[slug]
    if language == "python": return f"from solution import {name}\n" + "\n".join(f"assert {name}({v!r}) is None" if e is None else f"assert {name}({v!r}) == {e!r}" for v,e in cases) + "\n"
    if language in {"javascript", "typescript"}:
        imp = f"const{{{cam}:f}}=require('./solution');" if language == "javascript" else f"import{{{cam} as f}}from'./solution';"
        checks = "&&".join(f"f({json.dumps(v)})===null" if e is None else f"f({json.dumps(v)})==={json.dumps(e)}" for v,e in cases)
        return imp + f"if(!({checks}))throw Error('contract');\n"
    if language == "go":
        gn="".join(x.title() for x in slug.split("-")); rows=[f"if _,ok:={gn}({json.dumps(v)});ok{{t.Fatal(\"invalid\")}}" if e is None else f"if x,ok:={gn}({json.dumps(v)});!ok||x!={json.dumps(e)}{{t.Fatal(x)}}" for v,e in cases]
        return "package solution\nimport \"testing\"\nfunc TestContract(t *testing.T){"+";".join(rows)+"}\n"
    if language == "java":
        rows=[f"Solution.{cam}({json.dumps(v)})==null" if e is None else f"{json.dumps(e)}.equals(Solution.{cam}({json.dumps(v)}))" for v,e in cases]
        return "public final class SolutionTest{public static void main(String[]z){if(!("+"&&".join(rows)+"))throw new AssertionError();}}\n"
    rows=[f"assert!({name}({json.dumps(v)}).is_none());" if e is None else f"assert_eq!({name}({json.dumps(v)}),Some({json.dumps(e)}.into()));" for v,e in cases]
    return "mod solution;use solution::*;#[test]fn contract(){"+"".join(rows)+"}\n"


FILE = {"go":"Return solution.go in package solution.","java":"Return Solution.java defining public final class Solution.","javascript":"Return CommonJS module solution.js.","typescript":"Return strict TypeScript module solution.ts.","python":"Return solution.py with the function at module scope.","rust":"Return solution.rs with the public function at module scope."}


def api(language: str, slug: str) -> str:
    name, cam = NAMES[slug], camel(slug)
    return {"go":f"func {''.join(x.title() for x in slug.split('-'))}(input string) (string, bool)","java":f"public static String {cam}(String input)","javascript":f"exports.{cam} = function(input)","typescript":f"export function {cam}(input: string): string | null","python":f"def {name}(input: str) -> str | None","rust":f"pub fn {name}(input: &str) -> Option<String>"}[language]


def artifact(language: str, slug: str) -> tuple[str,str,str]:
    ref = python_reference(slug) if language=="python" else js_reference(slug,language=="typescript") if language in {"javascript","typescript"} else go_reference(slug) if language=="go" else java_reference(slug) if language=="java" else rust_reference(slug)
    name,cam=NAMES[slug],camel(slug)
    bad={"python":f"def {name}(input: str) -> str | None:\n return input\n","javascript":f"exports.{cam}=input=>input;\n","typescript":f"export function {cam}(input:string):string|null{{return input}}\n","go":f"package solution\nfunc {''.join(x.title() for x in slug.split('-'))}(input string)(string,bool){{return input,true}}\n","java":f"public final class Solution{{public static String {cam}(String input){{return input;}}}}\n","rust":f"pub fn {name}(input:&str)->Option<String>{{Some(input.to_string())}}\n"}[language]
    return ref,bad,test_source(language,slug)


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC",text).casefold().split())


def comparison_prompts() -> tuple[set[str],set[str],dict[str,int]]:
    exact,norm=set(),set(); counts={"seed":0,"private_development":0,"prior_decision":0}
    for relative in SEED_PATHS:
        with (ROOT/relative).open(encoding="utf-8") as handle:
            for line in handle:
                text=json.loads(line)["messages"][0]["content"]; exact.add(sha256_text(text));norm.add(sha256_text(normalized(text)));counts["seed"]+=1
    for label,paths in (("private_development",DEVELOPMENT_MANIFESTS),("prior_decision",PRIOR_DECISION_MANIFESTS)):
        for relative in paths:
            manifest=load_json(ROOT/relative); claimed=manifest["manifest_sha256"]
            if sha256_object({k:v for k,v in manifest.items() if k!="manifest_sha256"})!=claimed:raise RuntimeError(f"comparison manifest hash mismatch: {relative}")
            if relative.endswith("decision-tranche5.json") and claimed!=EXPECTED_TRANCHE5_SHA256:raise RuntimeError("decision tranche5 changed after tranche6 separation was declared")
            for entry in manifest["tasks"]:
                task=load_json(ROOT/entry["path"])
                if sha256_object(task)!=entry["sha256"]:raise RuntimeError(f"comparison task hash mismatch: {entry['task_id']}")
                text=task["prompt"]["text"];exact.add(sha256_text(text));norm.add(sha256_text(normalized(text)));counts[label]+=1
    return exact,norm,counts


def build() -> tuple[dict,dict]:
    prior_overlap=load_json(ROOT/"manifests/evaluation/private/decision-tranche5-overlap.json")
    if prior_overlap.get("report_sha256")!=EXPECTED_TRANCHE5_OVERLAP_SHA256 or sha256_object({k:v for k,v in prior_overlap.items() if k!="report_sha256"})!=EXPECTED_TRANCHE5_OVERLAP_SHA256:raise RuntimeError("decision tranche5 overlap seal changed")
    OUT.mkdir(parents=True,exist_ok=True);tasks=[];counter:Counter[tuple[str,str]]=Counter()
    for language in RUNTIME:
        for slug,kind in zip(SLUGS,KINDS):
            ref,bad,test=artifact(language,slug); repair=f"\n\nBuggy source to repair:\n\n{bad.rstrip()}" if kind=="repair" else ""
            prompt=f"{'Implement the following API.' if kind=='generation' else 'Repair the buggy source below without changing the required API.'}\n\nFile contract: {FILE[language]}\nRequired API: {api(language,slug)}\nBehavior: {BEHAVIOR[slug]} Reject every malformed input by returning the language-specific absence value.\nVisible example: {EXAMPLE[slug]}{repair}\n\nReturn only the complete source file; do not include Markdown fences or prose."
            files=[]
            if language=="go":
                mod="module private.invalid/ganesh/decision/tranche6\n\ngo 1.22\n";files.append({"path":"go.mod","role":"support","content":mod,"sha256":sha256_text(mod)})
            test_path={"go":"solution_test.go","java":"SolutionTest.java","javascript":"solution.test.js","typescript":"solution.test.ts","python":"test_solution.py","rust":"solution_test.rs"}[language]
            files.append({"path":test_path,"role":"test","content":test,"sha256":sha256_text(test)})
            task={"schema_version":"1.0","task_id":f"decision-t6-{language}-{slug}","surface":"decision","language":language,"family":LANGUAGE_FAMILY[language],"task_type":kind,"prompt":{"text":prompt,"sha256":sha256_text(prompt)},"rendered_prompt":{"text":prompt,"sha256":sha256_text(prompt)},"candidate_path":CANDIDATE_PATH[language],"files":files,"runtime_id":RUNTIME[language],"limits":{"timeout_seconds":60 if language in {"go","java","rust"} else 30,"memory_mb":512,"cpus":1,"pids":64,"output_bytes":65536},"validation":{"reference":{"label":"author-reference","code":ref,"sha256":sha256_text(ref)},"known_bad":[{"label":"identity-instead-of-contract","code":bad,"sha256":sha256_text(bad)}]}}
            validate_task(task);tasks.append(task);counter[(language,kind)]+=1
    exact,norm,counts=comparison_prompts();exact_hits=[t["task_id"] for t in tasks if t["prompt"]["sha256"] in exact];norm_hits=[t["task_id"] for t in tasks if sha256_text(normalized(t["prompt"]["text"])) in norm]
    own_exact=[t["task_id"] for t in tasks if sum(x["prompt"]["sha256"]==t["prompt"]["sha256"] for x in tasks)>1];own_norm=[t["task_id"] for t in tasks if sum(normalized(x["prompt"]["text"])==normalized(t["prompt"]["text"]) for x in tasks)>1]
    if exact_hits or norm_hits or own_exact or own_norm:raise RuntimeError("decision tranche6 prompt overlap")
    entries=[]
    for task in tasks:
        path=OUT/f"{task['task_id']}.task.json";write_json(path,task);entries.append({"task_id":task["task_id"],"language":task["language"],"task_type":task["task_type"],"path":str(path.relative_to(ROOT)),"sha256":sha256_object(task),"prompt_sha256":task["prompt"]["sha256"],"rendered_prompt_sha256":task["rendered_prompt"]["sha256"]})
    manifest={"schema_version":"ganesh-mini-private-eval-manifest/v1","surface":"decision","tranche":"tranche6","status":"authored-unexecuted","task_count":len(tasks),"counts_by_lane":{language:{kind:counter[(language,kind)] for kind in ("generation","repair")} for language in RUNTIME},"runtime_config":"configs/eval/runtimes.json","tasks":entries};manifest["manifest_sha256"]=sha256_object(manifest)
    overlap={"schema_version":"ganesh-mini-evaluation-overlap/v1","evaluation_manifest":str(MANIFEST.relative_to(ROOT)),"evaluation_manifest_sha256":manifest["manifest_sha256"],"comparison_inputs":{"seed_jsonl":list(SEED_PATHS),"private_development_manifests":list(DEVELOPMENT_MANIFESTS),"prior_decision_manifests":list(PRIOR_DECISION_MANIFESTS)},"seed_records_inspected":counts["seed"],"private_development_prompts_inspected":counts["private_development"],"prior_decision_prompts_inspected":counts["prior_decision"],"comparison_prompts_inspected":sum(counts.values()),"evaluation_prompts_inspected":len(tasks),"normalization":"NFKC + Unicode casefold + whitespace collapse","exact_prompt_overlaps":exact_hits,"normalized_prompt_overlaps":norm_hits,"within_tranche_exact_overlaps":own_exact,"within_tranche_normalized_overlaps":own_norm,"status":"passed"};overlap["report_sha256"]=sha256_object(overlap)
    write_json(MANIFEST,manifest);write_json(OVERLAP,overlap);return manifest,overlap


if __name__=="__main__":
    manifest,overlap=build();print(json.dumps({"tasks":manifest["task_count"],"manifest_sha256":manifest["manifest_sha256"],"overlap_sha256":overlap["report_sha256"]},sort_keys=True))
