#!/usr/bin/env python3
"""Author and seal private decision tranche 5."""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

from scripts.eval.contracts import CANDIDATE_PATH, LANGUAGE_FAMILY, load_json, sha256_object, sha256_text, validate_task, write_json

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "eval/private/decision/tranche5"
MANIFEST = ROOT / "manifests/evaluation/private/decision-tranche5.json"
OVERLAP = ROOT / "manifests/evaluation/private/decision-tranche5-overlap.json"
SEED_PATHS = ("data/seed/ganesh_v01/train.jsonl", "data/seed/ganesh_v01/validation.jsonl")
DEVELOPMENT_MANIFESTS = tuple(f"manifests/evaluation/private/development-tranche{i}.json" for i in range(1, 7))
PRIOR_DECISION_MANIFESTS = tuple(f"manifests/evaluation/private/decision-tranche{i}.json" for i in range(1, 5))
EXPECTED_TRANCHE4_SHA256 = "118dbb5086725bd36ceed09ba37d1f14c53a7f41d79e365c0a6260ac24fb2658"
RUNTIME = {
    "go": "go-1.22.12", "java": "java-21.0.11", "javascript": "javascript-node-22.23.2",
    "typescript": "typescript-5.5.4-node-22", "python": "python-3.11.15", "rust": "rust-1.85.0",
}
SLUGS = (
    "signed-distance", "alternating-ends", "threshold-stable-partition", "unique-sorted-squares",
    "circular-deltas", "first-occurrence-order", "triple-window-sums", "magnitude-leaders",
    "zero-segment-sums", "rank-compress",
)
KINDS = ("generation",) * 5 + ("repair",) * 5
NAMES = {slug: slug.replace("-", "_") for slug in SLUGS}

