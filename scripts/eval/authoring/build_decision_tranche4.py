#!/usr/bin/env python3
"""Author and seal private decision tranche 4."""

from __future__ import annotations

import json
import re
import textwrap
import unicodedata
from collections import Counter
from pathlib import Path

from scripts.eval.contracts import (
    CANDIDATE_PATH,
    LANGUAGE_FAMILY,
    load_json,
    sha256_object,
    sha256_text,
    validate_task,
    write_json,
)

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "eval/private/decision/tranche4"
MANIFEST = ROOT / "manifests/evaluation/private/decision-tranche4.json"
OVERLAP = ROOT / "manifests/evaluation/private/decision-tranche4-overlap.json"
SEED_PATHS = ("data/seed/ganesh_v01/train.jsonl", "data/seed/ganesh_v01/validation.jsonl")
DEVELOPMENT_MANIFESTS = tuple(f"manifests/evaluation/private/development-tranche{i}.json" for i in range(1, 7))
PRIOR_DECISION_MANIFESTS = tuple(f"manifests/evaluation/private/decision-tranche{i}.json" for i in range(1, 4))
RUNTIME = {
    "go": "go-1.22.12",
    "java": "java-21.0.11",
    "javascript": "javascript-node-22.23.2",
    "typescript": "typescript-5.5.4-node-22",
    "python": "python-3.11.15",
    "rust": "rust-1.85.0",
}
SLUGS = (
    "parity-stable-partition",
    "nonnegative-prefix",
    "bounded-range-gaps",
    "frequency-leaders",
    "left-cycle",
    "adjacent-differences",
    "last-occurrence-order",
    "band-clamp",
    "strict-prefix-records",
    "consecutive-run-summary",
)
KINDS = ("generation",) * 5 + ("repair",) * 5
NAMES = {slug: slug.replace("-", "_") for slug in SLUGS}

BEHAVIOR = {
    "parity-stable-partition": "Parse a non-empty comma-separated list of canonical signed decimal integers in -1000..1000. Return all even values in their original order followed by all odd values in their original order, joined by commas. Reject malformed or out-of-range input.",
    "nonnegative-prefix": "Parse a non-empty comma-separated list of canonical signed decimal integers in -1000..1000. Return the maximal prefix before the first negative value, joined by commas; return the empty string when the first value is negative. Reject malformed or out-of-range input.",
    "bounded-range-gaps": "Parse a non-empty comma-separated list of canonical signed decimal integers in -1000..1000. Duplicate values are allowed. Return, in increasing order, every integer strictly between the minimum and maximum that is absent from the input, joined by commas. Reject malformed or out-of-range input.",
    "frequency-leaders": "Parse a non-empty comma-separated list of canonical signed decimal integers in -1000..1000. Count occurrences and return every value tied for greatest frequency in increasing numeric order, joined by commas. Reject malformed or out-of-range input.",
    "left-cycle": "Parse canonical k;values where k is an unsigned decimal in 0..1000000 and values is a non-empty comma-separated list of canonical signed integers in -1000..1000. Rotate the list left by k modulo its length and return comma-separated values. Reject malformed or out-of-range input.",
    "adjacent-differences": "Parse a non-empty comma-separated list of canonical signed decimal integers in -1000..1000. Return each next-minus-previous difference in input order, joined by commas; a one-value input returns the empty string. Reject malformed or out-of-range input.",
    "last-occurrence-order": "Parse a non-empty comma-separated list of canonical signed decimal integers in -1000..1000. Keep only each value's final occurrence while preserving the order of those retained positions, and return comma-separated values. Reject malformed or out-of-range input.",
    "band-clamp": "Parse canonical low;high;values where low and high are signed integers in -1000..1000, low must not exceed high, and values is a non-empty comma-separated list under the same bounds. Clamp each value into the inclusive band and return comma-separated values. Reject malformed or out-of-range input.",
    "strict-prefix-records": "Parse a non-empty comma-separated list of canonical signed decimal integers in -1000..1000. Return the first value and every later value that is strictly greater than all preceding values, preserving input order and joining with commas. Reject malformed or out-of-range input.",
    "consecutive-run-summary": "Parse a non-empty comma-separated list of canonical signed decimal integers in -1000..1000. Compress consecutive equal values into value:count records in input order and join records with commas. Reject malformed or out-of-range input.",
}

