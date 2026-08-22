#!/usr/bin/env python3
"""Author and seal private decision tranche 1 without executing candidates."""

from __future__ import annotations

import json
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.eval.contracts import CANDIDATE_PATH, LANGUAGE_FAMILY, load_json, sha256_object, sha256_text, validate_task, write_json

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "eval/private/decision/tranche1"
MANIFEST = ROOT / "manifests/evaluation/private/decision-tranche1.json"
OVERLAP = ROOT / "manifests/evaluation/private/decision-tranche1-overlap.json"
SEED_PATHS = ("data/seed/ganesh_v01/train.jsonl", "data/seed/ganesh_v01/validation.jsonl")
DEVELOPMENT_MANIFESTS = tuple(f"manifests/evaluation/private/development-tranche{i}.json" for i in range(1, 7))
RUNTIME = {"go":"go-1.22.12","java":"java-21.0.11","javascript":"javascript-node-22.23.2","typescript":"typescript-5.5.4-node-22","python":"python-3.11.15","rust":"rust-1.85.0"}
SLUGS = ("api-token-validation","escaped-field-parser","metric-rollup","retry-plan","circuit-trace","bounded-window-rollup","error-summary","tag-patch","ascii-query-escape","version-compaction")
KINDS = ("generation",) * 5 + ("repair",) * 5

BEHAVIOR = {
"api-token-validation":"Trim ASCII spaces, then validate scheme:name:version. Scheme is non-empty lowercase ASCII letters; name is lowercase ASCII letters or digits separated by single interior hyphens; version is canonical unsigned decimal in 0..9223372036854775807. Return the canonical token, otherwise invalid.",
"escaped-field-parser":"Parse comma-separated fields where backslash may escape only comma or backslash. Empty fields are retained. Reject a dangling backslash or any other escape. Return decoded fields joined by |.",
"metric-rollup":"Parse semicolon-separated key=amount records. Keys are non-empty lowercase ASCII identifiers with letters, digits, or interior hyphens; amounts are canonical non-negative decimals. Sum repeated keys with signed-64-bit overflow rejection and return sorted key=sum records joined by semicolons.",
"retry-plan":"Parse comma-separated canonical three-digit ASCII HTTP status codes in 100..599. Stop successfully at the first 2xx and return the zero-based indices of earlier retryable statuses joined by commas. Retryable statuses are 408, 429, 500, 502, 503, and 504. A different status before success returns fatal@index. If all are retryable, return their indices.",
"circuit-trace":"Parse threshold;events where threshold is a canonical positive decimal in 1..2147483647 and events contain only S or F. S resets consecutive failures. Reaching threshold failures opens the circuit; it then remains open. Return one C or O state per event, joined without separators.",
"bounded-window-rollup":"Parse start,end,limit;timestamp=value records. Start, end, timestamps, and values are canonical signed decimals in -9223372036854775808..9223372036854775807; limit is canonical unsigned decimal in 0..2147483647. Require start <= end. Select timestamps in [start,end), stable-sort by timestamp, retain the latest limit records, and return count:sum with signed-64-bit overflow rejection. Limit zero returns 0:0.",
"error-summary":"Parse a non-empty comma-separated sequence of TIMEOUT, IO, AUTH, or BAD_INPUT. TIMEOUT and IO are transient; AUTH and BAD_INPUT are permanent. Reject empty or unknown tokens and return permanent=N;transient=N.",
"tag-patch":"Parse base;operations. Keys start with a lowercase ASCII letter and contain lowercase letters or digits separated by single interior hyphens. Values may contain = but not comma or semicolon. Base key=value pairs are comma-separated and unique; operations are set:key=value or unset:key and apply in order. Reject malformed data or duplicate base keys. Return sorted final key=value pairs joined by commas.",
"ascii-query-escape":"Accept printable ASCII only. Preserve letters, digits, hyphen, period, underscore, and tilde; encode every other byte as uppercase %HH. Reject controls and non-ASCII input.",
"version-compaction":"Parse semicolon-separated version:key=value changes. Versions are canonical unsigned decimals in 0..9223372036854775807. Keys start with a lowercase ASCII letter and contain lowercase letters or digits separated by single interior hyphens. Values may contain = but not semicolon. Keep the greatest-version value per key; reject duplicate key+version pairs. Return sorted key=value@version records joined by semicolons.",
}
EXAMPLE = {
"api-token-validation":" auth:user-2:0  returns auth:user-2:0; Auth:user:1 is invalid.",
"escaped-field-parser":r"a\,b,c\\d, returns a,b|c\d|; a\q is invalid.",
"metric-rollup":"cpu=2;mem=3;cpu=4 returns cpu=6;mem=3.",
"retry-plan":"503,429,200,500 returns 0,1; 503,404 returns fatal@1.",
"circuit-trace":"2;FSFFS returns CCCOO.",
"bounded-window-rollup":"3,10,2;8=5,3=2,8=7,10=99 returns 2:12.",
"error-summary":"TIMEOUT,AUTH,IO returns permanent=1;transient=2.",
"tag-patch":"a=1,b=2;unset:a,set:b=3,set:c=4 returns b=3,c=4.",
"ascii-query-escape":"a b+c returns a%20b%2Bc.",
"version-compaction":"2:mode=fast;1:mode=safe;3:zone=west returns mode=fast@2;zone=west@3.",
}

NAMES = {
"api-token-validation":"api_token_validation","escaped-field-parser":"escaped_field_parser","metric-rollup":"metric_rollup","retry-plan":"retry_plan","circuit-trace":"circuit_trace","bounded-window-rollup":"bounded_window_rollup","error-summary":"error_summary","tag-patch":"tag_patch","ascii-query-escape":"ascii_query_escape","version-compaction":"version_compaction",
}