BEHAVIOR = {
    "signed-distance": "Parse canonical a;b, where each field is one signed decimal integer in -1000..1000. Return the absolute distance between a and b as a decimal string. Reject malformed or out-of-range input.",
    "alternating-ends": "Parse a non-empty comma-separated list of canonical signed decimal integers in -1000..1000. Return values by taking leftmost, rightmost, next-leftmost, next-rightmost until exhausted, joined by commas. Reject malformed or out-of-range input.",
    "threshold-stable-partition": "Parse canonical threshold;values, where threshold is one signed integer and values is a non-empty comma-separated list, all in -1000..1000. Return values below threshold in original order followed by values at least threshold in original order, joined by commas. Reject malformed or out-of-range input.",
    "unique-sorted-squares": "Parse a non-empty comma-separated list of canonical signed decimal integers in -1000..1000. Square every value, remove duplicates, sort increasing, and return comma-separated decimal values. Reject malformed or out-of-range input.",
    "circular-deltas": "Parse a non-empty comma-separated list of canonical signed decimal integers in -1000..1000. Return next-minus-current for each position, with the first value following the last; a singleton returns 0. Reject malformed or out-of-range input.",
    "first-occurrence-order": "Parse a non-empty comma-separated list of canonical signed decimal integers in -1000..1000. Keep only the first occurrence of each value, preserving input order, and return comma-separated values. Reject malformed or out-of-range input.",
    "triple-window-sums": "Parse a non-empty comma-separated list of canonical signed decimal integers in -1000..1000. Return sums of every consecutive three-value window in left-to-right order, joined by commas; fewer than three values returns the empty string. Reject malformed or out-of-range input.",
    "magnitude-leaders": "Parse a non-empty comma-separated list of canonical signed decimal integers in -1000..1000. Return every input occurrence whose absolute value equals the greatest absolute value present, preserving order and duplicates. Reject malformed or out-of-range input.",
    "zero-segment-sums": "Parse a non-empty comma-separated list of canonical signed decimal integers in -1000..1000. Treat zero as a separator; return the sum of each non-empty segment between zeros in input order, omitting empty segments, joined by commas. Reject malformed or out-of-range input.",
    "rank-compress": "Parse a non-empty comma-separated list of canonical signed decimal integers in -1000..1000. Replace each value by its zero-based index in the increasing sorted set of distinct input values and return the ranks in input order, joined by commas. Reject malformed or out-of-range input.",
}
EXAMPLE = {
    "signed-distance": "-4;7 returns 11.", "alternating-ends": "1,2,3,4,5 returns 1,5,2,4,3.",
    "threshold-stable-partition": "3;5,1,3,2,4 returns 1,2,5,3,4.",
    "unique-sorted-squares": "-3,2,3,0,-2 returns 0,4,9.", "circular-deltas": "2,5,1 returns 3,-4,1.",
    "first-occurrence-order": "4,2,4,3,2 returns 4,2,3.", "triple-window-sums": "1,2,3,4 returns 6,9.",
    "magnitude-leaders": "-5,2,5,-5 returns -5,5,-5.", "zero-segment-sums": "2,-1,0,4,3,0,0,-2 returns 1,7,-2.",
    "rank-compress": "40,10,40,20 returns 2,0,2,1.",
}
CASES: dict[str, tuple[tuple[str, str | None], ...]] = {
    "signed-distance": (("-4;7", "11"), ("5;5", "0"), ("-1000;1000", "2000"), ("1,2;3", None), ("01;2", None)),
    "alternating-ends": (("1,2,3,4,5", "1,5,2,4,3"), (("-1,0,9,8"), "-1,8,0,9"), (("7"), "7"), ("", None), ("1, 2", None)),
    "threshold-stable-partition": (("3;5,1,3,2,4", "1,2,5,3,4"), ("0;-1,0,-2,2", "-1,-2,0,2"), ("9;9", "9"), ("1;", None), ("+1;2", None)),
    "unique-sorted-squares": (("-3,2,3,0,-2", "0,4,9"), ("-1,1", "1"), ("10", "100"), ("1,,2", None), ("1001", None)),
    "circular-deltas": (("2,5,1", "3,-4,1"), ("7", "0"), ("-1000,1000", "2000,-2000"), ("-0", None), ("1,", None)),
    "first-occurrence-order": (("4,2,4,3,2", "4,2,3"), ("1,1,1", "1"), ("-1,0,-1", "-1,0"), ("", None), ("1.0", None)),
    "triple-window-sums": (("1,2,3,4", "6,9"), ("1,2", ""), ("-1000,0,1000", "0"), ("1,+2,3", None), ("1,,3", None)),
    "magnitude-leaders": (("-5,2,5,-5", "-5,5,-5"), ("0,0", "0,0"), ("-3,2", "-3"), ("01", None), ("", None)),
    "zero-segment-sums": (("2,-1,0,4,3,0,0,-2", "1,7,-2"), ("0,0", ""), ("1,2", "3"), ("1, 0", None), ("1002", None)),
    "rank-compress": (("40,10,40,20", "2,0,2,1"), ("-2,-1,0", "0,1,2"), ("5,5", "0,0"), ("--1", None), ("", None)),
}


def camel(slug: str) -> str:
    head, *tail = slug.split("-")
    return head + "".join(part.title() for part in tail)


def py_algorithm(slug: str) -> str:
    return {
        "signed-distance": "a,b=p;return str(abs(a-b))",
        "alternating-ends": "o=[];i=0;j=len(a)-1\nwhile i<=j:\n o.append(a[i]);i+=1\n if i<=j:o.append(a[j]);j-=1\nreturn join(o)",
        "threshold-stable-partition": "t,a=p;return join([x for x in a if x<t]+[x for x in a if x>=t])",
        "unique-sorted-squares": "return join(sorted({x*x for x in a}))",
        "circular-deltas": "return join([a[(i+1)%len(a)]-x for i,x in enumerate(a)])",
        "first-occurrence-order": "o=[];s=set()\nfor x in a:\n if x not in s:s.add(x);o.append(x)\nreturn join(o)",
        "triple-window-sums": "return join([sum(a[i:i+3]) for i in range(len(a)-2)])",
        "magnitude-leaders": "m=max(abs(x) for x in a);return join([x for x in a if abs(x)==m])",
        "zero-segment-sums": "o=[];n=0;seen=False\nfor x in a+[0]:\n if x==0:\n  if seen:o.append(n);n=0;seen=False\n else:n+=x;seen=True\nreturn join(o)",
        "rank-compress": "r={x:i for i,x in enumerate(sorted(set(a)))};return join([r[x] for x in a])",
    }[slug]