EXAMPLE = {
    "parity-stable-partition": "3,2,-1,4,0 returns 2,4,0,3,-1.",
    "nonnegative-prefix": "2,0,5,-1,8 returns 2,0,5.",
    "bounded-range-gaps": "3,1,3,6 returns 2,4,5.",
    "frequency-leaders": "4,2,4,2,9 returns 2,4.",
    "left-cycle": "7;10,20,30 returns 20,30,10.",
    "adjacent-differences": "3,8,5,-1 returns 5,-3,-6.",
    "last-occurrence-order": "4,2,4,3,2 returns 4,3,2.",
    "band-clamp": "-2;3;-5,-2,1,9 returns -2,-2,1,3.",
    "strict-prefix-records": "3,1,3,4,2,8 returns 3,4,8.",
    "consecutive-run-summary": "2,2,2,-1,-1,2 returns 2:3,-1:2,2:1.",
}

# Cases are authored independently of the reference implementations. ``None``
# is the invalid-input marker required from nullable/string+bool APIs.
CASES: dict[str, tuple[tuple[str, str | None], ...]] = {
    "parity-stable-partition": (("3,2,-1,4,0", "2,4,0,3,-1"), ("-2,-3", "-2,-3"), ("", None), ("01,2", None), ("1001", None)),
    "nonnegative-prefix": (("2,0,5,-1,8", "2,0,5"), ("-1,2", ""), ("0", "0"), ("1,,2", None), ("+1", None)),
    "bounded-range-gaps": (("3,1,3,6", "2,4,5"), ("-1,0,1", ""), ("5,5", ""), ("--1", None), ("-1001,0", None)),
    "frequency-leaders": (("4,2,4,2,9", "2,4"), ("3,-1,3,2,2", "2,3"), ("7", "7"), ("1, 2", None), ("", None)),
    "left-cycle": (("7;10,20,30", "20,30,10"), ("0;-1,2", "-1,2"), ("2;5", "5"), ("01;1,2", None), ("1;", None)),
    "adjacent-differences": (("3,8,5,-1", "5,-3,-6"), ("7", ""), ("-1000,1000", "2000"), ("1,", None), ("1.0", None)),
    "last-occurrence-order": (("4,2,4,3,2", "4,3,2"), ("1,1,1", "1"), ("-1,0,-1", "0,-1"), ("-0", None), ("1002", None)),
    "band-clamp": (("-2;3;-5,-2,1,9", "-2,-2,1,3"), ("0;0;-1,0,1", "0,0,0"), ("2;1;1", None), ("0;1;", None), ("0;01;1", None)),
    "strict-prefix-records": (("3,1,3,4,2,8", "3,4,8"), ("-2,-1,-1,0", "-2,-1,0"), ("5", "5"), ("1,+2", None), ("", None)),
    "consecutive-run-summary": (("2,2,2,-1,-1,2", "2:3,-1:2,2:1"), ("0", "0:1"), ("1,2,1", "1:1,2:1,1:1"), ("1,,1", None), ("1001", None)),
}


def camel(slug: str) -> str:
    head, *tail = slug.split("-")
    return head + "".join(part.title() for part in tail)


def _py_body(slug: str) -> str:
    bodies = {
        "parity-stable-partition": "return ','.join(map(str,[x for x in a if x%2==0]+[x for x in a if x%2!=0]))",
        "nonnegative-prefix": "o=[]\n for x in a:\n  if x<0:break\n  o.append(x)\n return ','.join(map(str,o))",
        "bounded-range-gaps": "s=set(a);return ','.join(map(str,(x for x in range(min(a)+1,max(a)) if x not in s)))",
        "frequency-leaders": "from collections import Counter\n c=Counter(a);m=max(c.values());return ','.join(map(str,sorted(x for x,n in c.items() if n==m)))",
        "left-cycle": "k,a=p\n k=int(k);n=k%len(a);return ','.join(map(str,a[n:]+a[:n]))",
        "adjacent-differences": "return ','.join(str(a[i]-a[i-1]) for i in range(1,len(a)))",
        "last-occurrence-order": "last={x:i for i,x in enumerate(a)};return ','.join(str(x) for i,x in enumerate(a) if last[x]==i)",
        "band-clamp": "lo,hi,a=p\n return ','.join(str(min(hi,max(lo,x))) for x in a)",
        "strict-prefix-records": "o=[];m=None\n for x in a:\n  if m is None or x>m:o.append(x);m=x\n return ','.join(map(str,o))",
        "consecutive-run-summary": "o=[]\n for x in a:\n  if o and o[-1][0]==x:o[-1][1]+=1\n  else:o.append([x,1])\n return ','.join(f'{x}:{n}' for x,n in o)",
    }
    return bodies[slug]