# Each reference is intentionally a self-contained implementation. The compact common
# engines keep the six language translations reviewable while task tests remain distinct.
PY_ENGINE = r'''import re
def _run(s,m):
 try:
  if m==0:
   s=s.strip(' '); p=s.split(':')
   return s if len(p)==3 and re.fullmatch('[a-z]+',p[0]) and re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',p[1]) and re.fullmatch('0|[1-9][0-9]*',p[2]) and int(p[2])<=9223372036854775807 else None
  if m==1:
   o=[];b='';e=False
   for c in s:
    if e:
     if c not in ',\\':return None
     b+=c;e=False
    elif c=='\\':e=True
    elif c==',':o.append(b);b=''
    else:b+=c
   if e:return None
   o.append(b);return '|'.join(o)
  if m==2:
   d={}
   for r in s.split(';'):
    p=r.split('=')
    if len(p)!=2 or not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',p[0]) or not re.fullmatch('0|[1-9][0-9]*',p[1]):return None
    v=d.get(p[0],0)+int(p[1])
    if v>9223372036854775807:return None
    d[p[0]]=v
   return ';'.join(f'{k}={d[k]}' for k in sorted(d))
  if m==3:
   out=[]
   for i,x in enumerate(s.split(',')):
    if not re.fullmatch('[1-5][0-9]{2}',x):return None
    c=int(x)
    if 200<=c<=299:return ','.join(map(str,out))
    if c in (408,429,500,502,503,504):out.append(i)
    else:return f'fatal@{i}'
   return ','.join(map(str,out))
  if m==4:
   p=s.split(';')
   if len(p)!=2 or not re.fullmatch('[1-9][0-9]*',p[0]) or any(c not in 'SF' for c in p[1]):return None
   n=int(p[0]);
   if n>2147483647:return None
   f=0;opened=False;o=''
   for c in p[1]:
    if not opened:f=0 if c=='S' else f+1;opened=f>=n
    o+='O' if opened else 'C'
   return o
  if m==5:
   h,body=s.split(';',1); a=h.split(',')
   if len(a)!=3 or not all(re.fullmatch('0|-?[1-9][0-9]*',x) for x in a[:2]) or not re.fullmatch('0|[1-9][0-9]*',a[2]):return None
   start,end,limit=map(int,a)
   if start>end or limit>2147483647 or any(x<-(1<<63) or x>(1<<63)-1 for x in (start,end)):return None
   rows=[]
   if body:
    for i,r in enumerate(body.split(',')):
     p=r.split('=')
     if len(p)!=2 or not all(re.fullmatch('0|-?[1-9][0-9]*',x) for x in p):return None
     t,v=map(int,p)
     if not -(1<<63)<=t<(1<<63) or not -(1<<63)<=v<(1<<63):return None
     if start<=t<end:rows.append((t,i,v))
   rows.sort();rows=rows[-limit:] if limit else []
   total=sum(x[2] for x in rows)
   return f'{len(rows)}:{total}' if -(1<<63)<=total<(1<<63) else None
  if m==6:
   p=s.split(',');
   if not p or any(x not in ('TIMEOUT','IO','AUTH','BAD_INPUT') for x in p):return None
   t=sum(x in ('TIMEOUT','IO') for x in p);return f'permanent={len(p)-t};transient={t}'
  if m==7:
   if s.count(';')!=1:return None
   base,ops=s.split(';',1);d={};key=re.compile('[a-z][a-z0-9]*(?:-[a-z0-9]+)*')
   if base:
    for r in base.split(','):
     p=r.split('=',1)
     if len(p)!=2 or not key.fullmatch(p[0]) or p[0] in d:return None
     d[p[0]]=p[1]
   if ops:
    for op in ops.split(','):
     if op.startswith('set:'):
      p=op[4:].split('=',1)
      if len(p)!=2 or not key.fullmatch(p[0]):return None
      d[p[0]]=p[1]
     elif op.startswith('unset:') and key.fullmatch(op[6:]):d.pop(op[6:],None)
     else:return None
   return ','.join(f'{k}={d[k]}' for k in sorted(d))
  if m==8:
   if any(ord(c)<32 or ord(c)>126 for c in s):return None
   return ''.join(c if c.isascii() and (c.isalnum() or c in '-._~') else f'%{ord(c):02X}' for c in s)
  d={};seen=set()
  for r in s.split(';'):
   left,val=r.split('=',1);v,key=left.split(':',1)
   if not re.fullmatch('0|[1-9][0-9]*',v) or int(v)>9223372036854775807 or not re.fullmatch('[a-z][a-z0-9]*(?:-[a-z0-9]+)*',key) or (key,v) in seen:return None
   seen.add((key,v));iv=int(v)
   if key not in d or iv>d[key][0]:d[key]=(iv,val)
  return ';'.join(f'{k}={d[k][1]}@{d[k][0]}' for k in sorted(d))
 except (ValueError,OverflowError):return None
'''

JS_ENGINE = r'''function run(s,m){
 try{
 if(m===0){s=s.replace(/^ +| +$/g,'');let p=s.split(':');return p.length===3&&/^[a-z]+$/.test(p[0])&&/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(p[1])&&/^(?:0|[1-9][0-9]*)$/.test(p[2])&&BigInt(p[2])<=9223372036854775807n?s:null}
 if(m===1){let o=[],b='',e=false;for(const c of s){if(e){if(c!==','&&c!=='\\')return null;b+=c;e=false}else if(c==='\\')e=true;else if(c===','){o.push(b);b=''}else b+=c}if(e)return null;o.push(b);return o.join('|')}
 if(m===2){let d=new Map;for(const r of s.split(';')){let p=r.split('=');if(p.length!==2||!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(p[0])||!/^(?:0|[1-9][0-9]*)$/.test(p[1]))return null;let v=(d.get(p[0])||0n)+BigInt(p[1]);if(v>9223372036854775807n)return null;d.set(p[0],v)}return[...d].sort().map(x=>x[0]+'='+x[1]).join(';')}
 if(m===3){let o=[];for(const [i,x]of s.split(',').entries()){if(!/^[1-5][0-9]{2}$/.test(x))return null;let c=+x;if(c>=200&&c<=299)return o.join(',');if([408,429,500,502,503,504].includes(c))o.push(i);else return'fatal@'+i}return o.join(',')}
 if(m===4){let p=s.split(';');if(p.length!==2||!/^[1-9]\d*$/.test(p[0])||BigInt(p[0])>2147483647n||/[^SF]/.test(p[1]))return null;let n=Number(p[0]),f=0,open=false,o='';for(const c of p[1]){if(!open){f=c==='S'?0:f+1;open=f>=n}o+=open?'O':'C'}return o}
 if(m===5){let [h,b,...z]=s.split(';');if(z.length)return null;let a=h.split(',');const signed=/^(?:0|-?[1-9]\d*)$/,unsigned=/^(?:0|[1-9]\d*)$/,lo=-9223372036854775808n,hi=9223372036854775807n;if(a.length!==3||!signed.test(a[0])||!signed.test(a[1])||!unsigned.test(a[2]))return null;let start=BigInt(a[0]),end=BigInt(a[1]),limit=BigInt(a[2]);if(start<lo||start>hi||end<lo||end>hi||start>end||limit>2147483647n)return null;let rows=[];if(b)for(const [i,r]of b.split(',').entries()){let at=r.indexOf('='),p=[r.slice(0,at),r.slice(at+1)];if(at<0||!signed.test(p[0])||!signed.test(p[1]))return null;let t=BigInt(p[0]),v=BigInt(p[1]);if(t<lo||t>hi||v<lo||v>hi)return null;if(t>=start&&t<end)rows.push([t,i,v])}rows.sort((a,b)=>a[0]<b[0]?-1:a[0]>b[0]?1:a[1]-b[1]);rows=limit?rows.slice(-Number(limit)):[];let sum=rows.reduce((q,x)=>q+x[2],0n);return sum>=lo&&sum<=hi?rows.length+':'+sum:null}
 if(m===6){let p=s.split(',');if(!p.length||p.some(x=>!['TIMEOUT','IO','AUTH','BAD_INPUT'].includes(x)))return null;let t=p.filter(x=>x==='TIMEOUT'||x==='IO').length;return`permanent=${p.length-t};transient=${t}`}
 if(m===7){let p=s.split(';');if(p.length!==2)return null;let d={},k=/^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/;if(p[0])for(const r of p[0].split(',')){let at=r.indexOf('='),q=[r.slice(0,at),r.slice(at+1)];if(at<0||!k.test(q[0])||Object.hasOwn(d,q[0]))return null;d[q[0]]=q[1]}if(p[1])for(const op of p[1].split(',')){if(op.startsWith('set:')){let x=op.slice(4),at=x.indexOf('='),q=[x.slice(0,at),x.slice(at+1)];if(at<0||!k.test(q[0]))return null;d[q[0]]=q[1]}else if(op.startsWith('unset:')&&k.test(op.slice(6)))delete d[op.slice(6)];else return null}return Object.keys(d).sort().map(k=>k+'='+d[k]).join(',')}
 if(m===8){if([...s].some(c=>c.charCodeAt(0)<32||c.charCodeAt(0)>126))return null;return[...s].map(c=>/[A-Za-z0-9._~-]/.test(c)?c:'%'+c.charCodeAt(0).toString(16).toUpperCase().padStart(2,'0')).join('')}
 let d=new Map,seen=new Set;for(const r of s.split(';')){let at=r.indexOf('='),left=r.slice(0,at),val=r.slice(at+1),q=left.split(':');if(at<0||q.length!==2||!/^(?:0|[1-9]\d*)$/.test(q[0])||BigInt(q[0])>9223372036854775807n||!/^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/.test(q[1])||seen.has(left))return null;seen.add(left);let v=BigInt(q[0]);if(!d.has(q[1])||v>d.get(q[1])[0])d.set(q[1],[v,val])}return[...d].sort().map(x=>x[0]+'='+x[1][1]+'@'+x[1][0]).join(';')
}catch(e){return null}}
'''