def python_reference(slug: str) -> str:
    name = NAMES[slug]
    if slug == "signed-distance":
        setup = " p=s.split(';')\n if len(p)!=2:return None\n a,b=nums(p[0]),nums(p[1])\n if a is None or b is None or len(a)!=1 or len(b)!=1:return None\n p=(a[0],b[0])\n"
    elif slug == "threshold-stable-partition":
        setup = " p=s.split(';')\n if len(p)!=2:return None\n t,a=nums(p[0]),nums(p[1])\n if t is None or a is None or len(t)!=1:return None\n p=(t[0],a)\n"
    else:
        setup = " a=nums(s)\n if a is None:return None\n"
    body = py_algorithm(slug).replace("\n", "\n ")
    return "import re\ndef nums(s):\n if not s:return None\n o=[]\n for z in s.split(','):\n  if not re.fullmatch(r'0|-?[1-9][0-9]*',z):return None\n  x=int(z)\n  if x < -1000 or x > 1000:return None\n  o.append(x)\n return o\ndef join(a):return ','.join(map(str,a))\n" + f"def {name}(s: str) -> str | None:\n{setup} " + body + "\n"


def js_algorithm(slug: str) -> str:
    return {
        "signed-distance": "let[a,b]=p;return String(Math.abs(a-b))",
        "alternating-ends": "let o=[],i=0,j=a.length-1;while(i<=j){o.push(a[i++]);if(i<=j)o.push(a[j--])}return o.join(',')",
        "threshold-stable-partition": "return a.filter(x=>x<t).concat(a.filter(x=>x>=t)).join(',')",
        "unique-sorted-squares": "return[...new Set(a.map(x=>x*x))].sort((x,y)=>x-y).join(',')",
        "circular-deltas": "return a.map((x,i)=>a[(i+1)%a.length]-x).join(',')",
        "first-occurrence-order": "return a.filter((x,i)=>a.indexOf(x)===i).join(',')",
        "triple-window-sums": "return a.slice(2).map((_,i)=>a[i]+a[i+1]+a[i+2]).join(',')",
        "magnitude-leaders": "let m=Math.max(...a.map(Math.abs));return a.filter(x=>Math.abs(x)===m).join(',')",
        "zero-segment-sums": "let o=[],n=0,z=false;for(const x of [...a,0]){if(x===0){if(z)o.push(n);n=0;z=false}else{n+=x;z=true}}return o.join(',')",
        "rank-compress": "let u=[...new Set(a)].sort((x,y)=>x-y),r=new Map(u.map((x,i)=>[x,i]));return a.map(x=>r.get(x)).join(',')",
    }[slug]


def javascript_reference(slug: str, typescript: bool) -> str:
    name = camel(slug)
    sig = f"export function {name}(s:string):string|null" if typescript else f"exports.{name}=function(s)"
    parser = "const nums" + ("=(s:string):number[]|null=>" if typescript else "=s=>") + "{if(!s)return null;let o=[];for(const z of s.split(',')){if(!/^(?:0|-?[1-9][0-9]*)$/.test(z))return null;let x=Number(z);if(x< -1000||x>1000)return null;o.push(x)}return o};"
    if slug == "signed-distance":
        setup = "let q=s.split(';');if(q.length!==2)return null;let x=nums(q[0]),y=nums(q[1]);if(!x||!y||x.length!==1" + ("||y.length!==1" if slug == "signed-distance" else "") + ")return null;let p=[x[0]," + ("y[0]" if slug == "signed-distance" else "y") + "];"
    elif slug == "threshold-stable-partition":
        setup = "let q=s.split(';');if(q.length!==2)return null;let x=nums(q[0]),y=nums(q[1]);if(!x||!y||x.length!==1)return null;let t=x[0],a=y;"
    else:
        setup = "let a=nums(s);if(!a)return null;"
    return parser + sig + "{" + setup + js_algorithm(slug) + "}\n"