def python_reference(slug: str) -> str:
    name = NAMES[slug]
    special = slug in {"left-cycle", "band-clamp"}
    parse = (
        " q=s.split(';')\n"
        + (" if len(q)!=2 or not re.fullmatch(r'0|[1-9][0-9]*',q[0]) or int(q[0])>1000000:return None\n p=(q[0],nums(q[1]))\n if p[1] is None:return None\n" if slug == "left-cycle" else " if len(q)!=3:return None\n lo,hi=nums(q[0]),nums(q[1]);a=nums(q[2])\n if lo is None or hi is None or a is None or len(lo)!=1 or len(hi)!=1 or lo[0]>hi[0]:return None\n p=(lo[0],hi[0],a)\n")
    ) if special else " a=nums(s)\n if a is None:return None\n"
    raw_lines = _py_body(slug).splitlines()
    normalized_lines = [raw_lines[0], *(line[1:] if line.startswith(" ") else line for line in raw_lines[1:])]
    body = textwrap.indent("\n".join(normalized_lines), " ")
    return (
        "import re\n"
        "def nums(s):\n"
        " if not s:return None\n"
        " o=[]\n"
        " for z in s.split(','):\n"
        "  if not re.fullmatch(r'0|-?[1-9][0-9]*',z):return None\n"
        "  x=int(z)\n"
        "  if x < -1000 or x > 1000:return None\n"
        "  o.append(x)\n"
        " return o\n"
        f"def {name}(s: str) -> str | None:\n{parse}" + body + "\n"
    )


def js_algorithm(slug: str) -> str:
    return {
        "parity-stable-partition": "return a.filter(x=>x%2===0).concat(a.filter(x=>x%2!==0)).join(',')",
        "nonnegative-prefix": "let o=[];for(const x of a){if(x<0)break;o.push(x)}return o.join(',')",
        "bounded-range-gaps": "let seen=new Set(a),o=[];for(let x=Math.min(...a)+1;x<Math.max(...a);x++)if(!seen.has(x))o.push(x);return o.join(',')",
        "frequency-leaders": "let c=new Map;for(const x of a)c.set(x,(c.get(x)||0)+1);let m=Math.max(...c.values());return[...c].filter(x=>x[1]===m).map(x=>x[0]).sort((x,y)=>x-y).join(',')",
        "left-cycle": "let k=Number(p[0]),n=k%a.length;return a.slice(n).concat(a.slice(0,n)).join(',')",
        "adjacent-differences": "return a.slice(1).map((x,i)=>x-a[i]).join(',')",
        "last-occurrence-order": "let last=new Map;a.forEach((x,i)=>last.set(x,i));return a.filter((x,i)=>last.get(x)===i).join(',')",
        "band-clamp": "return a.map(x=>Math.min(hi,Math.max(lo,x))).join(',')",
        "strict-prefix-records": "let o=[],m=null;for(const x of a)if(m===null||x>m){o.push(x);m=x}return o.join(',')",
        "consecutive-run-summary": "let o:any[]=[];for(const x of a){let q:any=o[o.length-1];if(q&&q[0]===x)q[1]++;else o.push([x,1])}return o.map(x=>x[0]+':'+x[1]).join(',')",
    }[slug]


def javascript_reference(slug: str, typescript: bool) -> str:
    name = camel(slug)
    signature = f"export function {name}(s:string):string|null" if typescript else f"exports.{name}=function(s)"
    parser = "const nums=(s:string):number[]|null=>{if(!s)return null;let o:number[]=[];for(const z of s.split(',')){if(!/^(?:0|-?[1-9][0-9]*)$/.test(z))return null;let x=Number(z);if(x< -1000||x>1000)return null;o.push(x)}return o};" if typescript else "const nums=s=>{if(!s)return null;let o=[];for(const z of s.split(',')){if(!/^(?:0|-?[1-9][0-9]*)$/.test(z))return null;let x=Number(z);if(x< -1000||x>1000)return null;o.push(x)}return o};"
    if slug == "left-cycle":
        setup = "let p=s.split(';');if(p.length!==2||!/^(?:0|[1-9][0-9]*)$/.test(p[0])||Number(p[0])>1000000)return null;let a=nums(p[1]);if(!a)return null;"
    elif slug == "band-clamp":
        setup = "let p=s.split(';');if(p.length!==3)return null;let l=nums(p[0]),h=nums(p[1]),a=nums(p[2]);if(!l||!h||!a||l.length!==1||h.length!==1||l[0]>h[0])return null;let lo=l[0],hi=h[0];"
    else:
        setup = "let a=nums(s);if(!a)return null;"
    algorithm = js_algorithm(slug)
    if not typescript:
        algorithm = algorithm.replace("let o:any[]=", "let o=").replace("let q:any=", "let q=")
    return parser + signature + "{" + setup + algorithm + "}\n"