TS_ENGINE = r'''function run(s:string,m:number):string|null{
 try{
 if(m===0){s=s.replace(/^ +| +$/g,'');const p:string[]=s.split(':');return p.length===3&&/^[a-z]+$/.test(p[0])&&/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(p[1])&&/^(?:0|[1-9][0-9]*)$/.test(p[2])&&BigInt(p[2])<=9223372036854775807n?s:null}
 if(m===1){const o:string[]=[];let b='',e=false;for(const c of s){if(e){if(c!==','&&c!=='\\')return null;b+=c;e=false}else if(c==='\\')e=true;else if(c===','){o.push(b);b=''}else b+=c}if(e)return null;o.push(b);return o.join('|')}
 if(m===2){const d=new Map<string,bigint>();for(const r of s.split(';')){const p=r.split('=');if(p.length!==2||!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(p[0])||!/^(?:0|[1-9][0-9]*)$/.test(p[1]))return null;const v=(d.get(p[0])??0n)+BigInt(p[1]);if(v>9223372036854775807n)return null;d.set(p[0],v)}return[...d].sort(([a],[b])=>a<b?-1:a>b?1:0).map(([k,v])=>k+'='+v).join(';')}
 if(m===3){const o:number[]=[];for(const [i,x]of s.split(',').entries()){if(!/^[1-5][0-9]{2}$/.test(x))return null;const c=Number(x);if(c>=200&&c<=299)return o.join(',');if([408,429,500,502,503,504].includes(c))o.push(i);else return'fatal@'+i}return o.join(',')}
 if(m===4){const p=s.split(';');if(p.length!==2||!/^[1-9]\d*$/.test(p[0])||BigInt(p[0])>2147483647n||/[^SF]/.test(p[1]))return null;const n=Number(p[0]);let f=0,open=false,o='';for(const c of p[1]){if(!open){f=c==='S'?0:f+1;open=f>=n}o+=open?'O':'C'}return o}
 if(m===5){const parts=s.split(';');if(parts.length!==2)return null;const [h,b]=parts,a=h.split(','),signed=/^(?:0|-?[1-9]\d*)$/,unsigned=/^(?:0|[1-9]\d*)$/,lo=-9223372036854775808n,hi=9223372036854775807n;if(a.length!==3||!signed.test(a[0])||!signed.test(a[1])||!unsigned.test(a[2]))return null;const start=BigInt(a[0]),end=BigInt(a[1]),limit=BigInt(a[2]);if(start<lo||start>hi||end<lo||end>hi||start>end||limit>2147483647n)return null;let rows:Array<[bigint,number,bigint]>=[];if(b)for(const [i,r]of b.split(',').entries()){const at=r.indexOf('='),p=[r.slice(0,at),r.slice(at+1)];if(at<0||!signed.test(p[0])||!signed.test(p[1]))return null;const t=BigInt(p[0]),v=BigInt(p[1]);if(t<lo||t>hi||v<lo||v>hi)return null;if(t>=start&&t<end)rows.push([t,i,v])}rows.sort((a,b)=>a[0]<b[0]?-1:a[0]>b[0]?1:a[1]-b[1]);rows=limit!==0n?rows.slice(-Number(limit)):[];const sum=rows.reduce((q,x)=>q+x[2],0n);return sum>=lo&&sum<=hi?rows.length+':'+sum:null}
 if(m===6){const p=s.split(',');if(!p.length||p.some(x=>!['TIMEOUT','IO','AUTH','BAD_INPUT'].includes(x)))return null;const t=p.filter(x=>x==='TIMEOUT'||x==='IO').length;return`permanent=${p.length-t};transient=${t}`}
 if(m===7){const p=s.split(';');if(p.length!==2)return null;const d:Record<string,string>=Object.create(null) as Record<string,string>,k=/^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/;if(p[0])for(const r of p[0].split(',')){const at=r.indexOf('='),key=r.slice(0,at),value=r.slice(at+1);if(at<0||!k.test(key)||Object.hasOwn(d,key))return null;d[key]=value}if(p[1])for(const op of p[1].split(',')){if(op.startsWith('set:')){const x=op.slice(4),at=x.indexOf('='),key=x.slice(0,at),value=x.slice(at+1);if(at<0||!k.test(key))return null;d[key]=value}else if(op.startsWith('unset:')&&k.test(op.slice(6)))delete d[op.slice(6)];else return null}return Object.keys(d).sort().map(key=>key+'='+d[key]).join(',')}
 if(m===8){if([...s].some(c=>c.charCodeAt(0)<32||c.charCodeAt(0)>126))return null;return[...s].map(c=>/[A-Za-z0-9._~-]/.test(c)?c:'%'+c.charCodeAt(0).toString(16).toUpperCase().padStart(2,'0')).join('')}
 const d=new Map<string,[bigint,string]>(),seen=new Set<string>();for(const r of s.split(';')){const at=r.indexOf('='),left=r.slice(0,at),val=r.slice(at+1),q=left.split(':');if(at<0||q.length!==2||!/^(?:0|[1-9]\d*)$/.test(q[0])||BigInt(q[0])>9223372036854775807n||!/^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/.test(q[1])||seen.has(left))return null;seen.add(left);const v=BigInt(q[0]),old=d.get(q[1]);if(!old||v>old[0])d.set(q[1],[v,val])}return[...d].sort(([a],[b])=>a<b?-1:a>b?1:0).map(([k,[v,value]])=>k+'='+value+'@'+v).join(';')
 }catch{return null}}
'''