def go_reference(slug: str) -> str:
    name = "".join(part.title() for part in slug.split("-"))
    algorithms = {
        "signed-distance": "d:=p[0]-p[1];if d<0{d= -d};return strconv.Itoa(d),true",
        "alternating-ends": "o:=[]int{};for i,j:=0,len(a)-1;i<=j;i,j=i+1,j-1{o=append(o,a[i]);if i<j{o=append(o,a[j])}};return join(o),true",
        "threshold-stable-partition": "o:=[]int{};for _,x:=range a{if x<t{o=append(o,x)}};for _,x:=range a{if x>=t{o=append(o,x)}};return join(o),true",
        "unique-sorted-squares": "seen:=map[int]bool{};for _,x:=range a{seen[x*x]=true};o:=[]int{};for x:=range seen{o=append(o,x)};sort.Ints(o);return join(o),true",
        "circular-deltas": "o:=[]int{};for i,x:=range a{o=append(o,a[(i+1)%len(a)]-x)};return join(o),true",
        "first-occurrence-order": "seen:=map[int]bool{};o:=[]int{};for _,x:=range a{if !seen[x]{seen[x]=true;o=append(o,x)}};return join(o),true",
        "triple-window-sums": "o:=[]int{};for i:=0;i+2<len(a);i++{o=append(o,a[i]+a[i+1]+a[i+2])};return join(o),true",
        "magnitude-leaders": "m:=0;for _,x:=range a{if x<0{x= -x};if x>m{m=x}};o:=[]int{};for _,x:=range a{q:=x;if q<0{q= -q};if q==m{o=append(o,x)}};return join(o),true",
        "zero-segment-sums": "o:=[]int{};n:=0;seen:=false;for _,x:=range append(a,0){if x==0{if seen{o=append(o,n)};n=0;seen=false}else{n+=x;seen=true}};return join(o),true",
        "rank-compress": "u:=append([]int{},a...);sort.Ints(u);r:=map[int]int{};n:=0;for _,x:=range u{if _,ok:=r[x];!ok{r[x]=n;n++}};o:=[]int{};for _,x:=range a{o=append(o,r[x])};return join(o),true",
    }
    if slug in {"signed-distance", "threshold-stable-partition"}:
        setup = "q:=strings.Split(s,\";\");if len(q)!=2{return \"\",false};p,o1:=nums(q[0]);a,o2:=nums(q[1]);if !o1||!o2||len(p)!=1" + ("||len(a)!=1" if slug == "signed-distance" else "") + "{return \"\",false};" + ("p=[]int{p[0],a[0]};" if slug == "signed-distance" else "t:=p[0];")
    else:
        setup = "a,ok:=nums(s);if !ok{return \"\",false};"
    return "package solution\nimport(\"regexp\";\"sort\";\"strconv\";\"strings\")\nvar _=sort.Ints\nfunc nums(s string)([]int,bool){if s==\"\"{return nil,false};o:=[]int{};r:=regexp.MustCompile(`^(0|-?[1-9][0-9]*)$`);for _,z:=range strings.Split(s,\",\"){if !r.MatchString(z){return nil,false};x,e:=strconv.Atoi(z);if e!=nil||x< -1000||x>1000{return nil,false};o=append(o,x)};return o,true}\nfunc join(a []int)string{o:=[]string{};for _,x:=range a{o=append(o,strconv.Itoa(x))};return strings.Join(o,\",\")}\nfunc " + name + "(s string)(string,bool){" + setup + algorithms[slug] + "}\n"