def go_reference(slug: str) -> str:
    name = camel(slug).title().replace("-", "")
    # title() lowercases internal capitals; derive explicitly instead.
    name = "".join(part.title() for part in slug.split("-"))
    algorithms = {
        "parity-stable-partition": "o:=[]int{};for _,x:=range a{if x%2==0{o=append(o,x)}};for _,x:=range a{if x%2!=0{o=append(o,x)}};return join(o),true",
        "nonnegative-prefix": "o:=[]int{};for _,x:=range a{if x<0{break};o=append(o,x)};return join(o),true",
        "bounded-range-gaps": "lo,hi:=a[0],a[0];seen:=map[int]bool{};for _,x:=range a{seen[x]=true;if x<lo{lo=x};if x>hi{hi=x}};o:=[]int{};for x:=lo+1;x<hi;x++{if !seen[x]{o=append(o,x)}};return join(o),true",
        "frequency-leaders": "c:=map[int]int{};m:=0;for _,x:=range a{c[x]++;if c[x]>m{m=c[x]}};o:=[]int{};for x,n:=range c{if n==m{o=append(o,x)}};sort.Ints(o);return join(o),true",
        "left-cycle": "n:=k%len(a);return join(append(append([]int{},a[n:]...),a[:n]...)),true",
        "adjacent-differences": "o:=[]int{};for i:=1;i<len(a);i++{o=append(o,a[i]-a[i-1])};return join(o),true",
        "last-occurrence-order": "last:=map[int]int{};for i,x:=range a{last[x]=i};o:=[]int{};for i,x:=range a{if last[x]==i{o=append(o,x)}};return join(o),true",
        "band-clamp": "for i,x:=range a{if x<lo{a[i]=lo}else if x>hi{a[i]=hi}};return join(a),true",
        "strict-prefix-records": "o:=[]int{a[0]};m:=a[0];for _,x:=range a[1:]{if x>m{o=append(o,x);m=x}};return join(o),true",
        "consecutive-run-summary": "o:=[]string{};for i,x:=range a{if i==0||x!=a[i-1]{o=append(o,strconv.Itoa(x)+\":1\")}else{q:=strings.Split(o[len(o)-1],\":\");n,_:=strconv.Atoi(q[1]);o[len(o)-1]=q[0]+\":\"+strconv.Itoa(n+1)}};return strings.Join(o,\",\"),true",
    }
    if slug == "left-cycle":
        setup = "p:=strings.Split(s,\";\");if len(p)!=2||!regexp.MustCompile(`^(0|[1-9][0-9]*)$`).MatchString(p[0]){return \"\",false};k,e:=strconv.Atoi(p[0]);if e!=nil||k>1000000{return \"\",false};a,ok:=nums(p[1]);if !ok{return \"\",false};"
    elif slug == "band-clamp":
        setup = "p:=strings.Split(s,\";\");if len(p)!=3{return \"\",false};l,o1:=nums(p[0]);h,o2:=nums(p[1]);a,o3:=nums(p[2]);if !o1||!o2||!o3||len(l)!=1||len(h)!=1||l[0]>h[0]{return \"\",false};lo,hi:=l[0],h[0];"
    else:
        setup = "a,ok:=nums(s);if !ok{return \"\",false};"
    return "package solution\nimport(\"regexp\";\"sort\";\"strconv\";\"strings\")\nvar _=sort.Ints\nfunc nums(s string)([]int,bool){if s==\"\"{return nil,false};o:=[]int{};r:=regexp.MustCompile(`^(0|-?[1-9][0-9]*)$`);for _,z:=range strings.Split(s,\",\"){if !r.MatchString(z){return nil,false};x,e:=strconv.Atoi(z);if e!=nil||x< -1000||x>1000{return nil,false};o=append(o,x)};return o,true}\nfunc join(a []int)string{o:=[]string{};for _,x:=range a{o=append(o,strconv.Itoa(x))};return strings.Join(o,\",\")}\nfunc " + name + "(s string)(string,bool){" + setup + algorithms[slug] + "}\n"