def _wrapper(language: str, slug: str, mode: int) -> tuple[str, str, str, str]:
    snake=NAMES[slug]; camel="".join([snake.split('_')[0], *[x.title() for x in snake.split('_')[1:]]])
    if language=="python":
        ref=PY_ENGINE+f"\ndef {snake}(input: str) -> str | None:\n return _run(input,{mode})\n"
        bad=f"def {snake}(input: str) -> str | None:\n return input\n"
        api=f"def {snake}(input: str) -> str | None"
        return ref,bad,api,snake
    if language=="javascript":
        ref=JS_ENGINE+f"\nexports.{camel}=s=>run(s,{mode});\n";bad=f"exports.{camel}=s=>s;\n";api=f"exports.{camel} = function(input)";return ref,bad,api,camel
    if language=="typescript":
        ref=TS_ENGINE+f"\nexport function {camel}(input:string):string|null{{return run(input,{mode})}}\n";bad=f"export function {camel}(input:string):string|null{{return input}}\n";api=f"export function {camel}(input: string): string | null";return ref,bad,api,camel
    return _native_wrapper(language, slug, mode, snake, camel)

# Go, Java, and Rust use task-specific references to retain their native error contracts.
def _native_wrapper(language: str, slug: str, mode: int, snake: str, camel: str) -> tuple[str,str,str,str]:
    impl = NATIVE[language][slug]
    if language=="go": return impl, f"package solution\nfunc {camel[0].upper()+camel[1:]}(input string)(string,bool){{return input,true}}\n", f"func {camel[0].upper()+camel[1:]}(input string) (string, bool)", camel[0].upper()+camel[1:]
    if language=="java": return impl, f"public final class Solution{{public static String {camel}(String input){{return input;}}}}\n", f"public static String {camel}(String input)", camel
    return impl, f"pub fn {snake}(input:&str)->Option<String>{{Some(input.to_string())}}\n", f"pub fn {snake}(input: &str) -> Option<String>", snake

NATIVE: dict[str,dict[str,str]] = {"go":{},"java":{},"rust":{}}

NATIVE["go"] = {
"api-token-validation":r'''package solution
import("regexp";"strconv";"strings")
func ApiTokenValidation(s string)(string,bool){s=strings.Trim(s," ");p:=strings.Split(s,":");if len(p)!=3||!regexp.MustCompile(`^[a-z]+$`).MatchString(p[0])||!regexp.MustCompile(`^[a-z0-9]+(?:-[a-z0-9]+)*$`).MatchString(p[1])||!regexp.MustCompile(`^(?:0|[1-9][0-9]*)$`).MatchString(p[2]){return "",false};_,e:=strconv.ParseInt(p[2],10,64);return s,e==nil}
''',
"escaped-field-parser":r'''package solution
import "strings"
func EscapedFieldParser(s string)(string,bool){o:=[]string{};var b strings.Builder;e:=false;for _,c:=range s{if e{if c!=','&&c!='\\'{return "",false};b.WriteRune(c);e=false}else if c=='\\'{e=true}else if c==','{o=append(o,b.String());b.Reset()}else{b.WriteRune(c)}};if e{return "",false};o=append(o,b.String());return strings.Join(o,"|"),true}
''',
"metric-rollup":r'''package solution
import("math";"regexp";"sort";"strconv";"strings")
func MetricRollup(s string)(string,bool){d:=map[string]int64{};for _,r:=range strings.Split(s,";"){p:=strings.Split(r,"=");if len(p)!=2||!regexp.MustCompile(`^[a-z0-9]+(?:-[a-z0-9]+)*$`).MatchString(p[0])||!regexp.MustCompile(`^(?:0|[1-9][0-9]*)$`).MatchString(p[1]){return "",false};v,e:=strconv.ParseInt(p[1],10,64);if e!=nil||v>math.MaxInt64-d[p[0]]{return "",false};d[p[0]]+=v};k:=make([]string,0,len(d));for x:=range d{k=append(k,x)};sort.Strings(k);o:=[]string{};for _,x:=range k{o=append(o,x+"="+strconv.FormatInt(d[x],10))};return strings.Join(o,";"),true}
''',
"retry-plan":r'''package solution
import("regexp";"strconv";"strings")
func RetryPlan(s string)(string,bool){o:=[]string{};for i,x:=range strings.Split(s,","){if !regexp.MustCompile(`^[1-5][0-9]{2}$`).MatchString(x){return "",false};c,_:=strconv.Atoi(x);if c>=200&&c<=299{return strings.Join(o,","),true};if c==408||c==429||c==500||c==502||c==503||c==504{o=append(o,strconv.Itoa(i))}else{return "fatal@"+strconv.Itoa(i),true}};return strings.Join(o,","),true}
''',
"circuit-trace":r'''package solution
import("strconv";"strings")
func CircuitTrace(s string)(string,bool){p:=strings.Split(s,";");if len(p)!=2{return "",false};n,e:=strconv.ParseInt(p[0],10,32);if e!=nil||n<1||strconv.FormatInt(n,10)!=p[0]{return "",false};f:=int64(0);open:=false;var o strings.Builder;for _,c:=range p[1]{if c!='S'&&c!='F'{return "",false};if !open{if c=='S'{f=0}else{f++};open=f>=n};if open{o.WriteByte('O')}else{o.WriteByte('C')}};return o.String(),true}
''',
"bounded-window-rollup":r'''package solution
import("math";"sort";"strconv";"strings")
func BoundedWindowRollup(s string)(string,bool){p:=strings.Split(s,";");if len(p)!=2{return "",false};h:=strings.Split(p[0],",");if len(h)!=3{return "",false};start,e1:=strconv.ParseInt(h[0],10,64);end,e2:=strconv.ParseInt(h[1],10,64);limit,e3:=strconv.ParseInt(h[2],10,32);if e1!=nil||e2!=nil||e3!=nil||strconv.FormatInt(start,10)!=h[0]||strconv.FormatInt(end,10)!=h[1]||strconv.FormatInt(limit,10)!=h[2]||start>end||limit<0{return "",false};type row struct{t,v int64;i int};r:=[]row{};if p[1]!=""{for i,x:=range strings.Split(p[1],","){q:=strings.SplitN(x,"=",2);if len(q)!=2{return "",false};t,x1:=strconv.ParseInt(q[0],10,64);v,x2:=strconv.ParseInt(q[1],10,64);if x1!=nil||x2!=nil||strconv.FormatInt(t,10)!=q[0]||strconv.FormatInt(v,10)!=q[1]{return "",false};if t>=start&&t<end{r=append(r,row{t,v,i})}}};sort.SliceStable(r,func(i,j int)bool{return r[i].t<r[j].t});if int64(len(r))>limit{r=r[len(r)-int(limit):]};if limit==0{r=nil};var sum int64;for _,x:=range r{if x.v>0&&sum>math.MaxInt64-x.v||x.v<0&&sum<math.MinInt64-x.v{return "",false};sum+=x.v};return strconv.Itoa(len(r))+":"+strconv.FormatInt(sum,10),true}
''',
"error-summary":r'''package solution
import("strconv";"strings")
func ErrorSummary(s string)(string,bool){p:=strings.Split(s,",");t:=0;for _,x:=range p{if x=="TIMEOUT"||x=="IO"{t++}else if x!="AUTH"&&x!="BAD_INPUT"{return "",false}};return "permanent="+strconv.Itoa(len(p)-t)+";transient="+strconv.Itoa(t),true}
''',
"tag-patch":r'''package solution
import("regexp";"sort";"strings")
func TagPatch(s string)(string,bool){p:=strings.Split(s,";");if len(p)!=2{return "",false};d:=map[string]string{};key:=regexp.MustCompile(`^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$`);if p[0]!=""{for _,r:=range strings.Split(p[0],","){q:=strings.SplitN(r,"=",2);if len(q)!=2||!key.MatchString(q[0]){return "",false};if _,ok:=d[q[0]];ok{return "",false};d[q[0]]=q[1]}};if p[1]!=""{for _,op:=range strings.Split(p[1],","){if strings.HasPrefix(op,"set:"){q:=strings.SplitN(op[4:],"=",2);if len(q)!=2||!key.MatchString(q[0]){return "",false};d[q[0]]=q[1]}else if strings.HasPrefix(op,"unset:")&&key.MatchString(op[6:]){delete(d,op[6:])}else{return "",false}}};k:=make([]string,0,len(d));for x:=range d{k=append(k,x)};sort.Strings(k);o:=[]string{};for _,x:=range k{o=append(o,x+"="+d[x])};return strings.Join(o,","),true}
''',
"ascii-query-escape":r'''package solution
import "strings"
func AsciiQueryEscape(s string)(string,bool){const hex="0123456789ABCDEF";var o strings.Builder;for _,c:=range []byte(s){if c<32||c>126{return "",false};if c>='A'&&c<='Z'||c>='a'&&c<='z'||c>='0'&&c<='9'||strings.ContainsRune("-._~",rune(c)){o.WriteByte(c)}else{o.WriteByte('%');o.WriteByte(hex[c>>4]);o.WriteByte(hex[c&15])}};return o.String(),true}
''',
"version-compaction":r'''package solution
import("regexp";"sort";"strconv";"strings")
func VersionCompaction(s string)(string,bool){type x struct{v int64;s string};d:=map[string]x{};seen:=map[string]bool{};for _,r:=range strings.Split(s,";"){q:=strings.SplitN(r,"=",2);left:=strings.Split(q[0],":");if len(q)!=2||len(left)!=2||!regexp.MustCompile(`^(?:0|[1-9][0-9]*)$`).MatchString(left[0])||!regexp.MustCompile(`^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$`).MatchString(left[1])||seen[q[0]]{return "",false};seen[q[0]]=true;v,e:=strconv.ParseInt(left[0],10,64);if e!=nil{return "",false};if old,ok:=d[left[1]];!ok||v>old.v{d[left[1]]=x{v,q[1]}}};k:=make([]string,0,len(d));for z:=range d{k=append(k,z)};sort.Strings(k);o:=[]string{};for _,z:=range k{o=append(o,z+"="+d[z].s+"@"+strconv.FormatInt(d[z].v,10))};return strings.Join(o,";"),true}
''',
}