def java_reference(slug: str) -> str:
    name, mode = camel(slug), SLUGS.index(slug)
    return f'''import java.util.*;public final class Solution{{
static List<Integer> n(String s){{if(s.isEmpty())return null;var o=new ArrayList<Integer>();for(var z:s.split(",",-1)){{if(!z.matches("(?:0|-?[1-9][0-9]*)"))return null;try{{int x=Integer.parseInt(z);if(x< -1000||x>1000)return null;o.add(x);}}catch(Exception e){{return null;}}}}return o;}}
static String j(List<?>a){{return String.join(",",a.stream().map(Object::toString).toList());}}
public static String {name}(String s){{int mode={mode};List<Integer>a;int t=0,b=0;String[]q=s.split(";",-1);if(mode==0||mode==2){{if(q.length!=2)return null;var x=n(q[0]);a=n(q[1]);if(x==null||a==null||x.size()!=1||(mode==0&&a.size()!=1))return null;t=x.get(0);if(mode==0)b=a.get(0);}}else if((a=n(s))==null)return null;
if(mode==0)return Integer.toString(Math.abs(t-b));if(mode==1){{var o=new ArrayList<Integer>();for(int i=0,k=a.size()-1;i<=k;i++,k--){{o.add(a.get(i));if(i<k)o.add(a.get(k));}}return j(o);}}if(mode==2){{var o=new ArrayList<Integer>();for(int x:a)if(x<t)o.add(x);for(int x:a)if(x>=t)o.add(x);return j(o);}}if(mode==3){{var o=new TreeSet<Integer>();for(int x:a)o.add(x*x);return j(new ArrayList<>(o));}}if(mode==4){{var o=new ArrayList<Integer>();for(int i=0;i<a.size();i++)o.add(a.get((i+1)%a.size())-a.get(i));return j(o);}}if(mode==5)return j(new ArrayList<>(new LinkedHashSet<>(a)));if(mode==6){{var o=new ArrayList<Integer>();for(int i=0;i+2<a.size();i++)o.add(a.get(i)+a.get(i+1)+a.get(i+2));return j(o);}}if(mode==7){{int m=a.stream().mapToInt(Math::abs).max().getAsInt();return j(a.stream().filter(x->Math.abs(x)==m).toList());}}if(mode==8){{var o=new ArrayList<Integer>();int z=0;boolean seen=false;for(int i=0;i<=a.size();i++){{int x=i==a.size()?0:a.get(i);if(x==0){{if(seen)o.add(z);z=0;seen=false;}}else{{z+=x;seen=true;}}}}return j(o);}}var u=new TreeSet<Integer>(a);var r=new HashMap<Integer,Integer>();int i=0;for(int x:u)r.put(x,i++);return j(a.stream().map(r::get).toList());}}
}}\n'''


def rust_reference(slug: str) -> str:
    name = NAMES[slug]
    alg = {
        "signed-distance": "let d=(p[0]-p[1]).abs();Some(d.to_string())",
        "alternating-ends": "let(mut o,mut i,mut j)=(vec![],0,a.len()-1);while i<=j{o.push(a[i]);if i<j{o.push(a[j]);}i+=1;if j==0{break}j-=1}Some(join(&o))",
        "threshold-stable-partition": "let(t,a)=(p[0],a);Some(a.iter().filter(|x|**x<t).chain(a.iter().filter(|x|**x>=t)).map(|x|x.to_string()).collect::<Vec<_>>().join(\",\"))",
        "unique-sorted-squares": "let s:std::collections::BTreeSet<_>=a.into_iter().map(|x|x*x).collect();Some(s.into_iter().map(|x|x.to_string()).collect::<Vec<_>>().join(\",\"))",
        "circular-deltas": "Some((0..a.len()).map(|i|(a[(i+1)%a.len()]-a[i]).to_string()).collect::<Vec<_>>().join(\",\"))",
        "first-occurrence-order": "let mut s=std::collections::HashSet::new();Some(a.into_iter().filter(|x|s.insert(*x)).map(|x|x.to_string()).collect::<Vec<_>>().join(\",\"))",
        "triple-window-sums": "Some(a.windows(3).map(|x|(x[0]+x[1]+x[2]).to_string()).collect::<Vec<_>>().join(\",\"))",
        "magnitude-leaders": "let m=a.iter().map(|x|x.abs()).max()?;Some(a.into_iter().filter(|x|x.abs()==m).map(|x|x.to_string()).collect::<Vec<_>>().join(\",\"))",
        "zero-segment-sums": "let(mut o,mut n,mut seen)=(vec![],0,false);for x in a.into_iter().chain(std::iter::once(0)){if x==0{if seen{o.push(n)}n=0;seen=false}else{n+=x;seen=true}}Some(join(&o))",
        "rank-compress": "let u:std::collections::BTreeSet<_>=a.iter().copied().collect();let r:std::collections::HashMap<_,_>=u.into_iter().enumerate().map(|(i,x)|(x,i)).collect();Some(a.into_iter().map(|x|r[&x].to_string()).collect::<Vec<_>>().join(\",\"))",
    }[slug]
    if slug in {"signed-distance", "threshold-stable-partition"}:
        setup = "let q:Vec<_>=s.split(';').collect();if q.len()!=2{return None}let p=nums(q[0])?;let a=nums(q[1])?;if p.len()!=1" + ("||a.len()!=1" if slug == "signed-distance" else "") + "{return None}" + ("let p=[p[0],a[0]];" if slug == "signed-distance" else "")
    else:
        setup = "let a=nums(s)?;"
    return "fn nums(s:&str)->Option<Vec<i32>>{if s.is_empty(){return None}let mut o=vec![];for z in s.split(','){let x:i32=z.parse().ok()?;if x.to_string()!=z||x< -1000||x>1000{return None}o.push(x)}Some(o)}fn join(a:&[i32])->String{a.iter().map(|x|x.to_string()).collect::<Vec<_>>().join(\",\")}pub fn " + name + "(s:&str)->Option<String>{" + setup + alg + "}\n"