def java_reference(slug: str) -> str:
    name = camel(slug)
    # Java uses one deliberately plain reference interpreter with a mode fixed
    # per task. Tests remain task-specific and do not call any oracle.
    mode = SLUGS.index(slug)
    return f"""import java.util.*;public final class Solution{{
static List<Integer> nums(String s){{if(s.isEmpty())return null;var o=new ArrayList<Integer>();for(var z:s.split(\",\",-1)){{if(!z.matches(\"(?:0|-?[1-9][0-9]*)\"))return null;int x;try{{x=Integer.parseInt(z);}}catch(Exception e){{return null;}}if(x< -1000||x>1000)return null;o.add(x);}}return o;}}
static String j(List<?>a){{return String.join(\",\",a.stream().map(Object::toString).toList());}}
public static String {name}(String s){{int mode={mode};String[]p=s.split(\";\",-1);List<Integer>a;int lo=0,hi=0,k=0;
if(mode==4){{if(p.length!=2||!p[0].matches(\"(?:0|[1-9][0-9]*)\"))return null;try{{k=Integer.parseInt(p[0]);}}catch(Exception e){{return null;}}if(k>1000000||(a=nums(p[1]))==null)return null;}}
else if(mode==7){{if(p.length!=3)return null;var l=nums(p[0]);var h=nums(p[1]);a=nums(p[2]);if(l==null||h==null||a==null||l.size()!=1||h.size()!=1||(lo=l.get(0))>(hi=h.get(0)))return null;}}
else if((a=nums(s))==null)return null;
if(mode==0){{var o=new ArrayList<Integer>();for(int x:a)if(x%2==0)o.add(x);for(int x:a)if(x%2!=0)o.add(x);return j(o);}}
if(mode==1){{var o=new ArrayList<Integer>();for(int x:a){{if(x<0)break;o.add(x);}}return j(o);}}
if(mode==2){{var z=new TreeSet<Integer>(a);var o=new ArrayList<Integer>();for(int x=z.first()+1;x<z.last();x++)if(!z.contains(x))o.add(x);return j(o);}}
if(mode==3){{var c=new TreeMap<Integer,Integer>();int m=0;for(int x:a){{int n=c.merge(x,1,Integer::sum);m=Math.max(m,n);}}var o=new ArrayList<Integer>();for(var e:c.entrySet())if(e.getValue()==m)o.add(e.getKey());return j(o);}}
if(mode==4){{Collections.rotate(a,-(k%a.size()));return j(a);}}
if(mode==5){{var o=new ArrayList<Integer>();for(int i=1;i<a.size();i++)o.add(a.get(i)-a.get(i-1));return j(o);}}
if(mode==6){{var last=new HashMap<Integer,Integer>();for(int i=0;i<a.size();i++)last.put(a.get(i),i);var o=new ArrayList<Integer>();for(int i=0;i<a.size();i++)if(last.get(a.get(i))==i)o.add(a.get(i));return j(o);}}
if(mode==7){{for(int i=0;i<a.size();i++)a.set(i,Math.min(hi,Math.max(lo,a.get(i))));return j(a);}}
if(mode==8){{var o=new ArrayList<Integer>();int m=a.get(0);o.add(m);for(int x:a.subList(1,a.size()))if(x>m){{o.add(x);m=x;}}return j(o);}}
var o=new ArrayList<String>();for(int i=0;i<a.size();){{int q=i+1;while(q<a.size()&&a.get(q).equals(a.get(i)))q++;o.add(a.get(i)+\":\"+(q-i));i=q;}}return j(o);}}
}}\n"""