JAVA_ENGINE = r'''import java.util.*;import java.util.regex.*;
public final class Solution{
 static String run(String s,int m){try{
  if(m==0){s=s.replaceAll("^ +| +$","");String[]p=s.split(":",-1);return p.length==3&&p[0].matches("[a-z]+")&&p[1].matches("[a-z0-9]+(?:-[a-z0-9]+)*")&&p[2].matches("0|[1-9][0-9]*")&&Long.parseLong(p[2])>=0?s:null;}
  if(m==1){var o=new ArrayList<String>();var b=new StringBuilder();boolean e=false;for(char c:s.toCharArray()){if(e){if(c!=','&&c!='\\')return null;b.append(c);e=false;}else if(c=='\\')e=true;else if(c==','){o.add(b.toString());b.setLength(0);}else b.append(c);}if(e)return null;o.add(b.toString());return String.join("|",o);}
  if(m==2){var d=new TreeMap<String,Long>();for(String r:s.split(";",-1)){String[]p=r.split("=",-1);if(p.length!=2||!p[0].matches("[a-z0-9]+(?:-[a-z0-9]+)*")||!p[1].matches("0|[1-9][0-9]*"))return null;long v=Long.parseLong(p[1]);d.put(p[0],Math.addExact(d.getOrDefault(p[0],0L),v));}var o=new ArrayList<String>();d.forEach((k,v)->o.add(k+"="+v));return String.join(";",o);}
  if(m==3){var o=new ArrayList<String>();String[]p=s.split(",",-1);for(int i=0;i<p.length;i++){if(!p[i].matches("[1-5][0-9]{2}"))return null;int c=Integer.parseInt(p[i]);if(c>=200&&c<=299)return String.join(",",o);if(c==408||c==429||c==500||c==502||c==503||c==504)o.add(""+i);else return"fatal@"+i;}return String.join(",",o);}
  if(m==4){String[]p=s.split(";",-1);if(p.length!=2||!p[0].matches("[1-9][0-9]*")||!p[1].matches("[SF]*"))return null;int n=Integer.parseInt(p[0]),f=0;boolean open=false;var o=new StringBuilder();for(char c:p[1].toCharArray()){if(!open){f=c=='S'?0:f+1;open=f>=n;}o.append(open?'O':'C');}return o.toString();}
  if(m==5){String[]p=s.split(";",-1),h=p[0].split(",",-1);if(p.length!=2||h.length!=3)return null;long start=Long.parseLong(h[0]),end=Long.parseLong(h[1]);int limit=Integer.parseInt(h[2]);if(!h[0].equals(""+start)||!h[1].equals(""+end)||!h[2].equals(""+limit)||start>end||limit<0)return null;var rows=new ArrayList<long[]>();if(!p[1].isEmpty()){String[]rs=p[1].split(",",-1);for(int i=0;i<rs.length;i++){String[]q=rs[i].split("=",-1);if(q.length!=2)return null;long t=Long.parseLong(q[0]),v=Long.parseLong(q[1]);if(!q[0].equals(""+t)||!q[1].equals(""+v))return null;if(t>=start&&t<end)rows.add(new long[]{t,i,v});}}rows.sort(Comparator.comparingLong(x->x[0]));if(limit==0)rows.clear();else if(rows.size()>limit)rows=new ArrayList<>(rows.subList(rows.size()-limit,rows.size()));long sum=0;for(var x:rows)sum=Math.addExact(sum,x[2]);return rows.size()+":"+sum;}
  if(m==6){String[]p=s.split(",",-1);int t=0;for(String x:p){if(x.equals("TIMEOUT")||x.equals("IO"))t++;else if(!x.equals("AUTH")&&!x.equals("BAD_INPUT"))return null;}return"permanent="+(p.length-t)+";transient="+t;}
  if(m==7){String[]p=s.split(";",-1);if(p.length!=2)return null;var d=new TreeMap<String,String>();if(!p[0].isEmpty())for(String r:p[0].split(",",-1)){String[]q=r.split("=",2);if(q.length!=2||!q[0].matches("[a-z][a-z0-9]*(?:-[a-z0-9]+)*")||d.putIfAbsent(q[0],q[1])!=null)return null;}if(!p[1].isEmpty())for(String op:p[1].split(",",-1)){if(op.startsWith("set:")){String[]q=op.substring(4).split("=",2);if(q.length!=2||!q[0].matches("[a-z][a-z0-9]*(?:-[a-z0-9]+)*"))return null;d.put(q[0],q[1]);}else if(op.startsWith("unset:")&&op.substring(6).matches("[a-z][a-z0-9]*(?:-[a-z0-9]+)*"))d.remove(op.substring(6));else return null;}var o=new ArrayList<String>();d.forEach((k,v)->o.add(k+"="+v));return String.join(",",o);}
  if(m==8){var o=new StringBuilder();for(char c:s.toCharArray()){if(c<32||c>126)return null;if(Character.isLetterOrDigit(c)||"-._~".indexOf(c)>=0)o.append(c);else o.append(String.format("%%%02X",(int)c));}return o.toString();}
  var d=new TreeMap<String,Object[]>();var seen=new HashSet<String>();for(String r:s.split(";",-1)){int eq=r.indexOf('=');if(eq<0)return null;String left=r.substring(0,eq),val=r.substring(eq+1);String[]q=left.split(":",-1);if(q.length!=2||!q[0].matches("0|[1-9][0-9]*")||!q[1].matches("[a-z][a-z0-9]*(?:-[a-z0-9]+)*")||!seen.add(left))return null;long v=Long.parseLong(q[0]);if(!d.containsKey(q[1])||v>(Long)d.get(q[1])[0])d.put(q[1],new Object[]{v,val});}var o=new ArrayList<String>();d.forEach((k,v)->o.add(k+"="+v[1]+"@"+v[0]));return String.join(";",o);
 }catch(Exception e){return null;}}
 %WRAPPER%
}
'''