def test_source(language: str, slug: str) -> str:
    name, cam, cases = NAMES[slug], camel(slug), CASES[slug]
    if language == "python":
        return f"from solution import {name}\n" + "\n".join(f"assert {name}({v!r}) is None" if e is None else f"assert {name}({v!r}) == {e!r}" for v, e in cases) + "\n"
    if language in {"javascript", "typescript"}:
        imp = f"const{{{cam}:f}}=require('./solution');" if language == "javascript" else f"import{{{cam} as f}}from'./solution';"
        checks = "&&".join(f"f({json.dumps(v)})===null" if e is None else f"f({json.dumps(v)})==={json.dumps(e)}" for v, e in cases)
        return imp + f"if(!({checks}))throw Error('contract');\n"
    if language == "go":
        gn = "".join(part.title() for part in slug.split("-")); rows = []
        for v, e in cases:
            rows.append(f"if _,ok:={gn}({json.dumps(v)});ok{{t.Fatal(\"invalid\")}}" if e is None else f"if x,ok:={gn}({json.dumps(v)});!ok||x!={json.dumps(e)}{{t.Fatal(x)}}")
        return "package solution\nimport \"testing\"\nfunc TestContract(t *testing.T){" + ";".join(rows) + "}\n"
    if language == "java":
        rows = [f"Solution.{cam}({json.dumps(v)})==null" if e is None else f"{json.dumps(e)}.equals(Solution.{cam}({json.dumps(v)}))" for v, e in cases]
        return "public final class SolutionTest{public static void main(String[]z){if(!(" + "&&".join(rows) + "))throw new AssertionError();}}\n"
    rows = [f"assert!({name}({json.dumps(v)}).is_none());" if e is None else f"assert_eq!({name}({json.dumps(v)}),Some({json.dumps(e)}.into()));" for v, e in cases]
    return "mod solution;use solution::*;#[test]fn contract(){" + "".join(rows) + "}\n"


FILE = {"go": "Return solution.go in package solution.", "java": "Return Solution.java defining public final class Solution.", "javascript": "Return CommonJS module solution.js.", "typescript": "Return strict TypeScript module solution.ts.", "python": "Return solution.py with the function at module scope.", "rust": "Return solution.rs with the public function at module scope."}


def api(language: str, slug: str) -> str:
    name, cam = NAMES[slug], camel(slug)
    return {"go": f"func {''.join(part.title() for part in slug.split('-'))}(input string) (string, bool)", "java": f"public static String {cam}(String input)", "javascript": f"exports.{cam} = function(input)", "typescript": f"export function {cam}(input: string): string | null", "python": f"def {name}(input: str) -> str | None", "rust": f"pub fn {name}(input: &str) -> Option<String>"}[language]