def rust_reference(slug: str) -> str:
    name = NAMES[slug]
    algorithms = {
        "parity-stable-partition": "let mut o:Vec<_>=a.iter().filter(|x|**x%2==0).copied().collect();o.extend(a.iter().filter(|x|**x%2!=0));Some(join(&o))",
        "nonnegative-prefix": "Some(join(&a.into_iter().take_while(|x|*x>=0).collect::<Vec<_>>()))",
        "bounded-range-gaps": "let s:std::collections::HashSet<_>=a.iter().copied().collect();Some((*a.iter().min()?+1..*a.iter().max()?).filter(|x|!s.contains(x)).map(|x|x.to_string()).collect::<Vec<_>>().join(\",\"))",
        "frequency-leaders": "let mut c=std::collections::BTreeMap::new();for x in a{*c.entry(x).or_insert(0)+=1}let m=*c.values().max()?;Some(c.into_iter().filter(|x|x.1==m).map(|x|x.0.to_string()).collect::<Vec<_>>().join(\",\"))",
        "left-cycle": "let n=k%a.len();a.rotate_left(n);Some(join(&a))",
        "adjacent-differences": "Some(a.windows(2).map(|x|(x[1]-x[0]).to_string()).collect::<Vec<_>>().join(\",\"))",
        "last-occurrence-order": "let mut last=std::collections::HashMap::new();for(i,x)in a.iter().enumerate(){last.insert(*x,i);}Some(a.iter().enumerate().filter(|(i,x)|last[x]==*i).map(|x|x.1.to_string()).collect::<Vec<_>>().join(\",\"))",
        "band-clamp": "Some(a.into_iter().map(|x|x.clamp(lo,hi).to_string()).collect::<Vec<_>>().join(\",\"))",
        "strict-prefix-records": "let mut m=None;Some(a.into_iter().filter(|x|if m.is_none_or(|v|*x>v){m=Some(*x);true}else{false}).map(|x|x.to_string()).collect::<Vec<_>>().join(\",\"))",
        "consecutive-run-summary": "let mut o=vec![];let mut i=0;while i<a.len(){let mut q=i+1;while q<a.len()&&a[q]==a[i]{q+=1}o.push(format!(\"{}:{}\",a[i],q-i));i=q}Some(o.join(\",\"))",
    }
    if slug == "left-cycle":
        setup = "let p:Vec<_>=s.split(';').collect();if p.len()!=2||!p[0].bytes().all(|x|x.is_ascii_digit())||p[0].len()>1&&p[0].starts_with('0'){return None}let k:usize=p[0].parse().ok()?;if k>1000000{return None}let mut a=nums(p[1])?;"
    elif slug == "band-clamp":
        setup = "let p:Vec<_>=s.split(';').collect();if p.len()!=3{return None}let l=nums(p[0])?;let h=nums(p[1])?;let a=nums(p[2])?;if l.len()!=1||h.len()!=1||l[0]>h[0]{return None}let(lo,hi)=(l[0],h[0]);"
    else:
        setup = "let a=nums(s)?;"
    return "fn nums(s:&str)->Option<Vec<i32>>{if s.is_empty(){return None}let mut o=vec![];for z in s.split(','){let x:i32=z.parse().ok()?;if x.to_string()!=z||x< -1000||x>1000{return None}o.push(x)}Some(o)}fn join(a:&[i32])->String{a.iter().map(|x|x.to_string()).collect::<Vec<_>>().join(\",\")}pub fn " + name + "(s:&str)->Option<String>{" + setup + algorithms[slug] + "}\n"


def test_source(language: str, slug: str) -> str:
    name, cases = NAMES[slug], CASES[slug]
    cam = camel(slug)
    if language == "python":
        checks = "\n".join(f"assert {name}({value!r}) is None" if expected is None else f"assert {name}({value!r}) == {expected!r}" for value, expected in cases)
        return f"from solution import {name}\n{checks}\n"
    if language in {"javascript", "typescript"}:
        eq = "===null" if language == "javascript" else "===null"
        checks = "&&".join(f"f({json.dumps(value)}){eq}" if expected is None else f"f({json.dumps(value)})==={json.dumps(expected)}" for value, expected in cases)
        imp = f"const{{{cam}:f}}=require('./solution');" if language == "javascript" else f"import{{{cam} as f}}from'./solution';"
        return imp + f"if(!({checks}))throw Error('contract');\n"
    if language == "go":
        gname = "".join(part.title() for part in slug.split("-"))
        rows = []
        for value, expected in cases:
            if expected is None:
                rows.append(f"if _,ok:={gname}({json.dumps(value)});ok{{t.Fatal(\"invalid\")}}")
            else:
                rows.append(f"if x,ok:={gname}({json.dumps(value)});!ok||x!={json.dumps(expected)}{{t.Fatal(x)}}")
        return "package solution\nimport \"testing\"\nfunc TestContract(t *testing.T){" + ";".join(rows) + "}\n"
    if language == "java":
        rows = []
        for value, expected in cases:
            call = f"Solution.{cam}({json.dumps(value)})"
            rows.append(call + "==null" if expected is None else f"{json.dumps(expected)}.equals({call})")
        return "public final class SolutionTest{public static void main(String[]z){if(!(" + "&&".join(rows) + "))throw new AssertionError();}}\n"
    rows = []
    for value, expected in cases:
        rows.append(f"assert!({name}({json.dumps(value)}).is_none());" if expected is None else f"assert_eq!({name}({json.dumps(value)}),Some({json.dumps(expected)}.into()));")
    return "mod solution;use solution::*;#[test]fn contract(){" + "".join(rows) + "}\n"