for _mode, _slug in enumerate(SLUGS):
    _camel="".join([NAMES[_slug].split('_')[0],*[x.title() for x in NAMES[_slug].split('_')[1:]]])
    NATIVE["java"][_slug]=JAVA_ENGINE.replace("%WRAPPER%",f"public static String {_camel}(String input){{return run(input,{_mode});}}")

NATIVE["rust"]={
"api-token-validation":r'''pub fn api_token_validation(input:&str)->Option<String>{let s=input.trim_matches(' ');let p:Vec<_>=s.split(':').collect();if p.len()!=3||p[0].is_empty()||!p[0].bytes().all(|c|c.is_ascii_lowercase())||p[1].split('-').any(|x|x.is_empty()||!x.bytes().all(|c|c.is_ascii_lowercase()||c.is_ascii_digit()))||!(p[2]=="0"||!p[2].starts_with('0')&&!p[2].is_empty()&&p[2].bytes().all(|c|c.is_ascii_digit())){return None}let _:i64=p[2].parse().ok()?;Some(s.into())}
''',
"escaped-field-parser":r'''pub fn escaped_field_parser(input:&str)->Option<String>{let mut o=vec![];let mut b=String::new();let mut e=false;for c in input.chars(){if e{if c!=','&&c!='\\'{return None}b.push(c);e=false}else if c=='\\'{e=true}else if c==','{o.push(b);b=String::new()}else{b.push(c)}}if e{return None}o.push(b);Some(o.join("|"))}
''',
"metric-rollup":r'''use std::collections::BTreeMap;pub fn metric_rollup(input:&str)->Option<String>{let mut d:BTreeMap<&str,i64>=BTreeMap::new();for r in input.split(';'){let(p,v)=r.split_once('=')?;if p.split('-').any(|x|x.is_empty()||!x.bytes().all(|c|c.is_ascii_lowercase()||c.is_ascii_digit()))||!(v=="0"||!v.starts_with('0')&&!v.is_empty()&&v.bytes().all(|c|c.is_ascii_digit())){return None}let n:i64=v.parse().ok()?;let old=d.get(p).copied().unwrap_or(0);d.insert(p,old.checked_add(n)?);}Some(d.into_iter().map(|(k,v)|format!("{}={}",k,v)).collect::<Vec<_>>().join(";"))}
''',
"retry-plan":r'''pub fn retry_plan(input:&str)->Option<String>{let mut o=vec![];for(i,x)in input.split(',').enumerate(){if x.len()!=3||!x.bytes().all(|c|c.is_ascii_digit())||x.as_bytes()[0]<b'1'||x.as_bytes()[0]>b'5'{return None}let c:i32=x.parse().ok()?;if(200..=299).contains(&c){return Some(o.join(","))}if[408,429,500,502,503,504].contains(&c){o.push(i.to_string())}else{return Some(format!("fatal@{}",i))}}Some(o.join(","))}
''',
"circuit-trace":r'''pub fn circuit_trace(input:&str)->Option<String>{let(n,e)=input.split_once(';')?;if n.is_empty()||n.starts_with('0')||!n.bytes().all(|c|c.is_ascii_digit()){return None}let n:i32=n.parse().ok()?;if n<1{return None}let(mut f,mut open,mut o)=(0,false,String::new());for c in e.chars(){if c!='S'&&c!='F'{return None}if !open{if c=='S'{f=0}else{f+=1}open=f>=n}o.push(if open{'O'}else{'C'})}Some(o)}
''',
"bounded-window-rollup":r'''fn sint(s:&str)->Option<i64>{if s=="0"{return Some(0)}let d=s.strip_prefix('-').unwrap_or(s);if d==s&&s.starts_with('+')||d.is_empty()||d.starts_with('0')||!d.bytes().all(|c|c.is_ascii_digit()){return None}s.parse().ok()}pub fn bounded_window_rollup(input:&str)->Option<String>{let(h,b)=input.split_once(';')?;let a:Vec<_>=h.split(',').collect();if a.len()!=3{return None}let start=sint(a[0])?;let end=sint(a[1])?;if !a[2].bytes().all(|c|c.is_ascii_digit())||a[2].is_empty()||(a[2].len()>1&&a[2].starts_with('0')){return None}let limit:i32=a[2].parse().ok()?;if start>end{return None}let mut r=vec![];if !b.is_empty(){for(i,x)in b.split(',').enumerate(){let(t,v)=x.split_once('=')?;let(t,v)=(sint(t)?,sint(v)?);if t>=start&&t<end{r.push((t,i,v))}}}r.sort_by_key(|x|(x.0,x.1));let limit=limit as usize;if limit==0{r.clear()}else if r.len()>limit{r=r.split_off(r.len()-limit)}let sum=r.iter().try_fold(0i64,|q,x|q.checked_add(x.2))?;Some(format!("{}:{}",r.len(),sum))}
''',
"error-summary":r'''pub fn error_summary(input:&str)->Option<String>{let p:Vec<_>=input.split(',').collect();let mut t=0;for x in&p{match*x{"TIMEOUT"|"IO"=>t+=1,"AUTH"|"BAD_INPUT"=>(),_=>return None}}Some(format!("permanent={};transient={}",p.len()-t,t))}
''',
"tag-patch":r'''use std::collections::BTreeMap;fn key(s:&str)->bool{let mut p=s.split('-');p.all(|x|!x.is_empty()&&x.as_bytes()[0].is_ascii_lowercase()&&x.bytes().all(|c|c.is_ascii_lowercase()||c.is_ascii_digit()))}pub fn tag_patch(input:&str)->Option<String>{if input.matches(';').count()!=1{return None}let(base,ops)=input.split_once(';')?;let mut d=BTreeMap::new();if !base.is_empty(){for r in base.split(','){let(k,v)=r.split_once('=')?;if !key(k)||d.insert(k.to_string(),v.to_string()).is_some(){return None}}}if !ops.is_empty(){for op in ops.split(','){if let Some(x)=op.strip_prefix("set:"){let(k,v)=x.split_once('=')?;if !key(k){return None}d.insert(k.into(),v.into());}else if let Some(k)=op.strip_prefix("unset:"){if !key(k){return None}d.remove(k);}else{return None}}}Some(d.into_iter().map(|(k,v)|k+"="+&v).collect::<Vec<_>>().join(","))}
''',
"ascii-query-escape":r'''pub fn ascii_query_escape(input:&str)->Option<String>{let mut o=String::new();for c in input.bytes(){if !(32..=126).contains(&c){return None}if c.is_ascii_alphanumeric()||b"-._~".contains(&c){o.push(c as char)}else{o.push_str(&format!("%{:02X}",c))}}Some(o)}
''',
"version-compaction":r'''use std::collections::{BTreeMap,HashSet};pub fn version_compaction(input:&str)->Option<String>{let mut d:BTreeMap<&str,(i64,&str)>=BTreeMap::new();let mut seen=HashSet::new();for r in input.split(';'){let(left,val)=r.split_once('=')?;let(v,k)=left.split_once(':')?;if !(v=="0"||!v.starts_with('0')&&!v.is_empty()&&v.bytes().all(|c|c.is_ascii_digit()))||k.split('-').any(|x|x.is_empty()||!x.as_bytes()[0].is_ascii_lowercase()||!x.bytes().all(|c|c.is_ascii_lowercase()||c.is_ascii_digit()))||!seen.insert((k,v)){return None}let n:i64=v.parse().ok()?;if d.get(k).is_none_or(|x|n>x.0){d.insert(k,(n,val));}}Some(d.into_iter().map(|(k,(v,x))|format!("{}={}@{}",k,x,v)).collect::<Vec<_>>().join(";"))}
''',
}