def artifact(language: str, slug: str) -> tuple[str, str, str]:
    if language == "python": ref = python_reference(slug)
    elif language == "javascript": ref = javascript_reference(slug, False)
    elif language == "typescript": ref = javascript_reference(slug, True)
    elif language == "go": ref = go_reference(slug)
    elif language == "java": ref = java_reference(slug)
    else: ref = rust_reference(slug)
    name, cam = NAMES[slug], camel(slug)
    bad = {"python": f"def {name}(input: str) -> str | None:\n return input\n", "javascript": f"exports.{cam}=input=>input;\n", "typescript": f"export function {cam}(input:string):string|null{{return input}}\n", "go": f"package solution\nfunc {''.join(part.title() for part in slug.split('-'))}(input string)(string,bool){{return input,true}}\n", "java": f"public final class Solution{{public static String {cam}(String input){{return input;}}}}\n", "rust": f"pub fn {name}(input:&str)->Option<String>{{Some(input.to_string())}}\n"}[language]
    return ref, bad, test_source(language, slug)


def prompt_for(language: str, slug: str, kind: str, bad: str) -> str:
    head = "Implement the following API." if kind == "generation" else "Repair the buggy source below without changing the required API."
    repair = f"\n\nBuggy source to repair:\n\n{bad.rstrip()}" if kind == "repair" else ""
    return f"{head}\n\nFile contract: {FILE[language]}\nRequired API: {api(language, slug)}\nBehavior: {BEHAVIOR[slug]}\nVisible example: {EXAMPLE[slug]}{repair}\n\nReturn only the complete source file; do not include Markdown fences or prose."


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def comparison_prompts() -> tuple[set[str], set[str], dict[str, int]]:
    exact, norm = set(), set(); counts = {"seed": 0, "private_development": 0, "prior_decision": 0}
    for relative in SEED_PATHS:
        with (ROOT / relative).open(encoding="utf-8") as handle:
            for line in handle:
                text = json.loads(line)["messages"][0]["content"]; exact.add(sha256_text(text)); norm.add(sha256_text(normalized(text))); counts["seed"] += 1
    for label, paths in (("private_development", DEVELOPMENT_MANIFESTS), ("prior_decision", PRIOR_DECISION_MANIFESTS)):
        for relative in paths:
            manifest = load_json(ROOT / relative); claimed = manifest["manifest_sha256"]
            if sha256_object({k: v for k, v in manifest.items() if k != "manifest_sha256"}) != claimed: raise RuntimeError(f"comparison manifest hash mismatch: {relative}")
            if relative.endswith("decision-tranche4.json") and claimed != EXPECTED_TRANCHE4_SHA256: raise RuntimeError("decision tranche4 changed after tranche5 separation was declared")
            for entry in manifest["tasks"]:
                task = load_json(ROOT / entry["path"])
                if sha256_object(task) != entry["sha256"]: raise RuntimeError(f"comparison task hash mismatch: {entry['task_id']}")
                text = task["prompt"]["text"]; exact.add(sha256_text(text)); norm.add(sha256_text(normalized(text))); counts[label] += 1
    return exact, norm, counts