def artifact(language: str, slug: str) -> tuple[str, str, str]:
    if language == "python":
        ref = python_reference(slug)
    elif language == "javascript":
        ref = javascript_reference(slug, False)
    elif language == "typescript":
        ref = javascript_reference(slug, True)
    elif language == "go":
        ref = go_reference(slug)
    elif language == "java":
        ref = java_reference(slug)
    else:
        ref = rust_reference(slug)
    name = NAMES[slug]
    cam = camel(slug)
    bad = {
        "python": f"def {name}(input: str) -> str | None:\n return input\n",
        "javascript": f"exports.{cam}=input=>input;\n",
        "typescript": f"export function {cam}(input:string):string|null{{return input}}\n",
        "go": f"package solution\nfunc {''.join(part.title() for part in slug.split('-'))}(input string)(string,bool){{return input,true}}\n",
        "java": f"public final class Solution{{public static String {cam}(String input){{return input;}}}}\n",
        "rust": f"pub fn {name}(input:&str)->Option<String>{{Some(input.to_string())}}\n",
    }[language]
    return ref, bad, test_source(language, slug)


FILE = {
    "go": "Return solution.go in package solution.",
    "java": "Return Solution.java defining public final class Solution.",
    "javascript": "Return CommonJS module solution.js.",
    "typescript": "Return strict TypeScript module solution.ts.",
    "python": "Return solution.py with the function at module scope.",
    "rust": "Return solution.rs with the public function at module scope.",
}


def api(language: str, slug: str) -> str:
    name, cam = NAMES[slug], camel(slug)
    return {
        "go": f"func {''.join(part.title() for part in slug.split('-'))}(input string) (string, bool)",
        "java": f"public static String {cam}(String input)",
        "javascript": f"exports.{cam} = function(input)",
        "typescript": f"export function {cam}(input: string): string | null",
        "python": f"def {name}(input: str) -> str | None",
        "rust": f"pub fn {name}(input: &str) -> Option<String>",
    }[language]


def prompt_for(language: str, slug: str, kind: str, bad: str) -> str:
    head = "Implement the following API." if kind == "generation" else "Repair the buggy source below without changing the required API."
    repair = f"\n\nBuggy source to repair:\n\n{bad.rstrip()}" if kind == "repair" else ""
    return f"{head}\n\nFile contract: {FILE[language]}\nRequired API: {api(language, slug)}\nBehavior: {BEHAVIOR[slug]}\nVisible example: {EXAMPLE[slug]}{repair}\n\nReturn only the complete source file; do not include Markdown fences or prose."


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def comparison_prompts() -> tuple[set[str], set[str], dict[str, int]]:
    exact: set[str] = set()
    norm: set[str] = set()
    counts = {"seed": 0, "private_development": 0, "prior_decision": 0}
    for relative in SEED_PATHS:
        with (ROOT / relative).open(encoding="utf-8") as handle:
            for line in handle:
                text = json.loads(line)["messages"][0]["content"]
                exact.add(sha256_text(text))
                norm.add(sha256_text(normalized(text)))
                counts["seed"] += 1
    for label, paths in (("private_development", DEVELOPMENT_MANIFESTS), ("prior_decision", PRIOR_DECISION_MANIFESTS)):
        for relative in paths:
            manifest = load_json(ROOT / relative)
            claimed = manifest["manifest_sha256"]
            if sha256_object({k: v for k, v in manifest.items() if k != "manifest_sha256"}) != claimed:
                raise RuntimeError(f"comparison manifest hash mismatch: {relative}")
            for entry in manifest["tasks"]:
                task = load_json(ROOT / entry["path"])
                if sha256_object(task) != entry["sha256"]:
                    raise RuntimeError(f"comparison task hash mismatch: {entry['task_id']}")
                text = task["prompt"]["text"]
                exact.add(sha256_text(text))
                norm.add(sha256_text(normalized(text)))
                counts[label] += 1
    return exact, norm, counts