def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())

FILE_CONTRACT={"go":"Return solution.go in package solution.","java":"Return Solution.java defining public final class Solution.","javascript":"Return CommonJS module solution.js.","typescript":"Return strict TypeScript module solution.ts.","python":"Return solution.py with the function at module scope.","rust":"Return solution.rs with the public function at module scope."}

CASES = {
"api-token-validation":((" auth:user-2:0 ","auth:user-2:0"),("svc:a9:9223372036854775807","svc:a9:9223372036854775807"),("Auth:user:1",None),("auth:-user:1",None),("auth:user--x:1",None),("auth:user:",None),("auth:user:+1",None),("auth:user:01",None),("auth:user:9223372036854775808",None)),
"escaped-field-parser":((r"a\,b,c\\d,",r"a,b|c\d|"),("x,,y","x||y"),("",""),(r"a\q",None),("tail\\",None),(r"\\,",r"\|")),
"metric-rollup":(("cpu=2;mem=3;cpu=4","cpu=6;mem=3"),("a=0","a=0"),("cpu=01",None),("cpu=-1",None),("cpu=+1",None),("a--b=1",None),("x=9223372036854775807;x=1",None),("=1",None)),
"retry-plan":(("503,429,200,500","0,1"),("200,503",""),("503,404","fatal@1"),("408,504","0,1"),("99",None),("600",None),("503,,200",None),("+503",None)),
"circuit-trace":(("2;FSFFS","CCCOO"),("1;SFS","COO"),("2147483647;",""),("0;F",None),("+2;FF",None),("02;FF",None),("2147483648;F",None),("2;FX",None)),
"bounded-window-rollup":(("3,10,2;8=5,3=2,8=7,10=99","2:12"),("-3,10,2;-3=5,0=-2","2:3"),("3,10,0;4=9","0:0"),("10,3,2;",None),("+3,10,2;",None),("03,10,2;",None),("3,10,2147483648;",None),("-9223372036854775809,0,1;",None),("0,2,2;0=9223372036854775807,1=1",None)),
"error-summary":(("TIMEOUT,AUTH,IO","permanent=1;transient=2"),("AUTH,BAD_INPUT","permanent=2;transient=0"),("TIMEOUT","permanent=0;transient=1"),("AUTH,OTHER",None),("",None),("AUTH,",None)),
"tag-patch":(("a=1,b=2;unset:a,set:b=3,set:c=4","b=3,c=4"),(";set:x=a=b","x=a=b"),("x=a=b;","x=a=b"),("a=1,a=2;",None),("a--b=1;",None),("1a=1;",None),(";set:x--y=1",None),(";unset:",None),(";set:x=a;b",None)),
"ascii-query-escape":(("a b+c","a%20b%2Bc"),("AZaz09-._~","AZaz09-._~"),("%/?","%25%2F%3F"),("",""),("bad\n",None),("café",None)),
"version-compaction":(("2:mode=fast;1:mode=safe;3:zone=west","mode=fast@2;zone=west@3"),("0:a=x=y","a=x=y@0"),("9223372036854775807:a=z","a=z@9223372036854775807"),("1:a=x;1:a=y",None),("01:a=x",None),("+1:a=x",None),("9223372036854775808:a=x",None),("1:a--b=x",None)),
}

def _test(language:str, slug:str, name:str)->tuple[str,str]:
    cases=CASES[slug]
    def qi(value: str) -> str:
        return json.dumps(value, ensure_ascii=language != "rust")
    def q(x: str|None)->str:
        if language in {"go","java","javascript","typescript"}: return json.dumps(x) if x is not None else "null"
        if language=="python": return repr(x)
        return f'Some({json.dumps(x, ensure_ascii=False)}.to_string())' if x is not None else "None"
    if language=="python":
        body=f"from solution import {name} as f\n"+"\n".join(f"assert f({input!r}) == {q(out)}" for input,out in cases)+"\n";return "test_solution.py",body
    if language=="javascript":
        checks="||".join(f"f({qi(i)})!=={q(o)}" for i,o in cases);return "solution.test.js",f"const{{{name}:f}}=require('./solution');if({checks})throw Error('contract');\n"
    if language=="typescript":
        checks="||".join(f"f({qi(i)})!=={q(o)}" for i,o in cases);return "solution.test.ts",f"import{{{name} as f}}from'./solution';if({checks})throw Error('contract');\n"
    if language=="java":
        checks="&&".join(f"java.util.Objects.equals(Solution.{name}({qi(i)}),{q(o)})" for i,o in cases);return "SolutionTest.java",f"public final class SolutionTest{{public static void main(String[]z){{assert {checks};}}}}\n"
    if language=="go":
        checks=[]
        for i,o in cases:
            if o is None: checks.append(f'if _,ok:={name}({qi(i)});ok{{t.Fatal("invalid")}}')
            else: checks.append(f'if g,ok:={name}({qi(i)});!ok||g!={json.dumps(o)}{{t.Fatal(g,ok)}}')
        return "solution_test.go","package solution\nimport \"testing\"\nfunc TestContract(t *testing.T){"+";".join(checks)+"}\n"
    checks="\n".join(f"assert_eq!({name}({qi(i)}),{q(o)});" for i,o in cases);return "solution_test.rs",f"mod solution;use solution::{name};#[test]fn contract(){{{checks}}}\n"