def build() -> tuple[dict, dict]:
    OUT.mkdir(parents=True, exist_ok=True); tasks = []; counter: Counter[tuple[str, str]] = Counter()
    for language in RUNTIME:
        for slug, kind in zip(SLUGS, KINDS):
            ref, bad, test = artifact(language, slug); prompt = prompt_for(language, slug, kind, bad); files = []
            if language == "go":
                mod = "module private.invalid/ganesh/decision/tranche5\n\ngo 1.22\n"; files.append({"path": "go.mod", "role": "support", "content": mod, "sha256": sha256_text(mod)})
            test_path = {"go": "solution_test.go", "java": "SolutionTest.java", "javascript": "solution.test.js", "typescript": "solution.test.ts", "python": "test_solution.py", "rust": "solution_test.rs"}[language]
            files.append({"path": test_path, "role": "test", "content": test, "sha256": sha256_text(test)})
            timeout = 60 if language in {"go", "java", "rust"} else 30
            task = {"schema_version": "1.0", "task_id": f"decision-t5-{language}-{slug}", "surface": "decision", "language": language, "family": LANGUAGE_FAMILY[language], "task_type": kind, "prompt": {"text": prompt, "sha256": sha256_text(prompt)}, "rendered_prompt": {"text": prompt, "sha256": sha256_text(prompt)}, "candidate_path": CANDIDATE_PATH[language], "files": files, "runtime_id": RUNTIME[language], "limits": {"timeout_seconds": timeout, "memory_mb": 512, "cpus": 1, "pids": 64, "output_bytes": 65536}, "validation": {"reference": {"label": "author-reference", "code": ref, "sha256": sha256_text(ref)}, "known_bad": [{"label": "identity-instead-of-contract", "code": bad, "sha256": sha256_text(bad)}]}}
            validate_task(task); tasks.append(task); counter[(language, kind)] += 1
    exact, norm, counts = comparison_prompts(); exact_hits = [t["task_id"] for t in tasks if t["prompt"]["sha256"] in exact]; norm_hits = [t["task_id"] for t in tasks if sha256_text(normalized(t["prompt"]["text"])) in norm]
    own_exact = [t["task_id"] for t in tasks if sum(x["prompt"]["sha256"] == t["prompt"]["sha256"] for x in tasks) > 1]; own_norm = [t["task_id"] for t in tasks if sum(normalized(x["prompt"]["text"]) == normalized(t["prompt"]["text"]) for x in tasks) > 1]
    if exact_hits or norm_hits or own_exact or own_norm: raise RuntimeError("decision tranche5 prompt overlap")
    entries = []
    for task in tasks:
        path = OUT / f"{task['task_id']}.task.json"; write_json(path, task); entries.append({"task_id": task["task_id"], "language": task["language"], "task_type": task["task_type"], "path": str(path.relative_to(ROOT)), "sha256": sha256_object(task), "prompt_sha256": task["prompt"]["sha256"], "rendered_prompt_sha256": task["rendered_prompt"]["sha256"]})
    manifest = {"schema_version": "ganesh-mini-private-eval-manifest/v1", "surface": "decision", "tranche": "tranche5", "status": "authored-unexecuted", "task_count": len(tasks), "counts_by_lane": {language: {kind: counter[(language, kind)] for kind in ("generation", "repair")} for language in RUNTIME}, "runtime_config": "configs/eval/runtimes.json", "tasks": entries}; manifest["manifest_sha256"] = sha256_object(manifest)
    overlap = {"schema_version": "ganesh-mini-evaluation-overlap/v1", "evaluation_manifest": str(MANIFEST.relative_to(ROOT)), "evaluation_manifest_sha256": manifest["manifest_sha256"], "comparison_inputs": {"seed_jsonl": list(SEED_PATHS), "private_development_manifests": list(DEVELOPMENT_MANIFESTS), "prior_decision_manifests": list(PRIOR_DECISION_MANIFESTS)}, "seed_records_inspected": counts["seed"], "private_development_prompts_inspected": counts["private_development"], "prior_decision_prompts_inspected": counts["prior_decision"], "comparison_prompts_inspected": sum(counts.values()), "evaluation_prompts_inspected": len(tasks), "normalization": "NFKC + Unicode casefold + whitespace collapse", "exact_prompt_overlaps": exact_hits, "normalized_prompt_overlaps": norm_hits, "within_tranche_exact_overlaps": own_exact, "within_tranche_normalized_overlaps": own_norm, "status": "passed"}; overlap["report_sha256"] = sha256_object(overlap)
    write_json(MANIFEST, manifest); write_json(OVERLAP, overlap); return manifest, overlap


if __name__ == "__main__":
    built_manifest, built_overlap = build(); print(json.dumps({"tasks": built_manifest["task_count"], "manifest_sha256": built_manifest["manifest_sha256"], "overlap_sha256": built_overlap["report_sha256"]}, sort_keys=True))