def build() -> tuple[dict, dict]:
    OUT.mkdir(parents=True, exist_ok=True)
    tasks = []
    counter: Counter[tuple[str, str]] = Counter()
    for language in RUNTIME:
        for slug, kind in zip(SLUGS, KINDS):
            ref, bad, test = artifact(language, slug)
            prompt = prompt_for(language, slug, kind, bad)
            files = []
            if language == "go":
                mod = "module private.invalid/ganesh/decision/tranche4\n\ngo 1.22\n"
                files.append({"path": "go.mod", "role": "support", "content": mod, "sha256": sha256_text(mod)})
            test_path = {"go": "solution_test.go", "java": "SolutionTest.java", "javascript": "solution.test.js", "typescript": "solution.test.ts", "python": "test_solution.py", "rust": "solution_test.rs"}[language]
            files.append({"path": test_path, "role": "test", "content": test, "sha256": sha256_text(test)})
            timeout = 60 if language in {"go", "java", "rust"} else 30
            task = {
                "schema_version": "1.0",
                "task_id": f"decision-t4-{language}-{slug}",
                "surface": "decision",
                "language": language,
                "family": LANGUAGE_FAMILY[language],
                "task_type": kind,
                "prompt": {"text": prompt, "sha256": sha256_text(prompt)},
                "rendered_prompt": {"text": prompt, "sha256": sha256_text(prompt)},
                "candidate_path": CANDIDATE_PATH[language],
                "files": files,
                "runtime_id": RUNTIME[language],
                "limits": {"timeout_seconds": timeout, "memory_mb": 512, "cpus": 1, "pids": 64, "output_bytes": 65536},
                "validation": {"reference": {"label": "author-reference", "code": ref, "sha256": sha256_text(ref)}, "known_bad": [{"label": "identity-instead-of-contract", "code": bad, "sha256": sha256_text(bad)}]},
            }
            validate_task(task)
            tasks.append(task)
            counter[(language, kind)] += 1
    exact, norm, counts = comparison_prompts()
    exact_hits = [t["task_id"] for t in tasks if t["prompt"]["sha256"] in exact]
    norm_hits = [t["task_id"] for t in tasks if sha256_text(normalized(t["prompt"]["text"])) in norm]
    own_exact = [t["task_id"] for t in tasks if sum(x["prompt"]["sha256"] == t["prompt"]["sha256"] for x in tasks) > 1]
    own_norm = [t["task_id"] for t in tasks if sum(normalized(x["prompt"]["text"]) == normalized(t["prompt"]["text"]) for x in tasks) > 1]
    if exact_hits or norm_hits or own_exact or own_norm:
        raise RuntimeError("decision tranche4 prompt overlap")
    entries = []
    for task in tasks:
        path = OUT / f"{task['task_id']}.task.json"
        write_json(path, task)
        entries.append({"task_id": task["task_id"], "language": task["language"], "task_type": task["task_type"], "path": str(path.relative_to(ROOT)), "sha256": sha256_object(task), "prompt_sha256": task["prompt"]["sha256"], "rendered_prompt_sha256": task["rendered_prompt"]["sha256"]})
    manifest = {"schema_version": "ganesh-mini-private-eval-manifest/v1", "surface": "decision", "tranche": "tranche4", "status": "authored-unexecuted", "task_count": len(tasks), "counts_by_lane": {language: {kind: counter[(language, kind)] for kind in ("generation", "repair")} for language in RUNTIME}, "runtime_config": "configs/eval/runtimes.json", "tasks": entries}
    manifest["manifest_sha256"] = sha256_object(manifest)
    overlap = {"schema_version": "ganesh-mini-evaluation-overlap/v1", "evaluation_manifest": str(MANIFEST.relative_to(ROOT)), "evaluation_manifest_sha256": manifest["manifest_sha256"], "comparison_inputs": {"seed_jsonl": list(SEED_PATHS), "private_development_manifests": list(DEVELOPMENT_MANIFESTS), "prior_decision_manifests": list(PRIOR_DECISION_MANIFESTS)}, "seed_records_inspected": counts["seed"], "private_development_prompts_inspected": counts["private_development"], "prior_decision_prompts_inspected": counts["prior_decision"], "comparison_prompts_inspected": sum(counts.values()), "evaluation_prompts_inspected": len(tasks), "normalization": "NFKC + Unicode casefold + whitespace collapse", "exact_prompt_overlaps": exact_hits, "normalized_prompt_overlaps": norm_hits, "within_tranche_exact_overlaps": own_exact, "within_tranche_normalized_overlaps": own_norm, "status": "passed"}
    overlap["report_sha256"] = sha256_object(overlap)
    write_json(MANIFEST, manifest)
    write_json(OVERLAP, overlap)
    return manifest, overlap


if __name__ == "__main__":
    built_manifest, built_overlap = build()
    print(json.dumps({"tasks": built_manifest["task_count"], "manifest_sha256": built_manifest["manifest_sha256"], "overlap_sha256": built_overlap["report_sha256"]}, sort_keys=True))