def comparison_fingerprints()->tuple[set[str],set[str],dict[str,int]]:
    exact:set[str]=set(); norm:set[str]=set(); counts={"seed":0,"private_development":0}
    for relative in SEED_PATHS:
        for line in (ROOT/relative).read_text(encoding="utf-8").splitlines():
            text=json.loads(line)["messages"][0]["content"];exact.add(sha256_text(text));norm.add(sha256_text(normalized(text)));counts["seed"]+=1
    for relative in DEVELOPMENT_MANIFESTS:
        manifest=load_json(ROOT/relative); claimed=manifest["manifest_sha256"]
        if sha256_object({k:v for k,v in manifest.items() if k!="manifest_sha256"})!=claimed: raise RuntimeError(f"development manifest hash mismatch: {relative}")
        for entry in manifest["tasks"]:
            task=validate_task(load_json(ROOT/entry["path"]))
            if sha256_object(task)!=entry["sha256"] or task["prompt"]["sha256"]!=entry["prompt_sha256"]: raise RuntimeError(f"development task hash mismatch: {entry['task_id']}")
            text=task["prompt"]["text"];exact.add(sha256_text(text));norm.add(sha256_text(normalized(text)));counts["private_development"]+=1
    if counts!={"seed":1449,"private_development":180}: raise RuntimeError(f"unexpected comparison inventory: {counts}")
    return exact,norm,counts

def make_task(language:str,slug:str,kind:str,mode:int)->dict[str,Any]:
    reference,bad,api,name=_wrapper(language,slug,mode);test_path,test=_test(language,slug,name)
    lead="Implement the following API." if kind=="generation" else "Repair the buggy source below without changing the required API."
    prompt=f"{lead}\n\nFile contract: {FILE_CONTRACT[language]}\nRequired API: {api}\nBehavior: {BEHAVIOR[slug]}\nVisible example: {EXAMPLE[slug]}\n"
    if kind=="repair":prompt+=f"\nBuggy source to repair:\n\n{bad}"
    prompt+="\nReturn only the complete source file; do not include Markdown fences or prose."
    files=[]
    if language=="go":
        mod="module private.invalid/ganesh/decision/tranche1\n\ngo 1.22\n";files.append({"path":"go.mod","role":"support","content":mod,"sha256":sha256_text(mod)})
    files.append({"path":test_path,"role":"test","content":test,"sha256":sha256_text(test)})
    timeout_seconds=60 if language in {"go","java","rust"} else 30
    task={"schema_version":"1.0","task_id":f"decision-t1-{language}-{slug}","surface":"decision","language":language,"family":LANGUAGE_FAMILY[language],"task_type":kind,"prompt":{"text":prompt,"sha256":sha256_text(prompt)},"rendered_prompt":{"text":prompt,"sha256":sha256_text(prompt)},"candidate_path":CANDIDATE_PATH[language],"files":files,"runtime_id":RUNTIME[language],"limits":{"timeout_seconds":timeout_seconds,"memory_mb":512,"cpus":1,"pids":64,"output_bytes":65536},"validation":{"reference":{"label":"author-reference","code":reference,"sha256":sha256_text(reference)},"known_bad":[{"label":"identity-instead-of-contract","code":bad,"sha256":sha256_text(bad)}]}}
    return validate_task(task)

def build()->tuple[dict[str,Any],dict[str,Any]]:
    if any(not NATIVE[l] for l in NATIVE): raise RuntimeError("native reference inventory not installed")
    tasks=[make_task(language,slug,kind,i) for language in RUNTIME for i,(slug,kind) in enumerate(zip(SLUGS,KINDS))]
    exact,norm,counts=comparison_fingerprints()
    exact_hits=[t["task_id"] for t in tasks if t["prompt"]["sha256"] in exact];norm_hits=[t["task_id"] for t in tasks if sha256_text(normalized(t["prompt"]["text"])) in norm]
    own_exact=[t["task_id"] for t in tasks if sum(x["prompt"]["sha256"]==t["prompt"]["sha256"] for x in tasks)>1];own_norm=[t["task_id"] for t in tasks if sum(normalized(x["prompt"]["text"])==normalized(t["prompt"]["text"]) for x in tasks)>1]
    if exact_hits or norm_hits or own_exact or own_norm:raise RuntimeError("decision tranche1 prompt overlap")
    entries=[]
    for task in tasks:
        path=OUT/f"{task['task_id']}.task.json";write_json(path,task);entries.append({"task_id":task["task_id"],"language":task["language"],"task_type":task["task_type"],"path":str(path.relative_to(ROOT)),"sha256":sha256_object(task),"prompt_sha256":task["prompt"]["sha256"],"rendered_prompt_sha256":task["rendered_prompt"]["sha256"]})
    counter=Counter((t["language"],t["task_type"]) for t in tasks)
    manifest={"schema_version":"ganesh-mini-private-eval-manifest/v1","surface":"decision","tranche":"tranche1","status":"authored-unexecuted","task_count":len(tasks),"counts_by_lane":{l:{k:counter[(l,k)] for k in("generation","repair")}for l in RUNTIME},"runtime_config":"configs/eval/runtimes.json","tasks":entries};manifest["manifest_sha256"]=sha256_object(manifest)
    overlap={"schema_version":"ganesh-mini-evaluation-overlap/v1","evaluation_manifest":str(MANIFEST.relative_to(ROOT)),"evaluation_manifest_sha256":manifest["manifest_sha256"],"comparison_inputs":{"seed_jsonl":list(SEED_PATHS),"private_development_manifests":list(DEVELOPMENT_MANIFESTS)},"seed_records_inspected":counts["seed"],"private_development_prompts_inspected":counts["private_development"],"comparison_prompts_inspected":sum(counts.values()),"evaluation_prompts_inspected":len(tasks),"normalization":"NFKC + Unicode casefold + whitespace collapse","exact_prompt_overlaps":exact_hits,"normalized_prompt_overlaps":norm_hits,"within_tranche_exact_overlaps":own_exact,"within_tranche_normalized_overlaps":own_norm,"status":"passed"};overlap["report_sha256"]=sha256_object(overlap)
    write_json(MANIFEST,manifest);write_json(OVERLAP,overlap);return manifest,overlap

if __name__=="__main__":
    m,o=build();print(json.dumps({"tasks":m["task_count"],"manifest_sha256":m["manifest_sha256"],"overlap_sha256":o["report_sha256"]},sort_keys=True))
