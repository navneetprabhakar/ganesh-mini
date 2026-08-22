#!/usr/bin/env python3
"""Build and audit private development tranche 2 deterministically."""

from __future__ import annotations

import json
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.eval.contracts import CANDIDATE_PATH, LANGUAGE_FAMILY, load_json, sha256_object, sha256_text, validate_task, write_json

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "eval/private/development/tranche2"
MANIFEST = ROOT / "manifests/evaluation/private/development-tranche2.json"
OVERLAP = ROOT / "manifests/evaluation/private/development-tranche2-overlap.json"
RUNTIME = {"go":"go-1.22.12","java":"java-21.0.11","javascript":"javascript-node-22.23.2","typescript":"typescript-5.5.4-node-22","python":"python-3.11.15","rust":"rust-1.85.0"}
SLUGS = ("decode-hex","encode-csv-field","parse-netstring","escape-log-fields","parse-quoted-list")
KINDS = {
    "go": ("generation","generation","generation","repair","repair"),
    "java": ("generation","generation","repair","repair","repair"),
    "javascript": ("generation","generation","generation","repair","repair"),
    "typescript": ("generation","generation","repair","repair","repair"),
    "python": ("generation","generation","generation","repair","repair"),
    "rust": ("generation","generation","repair","repair","repair"),
}
FILE_CONTRACT = {
    "go":"Return solution.go using package solution.", "java":"Return Solution.java defining public final class Solution.",
    "javascript":"Return CommonJS module solution.js.", "typescript":"Return solution.ts with named exports.",
    "python":"Return solution.py.", "rust":"Return solution.rs using only the standard library.",
}
API = {
"go":{"decode-hex":"func DecodeHex(text string) ([]byte, bool)","encode-csv-field":"func EncodeCSVField(value string) string","parse-netstring":"func ParseNetstring(text string) (string, bool)","escape-log-fields":"func EscapeLogFields(fields []string) string","parse-quoted-list":"func ParseQuotedList(text string) ([]string, bool)"},
"java":{"decode-hex":"public static byte[] decodeHex(String text), returning null on failure","encode-csv-field":"public static String encodeCsvField(String value)","parse-netstring":"public static String parseNetstring(String text), returning null on failure","escape-log-fields":"public static String escapeLogFields(List<String> fields)","parse-quoted-list":"public static List<String> parseQuotedList(String text), returning null on failure"},
"javascript":{"decode-hex":"exports.decodeHex = function(text), returning an array of byte numbers or null","encode-csv-field":"exports.encodeCsvField = function(value)","parse-netstring":"exports.parseNetstring = function(text), returning a string or null","escape-log-fields":"exports.escapeLogFields = function(fields)","parse-quoted-list":"exports.parseQuotedList = function(text), returning an array or null"},
"typescript":{"decode-hex":"export function decodeHex(text: string): number[] | null","encode-csv-field":"export function encodeCsvField(value: string): string","parse-netstring":"export function parseNetstring(text: string): string | null","escape-log-fields":"export function escapeLogFields(fields: readonly string[]): string","parse-quoted-list":"export function parseQuotedList(text: string): string[] | null"},
"python":{"decode-hex":"def decode_hex(text: str) -> bytes | None","encode-csv-field":"def encode_csv_field(value: str) -> str","parse-netstring":"def parse_netstring(text: str) -> str | None","escape-log-fields":"def escape_log_fields(fields: list[str]) -> str","parse-quoted-list":"def parse_quoted_list(text: str) -> list[str] | None"},
"rust":{"decode-hex":"pub fn decode_hex(text: &str) -> Option<Vec<u8>>","encode-csv-field":"pub fn encode_csv_field(value: &str) -> String","parse-netstring":"pub fn parse_netstring(text: &str) -> Option<String>","escape-log-fields":"pub fn escape_log_fields(fields: &[String]) -> String","parse-quoted-list":"pub fn parse_quoted_list(text: &str) -> Option<Vec<String>>"},
}
BEHAVIOR = {
"decode-hex":"Decode pairs of ASCII hexadecimal digits, accepting upper or lower case. Reject odd length, non-ASCII, or any non-hex digit; empty input succeeds with an empty byte sequence.",
"encode-csv-field":"Serialize one RFC-4180-style field. Return it unchanged unless it contains comma, double quote, CR, or LF; then surround it with double quotes and double every embedded double quote.",
"parse-netstring":"Parse exactly one ASCII netstring length:payload,. The length is decimal bytes with no sign and no leading zero except the single digit 0; payload must be printable ASCII, its byte length must match, and no trailing data is allowed.",
"escape-log-fields":"Serialize fields separated by a literal tab. Inside each field escape backslash as \\\\, tab as \\t, LF as \\n, and CR as \\r, in that precedence. An empty list serializes to the empty string.",
"parse-quoted-list":"Parse a comma-separated list in which every field is double-quoted and an embedded double quote is represented by two consecutive quotes. Preserve empty fields; reject unquoted text, whitespace outside quotes, malformed quoting, or trailing data. Empty input represents an empty list.",
}
EXAMPLE = {
"decode-hex":'"4A00ff" produces bytes [74, 0, 255].',
"encode-csv-field":'The value a,"b becomes "a,""b" (including the surrounding quotes).',
"parse-netstring":'"5:hello," produces "hello", while "05:hello," fails.',
"escape-log-fields":'Fields ["a<TAB>b", "c\\d"] serialize as a\\tb<TAB>c\\\\d, where <TAB> denotes a literal tab.',
"parse-quoted-list":'The text "a","b""c","" produces ["a", "b\\"c", ""].',
}

def spec(reference: str, bad: str, test: str, bad_label: str) -> dict[str,str]:
    return {"reference":reference,"bad":bad,"test":test,"bad_label":bad_label}

LANG: dict[str, dict[str, dict[str,str]]] = {
"go": {
"decode-hex": spec(r'''package solution

func DecodeHex(s string)([]byte,bool){if len(s)%2!=0{return nil,false};out:=make([]byte,len(s)/2);hex:=func(c byte)(byte,bool){switch{case c>='0'&&c<='9':return c-'0',true;case c>='a'&&c<='f':return c-'a'+10,true;case c>='A'&&c<='F':return c-'A'+10,true};return 0,false};for i:=range out{a,ok:=hex(s[2*i]);if !ok{return nil,false};b,ok:=hex(s[2*i+1]);if !ok{return nil,false};out[i]=a*16+b};return out,true}
''',r'''package solution
import "encoding/hex"
func DecodeHex(s string)([]byte,bool){b,_:=hex.DecodeString(s);return b,true}
''',r'''package solution
import("bytes";"testing")
func TestDecodeHex(t *testing.T){g,ok:=DecodeHex("4A00ff");if !ok||!bytes.Equal(g,[]byte{74,0,255}){t.Fatal(g,ok)};g,ok=DecodeHex("");if !ok||g==nil||len(g)!=0{t.Fatal("empty")};for _,x:=range []string{"f","0g","é0"}{if _,ok:=DecodeHex(x);ok{t.Fatal(x)}}}
''',"ignores-decoder-errors"),
"encode-csv-field": spec(r'''package solution
import "strings"
func EncodeCSVField(v string)string{if !strings.ContainsAny(v,",\"\r\n"){return v};return "\""+strings.ReplaceAll(v,"\"","\"\"")+"\""}
''',r'''package solution
import "strings"
func EncodeCSVField(v string)string{if strings.Contains(v,","){return "\""+v+"\""};return v}
''',r'''package solution
import "testing"
func TestCSV(t *testing.T){for _,x:=range[][2]string{{"plain","plain"},{"a,\"b","\"a,\"\"b\""},{"a\nb","\"a\nb\""},{"a\rb","\"a\rb\""},{"\"","\"\"\"\""}}{if g:=EncodeCSVField(x[0]);g!=x[1]{t.Fatalf("%q => %q",x[0],g)}}}
''',"quotes-only-commas"),
"parse-netstring": spec(r'''package solution
import "strconv"
func ParseNetstring(s string)(string,bool){i:=0;for i<len(s)&&s[i]>='0'&&s[i]<='9'{i++};if i==0||i>=len(s)||s[i]!=':'||(i>1&&s[0]=='0'){return "",false};n,e:=strconv.Atoi(s[:i]);if e!=nil||n>len(s)-i-2{return "",false};end:=i+1+n;if end+1!=len(s)||s[end]!=','{return "",false};p:=s[i+1:end];for j:=0;j<len(p);j++{if p[j]<32||p[j]>126{return "",false}};return p,true}
''',r'''package solution
import("strconv";"strings")
func ParseNetstring(s string)(string,bool){p:=strings.SplitN(s,":",2);if len(p)!=2{return "",false};n,_:=strconv.Atoi(p[0]);v:=strings.TrimSuffix(p[1],",");if len(v)<n{return "",false};return v[:n],true}
''',r'''package solution
import "testing"
func TestNet(t *testing.T){for _,x:=range[][2]string{{"5:hello,","hello"},{"0:,",""},{"3:a:b,","a:b"}}{g,ok:=ParseNetstring(x[0]);if !ok||g!=x[1]{t.Fatal(x,g,ok)}};for _,x:=range []string{"05:hello,","5:hell,","5:hello,x","1:\n,","x:a,"}{if _,ok:=ParseNetstring(x);ok{t.Fatal(x)}}}
''',"loose-length-and-trailing-data"),
"escape-log-fields": spec(r'''package solution
import "strings"
func EscapeLogFields(fields []string)string{out:=make([]string,len(fields));for i,v:=range fields{v=strings.ReplaceAll(v,"\\","\\\\");v=strings.ReplaceAll(v,"\t","\\t");v=strings.ReplaceAll(v,"\n","\\n");v=strings.ReplaceAll(v,"\r","\\r");out[i]=v};return strings.Join(out,"\t")}
''',r'''package solution
import "strings"
func EscapeLogFields(fields []string)string{return strings.Join(fields,"\t")}
''',r'''package solution
import "testing"
func TestLog(t *testing.T){if g:=EscapeLogFields([]string{"a\tb","c\\d","x\ny\r"});g!="a\\tb\tc\\\\d\tx\\ny\\r"{t.Fatalf("%q",g)};if EscapeLogFields(nil)!=""{t.Fatal("empty")};if EscapeLogFields([]string{"\\n"})!="\\\\n"{t.Fatal("precedence")}}
''',"joins-without-escaping"),
"parse-quoted-list": spec(r'''package solution
func ParseQuotedList(s string)([]string,bool){if s==""{return []string{},true};out:=[]string{};i:=0;for{if i>=len(s)||s[i]!='"'{return nil,false};i++;cur:=[]byte{};closed:=false;for i<len(s){if s[i]=='"'{if i+1<len(s)&&s[i+1]=='"'{cur=append(cur,'"');i+=2}else{i++;closed=true;break}}else{cur=append(cur,s[i]);i++}};if !closed{return nil,false};out=append(out,string(cur));if i==len(s){return out,true};if s[i]!=','{return nil,false};i++;if i==len(s){return nil,false}}}
''',r'''package solution
import "strings"
func ParseQuotedList(s string)([]string,bool){if s==""{return []string{},true};p:=strings.Split(s,",");for i:=range p{p[i]=strings.Trim(p[i],"\"")};return p,true}
''',r'''package solution
import("reflect";"testing")
func TestQuoted(t *testing.T){for _,x:=range[]struct{s string;w []string}{{"",[]string{}},{"\"a\",\"b\"\"c\",\"\"",[]string{"a","b\"c",""}},{"\"a,b\"",[]string{"a,b"}}}{g,ok:=ParseQuotedList(x.s);if !ok||!reflect.DeepEqual(g,x.w){t.Fatal(x.s,g,ok)}};for _,x:=range []string{"a"," \"a\"","\"a\"x","\"a","\"a\","}{if _,ok:=ParseQuotedList(x);ok{t.Fatal(x)}}}
''',"trim-and-split-parser"),
},
"java": {
"decode-hex": spec(r'''public final class Solution { public static byte[] decodeHex(String s){if((s.length()&1)!=0)return null;byte[]o=new byte[s.length()/2];for(int i=0;i<o.length;i++){int a=Character.digit(s.charAt(2*i),16),b=Character.digit(s.charAt(2*i+1),16);if(a<0||b<0||s.charAt(2*i)>127||s.charAt(2*i+1)>127)return null;o[i]=(byte)(a*16+b);}return o;} }
''',r'''public final class Solution { public static byte[] decodeHex(String s){try{return java.util.HexFormat.of().parseHex(s);}catch(Exception e){return new byte[0];}} }
''',r'''import java.util.*; public final class SolutionTest{public static void main(String[]z){assert Arrays.equals(Solution.decodeHex("4A00ff"),new byte[]{74,0,(byte)255});assert Arrays.equals(Solution.decodeHex(""),new byte[]{});for(String s:new String[]{"f","0g","é0"})assert Solution.decodeHex(s)==null;}}
''',"turns-errors-into-empty"),
"encode-csv-field": spec(r'''public final class Solution { public static String encodeCsvField(String v){if(v.indexOf(',')<0&&v.indexOf('"')<0&&v.indexOf('\r')<0&&v.indexOf('\n')<0)return v;return "\""+v.replace("\"","\"\"")+"\"";} }
''',r'''public final class Solution { public static String encodeCsvField(String v){return v.indexOf(',')>=0?"\""+v+"\"":v;} }
''',r'''public final class SolutionTest{public static void main(String[]z){assert Solution.encodeCsvField("plain").equals("plain");assert Solution.encodeCsvField("a,\"b").equals("\"a,\"\"b\"");assert Solution.encodeCsvField("a\nb").equals("\"a\nb\"");assert Solution.encodeCsvField("a\rb").equals("\"a\rb\"");assert Solution.encodeCsvField("\"").equals("\"\"\"\"");}}
''',"quotes-only-commas"),
"parse-netstring": spec(r'''public final class Solution { public static String parseNetstring(String s){int i=0;while(i<s.length()&&s.charAt(i)>='0'&&s.charAt(i)<='9')i++;if(i==0||i>=s.length()||s.charAt(i)!=':'||(i>1&&s.charAt(0)=='0'))return null;int n;try{n=Integer.parseInt(s.substring(0,i));}catch(Exception e){return null;}int end=i+1+n;if(end+1!=s.length()||end<0||s.charAt(end)!=',')return null;String p=s.substring(i+1,end);for(int j=0;j<p.length();j++)if(p.charAt(j)<32||p.charAt(j)>126)return null;return p;} }
''',r'''public final class Solution { public static String parseNetstring(String s){int c=s.indexOf(':');if(c<0)return null;int n=Integer.parseInt(s.substring(0,c));String p=s.substring(c+1).replace(",","");return p.length()>=n?p.substring(0,n):null;} }
''',r'''public final class SolutionTest{public static void main(String[]z){assert Solution.parseNetstring("5:hello,").equals("hello");assert Solution.parseNetstring("0:,").equals("");assert Solution.parseNetstring("3:a:b,").equals("a:b");for(String s:new String[]{"05:hello,","5:hell,","5:hello,x","1:\n,","x:a,"})assert Solution.parseNetstring(s)==null;}}
''',"loose-length-and-trailing-data"),
"escape-log-fields": spec(r'''import java.util.*; public final class Solution { public static String escapeLogFields(List<String>f){var out=new ArrayList<String>();for(String v:f)out.add(v.replace("\\","\\\\").replace("\t","\\t").replace("\n","\\n").replace("\r","\\r"));return String.join("\t",out);} }
''',r'''import java.util.*; public final class Solution { public static String escapeLogFields(List<String>f){return String.join("\t",f);} }
''',r'''import java.util.*; public final class SolutionTest{public static void main(String[]z){assert Solution.escapeLogFields(List.of("a\tb","c\\d","x\ny\r")).equals("a\\tb\tc\\\\d\tx\\ny\\r");assert Solution.escapeLogFields(List.of()).equals("");assert Solution.escapeLogFields(List.of("\\n")).equals("\\\\n");}}
''',"joins-without-escaping"),
"parse-quoted-list": spec(r'''import java.util.*; public final class Solution { public static List<String> parseQuotedList(String s){var out=new ArrayList<String>();if(s.isEmpty())return out;int i=0;while(true){if(i>=s.length()||s.charAt(i)!='"')return null;i++;var b=new StringBuilder();boolean closed=false;while(i<s.length()){if(s.charAt(i)=='"'){if(i+1<s.length()&&s.charAt(i+1)=='"'){b.append('"');i+=2;}else{i++;closed=true;break;}}else b.append(s.charAt(i++));}if(!closed)return null;out.add(b.toString());if(i==s.length())return out;if(s.charAt(i++)!=','||i==s.length())return null;}} }
''',r'''import java.util.*; public final class Solution { public static List<String> parseQuotedList(String s){if(s.isEmpty())return List.of();var out=new ArrayList<String>();for(String x:s.split(",",-1))out.add(x.replace("\"","").trim());return out;} }
''',r'''import java.util.*; public final class SolutionTest{public static void main(String[]z){assert Solution.parseQuotedList("").equals(List.of());assert Solution.parseQuotedList("\"a\",\"b\"\"c\",\"\"").equals(List.of("a","b\"c",""));assert Solution.parseQuotedList("\"a,b\"").equals(List.of("a,b"));for(String s:new String[]{"a"," \"a\"","\"a\"x","\"a","\"a\","})assert Solution.parseQuotedList(s)==null;}}
''',"strip-and-split-parser"),
},
}

# JS and TS share algorithms, with explicit module/type contracts.
LANG["javascript"] = {
"decode-hex":spec(r'''exports.decodeHex=function(s){if(s.length%2)return null;const o=[];for(let i=0;i<s.length;i+=2){const p=s.slice(i,i+2);if(!/^[0-9A-Fa-f]{2}$/.test(p))return null;o.push(parseInt(p,16))}return o}
''',r'''exports.decodeHex=s=>{const o=[];for(let i=0;i<s.length;i+=2)o.push(parseInt(s.slice(i,i+2),16)||0);return o}
''',r'''const{decodeHex}=require('./solution');const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);if(!eq(decodeHex('4A00ff'),[74,0,255])||!eq(decodeHex(''),[]))throw Error('valid');for(const x of ['f','0g','é0'])if(decodeHex(x)!==null)throw Error(x);
''',"coerces-malformed-to-zero"),
"encode-csv-field":spec(r'''exports.encodeCsvField=function(v){return /[,"\r\n]/.test(v)?'"'+v.replaceAll('"','""')+'"':v}
''',r'''exports.encodeCsvField=v=>v.includes(',')?'"'+v+'"':v
''',r'''const{encodeCsvField:f}=require('./solution');for(const[a,b]of[['plain','plain'],['a,"b','"a,""b"'],['a\nb','"a\nb"'],['a\rb','"a\rb"'],['"','""""']])if(f(a)!==b)throw Error(JSON.stringify([a,f(a)]));
''',"quotes-only-commas"),
"parse-netstring":spec(r'''exports.parseNetstring=function(s){const m=/^(0|[1-9][0-9]*):/.exec(s);if(!m)return null;const n=Number(m[1]),a=m[0].length;if(!Number.isSafeInteger(n)||a+n+1!==s.length||s[a+n]!==',')return null;const p=s.slice(a,a+n);for(const c of p)if(c.charCodeAt(0)<32||c.charCodeAt(0)>126)return null;return p}
''',r'''exports.parseNetstring=function(s){const c=s.indexOf(':');if(c<0)return null;const n=parseInt(s);return s.slice(c+1,c+1+n)}
''',r'''const{parseNetstring:f}=require('./solution');for(const[a,b]of[['5:hello,','hello'],['0:,',''],['3:a:b,','a:b']])if(f(a)!==b)throw Error(a);for(const x of ['05:hello,','5:hell,','5:hello,x','1:\n,','x:a,'])if(f(x)!==null)throw Error(x);
''',"ignores-framing-contract"),
"escape-log-fields":spec(r'''exports.escapeLogFields=fields=>fields.map(v=>v.replaceAll('\\','\\\\').replaceAll('\t','\\t').replaceAll('\n','\\n').replaceAll('\r','\\r')).join('\t')
''',r'''exports.escapeLogFields=fields=>fields.join('\t')
''',r'''const{escapeLogFields:f}=require('./solution');if(f(['a\tb','c\\d','x\ny\r'])!=='a\\tb\tc\\\\d\tx\\ny\\r'||f([])!==''||f(['\\n'])!=='\\\\n')throw Error('escape');
''',"joins-without-escaping"),
"parse-quoted-list":spec(r'''exports.parseQuotedList=function(s){if(s==='')return[];const o=[];let i=0;while(true){if(s[i]!=='"')return null;i++;let v='',closed=false;while(i<s.length){if(s[i]==='"'){if(s[i+1]==='"'){v+='"';i+=2}else{i++;closed=true;break}}else v+=s[i++]}if(!closed)return null;o.push(v);if(i===s.length)return o;if(s[i++]!==','||i===s.length)return null}}
''',r'''exports.parseQuotedList=s=>s===''?[]:s.split(',').map(x=>x.replaceAll('"','').trim())
''',r'''const{parseQuotedList:f}=require('./solution');const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);if(!eq(f(''),[])||!eq(f('"a","b""c",""'),['a','b"c',''])||!eq(f('"a,b"'),['a,b']))throw Error('valid');for(const x of ['a',' "a"','"a"x','"a','"a",'])if(f(x)!==null)throw Error(x);
''',"strip-and-split-parser"),
}
LANG["typescript"] = {
"decode-hex":spec(r'''export function decodeHex(s:string):number[]|null{if(s.length%2)return null;const o:number[]=[];for(let i=0;i<s.length;i+=2){const p=s.slice(i,i+2);if(!/^[0-9A-Fa-f]{2}$/.test(p))return null;o.push(parseInt(p,16))}return o}
''',r'''export const decodeHex=(s:string):number[]=>{const o:number[]=[];for(let i=0;i<s.length;i+=2)o.push(parseInt(s.slice(i,i+2),16)||0);return o}
''',r'''import{decodeHex}from'./solution';const eq=(a:unknown,b:unknown)=>JSON.stringify(a)===JSON.stringify(b);if(!eq(decodeHex('4A00ff'),[74,0,255])||!eq(decodeHex(''),[]))throw Error('valid');for(const x of ['f','0g','é0'])if(decodeHex(x)!==null)throw Error(x);
''',"coerces-malformed-to-zero"),
"encode-csv-field":spec(r'''export function encodeCsvField(v:string):string{return /[,"\r\n]/.test(v)?'"'+v.replaceAll('"','""')+'"':v}
''',r'''export const encodeCsvField=(v:string):string=>v.includes(',')?'"'+v+'"':v
''',r'''import{encodeCsvField as f}from'./solution';for(const[a,b]of[['plain','plain'],['a,"b','"a,""b"'],['a\nb','"a\nb"'],['a\rb','"a\rb"'],['"','""""']])if(f(a)!==b)throw Error(JSON.stringify([a,f(a)]));
''',"quotes-only-commas"),
"parse-netstring":spec(r'''export function parseNetstring(s:string):string|null{const m=/^(0|[1-9][0-9]*):/.exec(s);if(!m)return null;const n=Number(m[1]),a=m[0].length;if(!Number.isSafeInteger(n)||a+n+1!==s.length||s[a+n]!==',')return null;const p=s.slice(a,a+n);for(const c of p)if(c.charCodeAt(0)<32||c.charCodeAt(0)>126)return null;return p}
''',r'''export function parseNetstring(s:string):string|null{const c=s.indexOf(':');if(c<0)return null;const n=parseInt(s);return s.slice(c+1,c+1+n)}
''',r'''import{parseNetstring as f}from'./solution';for(const[a,b]of[['5:hello,','hello'],['0:,',''],['3:a:b,','a:b']])if(f(a)!==b)throw Error(a);for(const x of ['05:hello,','5:hell,','5:hello,x','1:\n,','x:a,'])if(f(x)!==null)throw Error(x);
''',"ignores-framing-contract"),
"escape-log-fields":spec(r'''export const escapeLogFields=(fields:readonly string[]):string=>fields.map(v=>v.replaceAll('\\','\\\\').replaceAll('\t','\\t').replaceAll('\n','\\n').replaceAll('\r','\\r')).join('\t')
''',r'''export const escapeLogFields=(fields:readonly string[]):string=>fields.join('\t')
''',r'''import{escapeLogFields as f}from'./solution';if(f(['a\tb','c\\d','x\ny\r'])!=='a\\tb\tc\\\\d\tx\\ny\\r'||f([])!==''||f(['\\n'])!=='\\\\n')throw Error('escape');
''',"joins-without-escaping"),
"parse-quoted-list":spec(r'''export function parseQuotedList(s:string):string[]|null{if(s==='')return[];const o:string[]=[];let i=0;while(true){if(s[i]!=='"')return null;i++;let v='',closed=false;while(i<s.length){if(s[i]==='"'){if(s[i+1]==='"'){v+='"';i+=2}else{i++;closed=true;break}}else v+=s[i++]}if(!closed)return null;o.push(v);if(i===s.length)return o;if(s[i++]!==','||i===s.length)return null}}
''',r'''export const parseQuotedList=(s:string):string[]=>s===''?[]:s.split(',').map(x=>x.replaceAll('"','').trim())
''',r'''import{parseQuotedList as f}from'./solution';const eq=(a:unknown,b:unknown)=>JSON.stringify(a)===JSON.stringify(b);if(!eq(f(''),[])||!eq(f('"a","b""c",""'),['a','b"c',''])||!eq(f('"a,b"'),['a,b']))throw Error('valid');for(const x of ['a',' "a"','"a"x','"a','"a",'])if(f(x)!==null)throw Error(x);
''',"strip-and-split-parser"),
}

LANG["python"]={
"decode-hex":spec("def decode_hex(text: str) -> bytes | None:\n    if len(text)%2: return None\n    if any(ord(c)>127 or c not in '0123456789abcdefABCDEF' for c in text): return None\n    return bytes(int(text[i:i+2],16) for i in range(0,len(text),2))\n","def decode_hex(text: str) -> bytes | None:\n    try: return bytes.fromhex(text)\n    except ValueError: return b''\n","from solution import decode_hex\nassert decode_hex('4A00ff')==bytes([74,0,255])\nassert decode_hex('')==b''\nfor x in ['f','0g','é0']: assert decode_hex(x) is None\n","turns-errors-into-empty"),
"encode-csv-field":spec("def encode_csv_field(value: str) -> str:\n    return '\"'+value.replace('\"','\"\"')+'\"' if any(c in value for c in ',\"\\r\\n') else value\n","def encode_csv_field(value: str) -> str:\n    return '\"'+value+'\"' if ',' in value else value\n","from solution import encode_csv_field as f\nfor a,b in [('plain','plain'),('a,\"b','\"a,\"\"b\"'),('a\\nb','\"a\\nb\"'),('a\\rb','\"a\\rb\"'),('\"','\"\"\"\"')]: assert f(a)==b,(a,f(a))\n","quotes-only-commas"),
"parse-netstring":spec("def parse_netstring(text: str) -> str | None:\n    p=text.find(':')\n    if p<1 or not text[:p].isascii() or not text[:p].isdigit() or (p>1 and text[0]=='0'): return None\n    n=int(text[:p]); end=p+1+n\n    if end+1!=len(text) or text[end]!=',': return None\n    value=text[p+1:end]\n    return value if all(32<=ord(c)<=126 for c in value) else None\n","def parse_netstring(text: str) -> str | None:\n    p=text.find(':')\n    if p<0: return None\n    n=int(text[:p]); return text[p+1:p+1+n]\n","from solution import parse_netstring as f\nfor a,b in [('5:hello,','hello'),('0:,',''),('3:a:b,','a:b')]: assert f(a)==b\nfor x in ['05:hello,','5:hell,','5:hello,x','1:\\n,','x:a,']: assert f(x) is None,x\n","ignores-framing-contract"),
"escape-log-fields":spec("def escape_log_fields(fields: list[str]) -> str:\n    return '\\t'.join(v.replace('\\\\','\\\\\\\\').replace('\\t','\\\\t').replace('\\n','\\\\n').replace('\\r','\\\\r') for v in fields)\n","def escape_log_fields(fields: list[str]) -> str:\n    return '\\t'.join(fields)\n","from solution import escape_log_fields as f\nassert f(['a\\tb','c\\\\d','x\\ny\\r'])=='a\\\\tb\\tc\\\\\\\\d\\tx\\\\ny\\\\r'\nassert f([])=='' and f(['\\\\n'])=='\\\\\\\\n'\n","joins-without-escaping"),
"parse-quoted-list":spec(r'''def parse_quoted_list(text: str) -> list[str] | None:
    if text=='': return []
    out=[]; i=0
    while True:
        if i>=len(text) or text[i]!='"': return None
        i+=1; cur=[]; closed=False
        while i<len(text):
            if text[i]=='"':
                if i+1<len(text) and text[i+1]=='"': cur.append('"'); i+=2
                else: i+=1; closed=True; break
            else: cur.append(text[i]); i+=1
        if not closed: return None
        out.append(''.join(cur))
        if i==len(text): return out
        if text[i]!=',' or i+1==len(text): return None
        i+=1
''',r'''def parse_quoted_list(text: str) -> list[str] | None:
    if not text: return []
    return [x.strip().replace('"','') for x in text.split(',')]
''',r'''from solution import parse_quoted_list as f
assert f('')==[] and f('"a","b""c",""')==['a','b"c',''] and f('"a,b"')==['a,b']
for x in ['a',' "a"','"a"x','"a','"a",']: assert f(x) is None,x
''',"strip-and-split-parser"),
}

LANG["rust"]={
"decode-hex":spec(r'''pub fn decode_hex(s:&str)->Option<Vec<u8>>{if s.len()%2!=0||!s.is_ascii(){return None}fn h(c:u8)->Option<u8>{match c{b'0'..=b'9'=>Some(c-b'0'),b'a'..=b'f'=>Some(c-b'a'+10),b'A'..=b'F'=>Some(c-b'A'+10),_=>None}}let b=s.as_bytes();(0..b.len()).step_by(2).map(|i|Some(h(b[i])?*16+h(b[i+1])?)).collect()}
''',r'''pub fn decode_hex(s:&str)->Option<Vec<u8>>{Some(s.as_bytes().chunks(2).map(|x|u8::from_str_radix(std::str::from_utf8(x).unwrap_or("0"),16).unwrap_or(0)).collect())}
''',r'''mod solution{include!("solution.rs");}use solution::*;#[test]fn cases(){assert_eq!(decode_hex("4A00ff"),Some(vec![74,0,255]));assert_eq!(decode_hex(""),Some(vec![]));for x in ["f","0g","é0"]{assert_eq!(decode_hex(x),None)}}
''',"coerces-malformed-to-zero"),
"encode-csv-field":spec(r'''pub fn encode_csv_field(v:&str)->String{if v.contains([',','"','\r','\n']){format!("\"{}\"",v.replace('"',"\"\""))}else{v.to_string()}}
''',r'''pub fn encode_csv_field(v:&str)->String{if v.contains(','){format!("\"{}\"",v)}else{v.to_string()}}
''',r'''mod solution{include!("solution.rs");}use solution::*;#[test]fn cases(){for(a,b)in [("plain","plain"),("a,\"b","\"a,\"\"b\""),("a\nb","\"a\nb\""),("a\rb","\"a\rb\""),("\"","\"\"\"\"")]{assert_eq!(encode_csv_field(a),b)}}
''',"quotes-only-commas"),
"parse-netstring":spec(r'''pub fn parse_netstring(s:&str)->Option<String>{let c=s.find(':')?;let ntext=&s[..c];if ntext.is_empty()||(ntext.len()>1&&ntext.starts_with('0'))||!ntext.bytes().all(|b|b.is_ascii_digit()){return None}let n:usize=ntext.parse().ok()?;let end=c.checked_add(1)?.checked_add(n)?;if end+1!=s.len()||s.as_bytes().get(end)!=Some(&b','){return None}let p=&s[c+1..end];if !p.bytes().all(|b|(32..=126).contains(&b)){return None}Some(p.to_string())}
''',r'''pub fn parse_netstring(s:&str)->Option<String>{let c=s.find(':')?;let n:usize=s[..c].parse().ok()?;Some(s[c+1..].chars().take(n).collect())}
''',r'''mod solution{include!("solution.rs");}use solution::*;#[test]fn cases(){for(a,b)in [("5:hello,","hello"),("0:,",""),("3:a:b,","a:b")]{assert_eq!(parse_netstring(a),Some(b.into()))}for x in ["05:hello,","5:hell,","5:hello,x","1:\n,","x:a,"]{assert_eq!(parse_netstring(x),None)}}
''',"ignores-framing-contract"),
"escape-log-fields":spec(r'''pub fn escape_log_fields(fields:&[String])->String{fields.iter().map(|v|v.replace('\\',"\\\\").replace('\t',"\\t").replace('\n',"\\n").replace('\r',"\\r")).collect::<Vec<_>>().join("\t")}
''',r'''pub fn escape_log_fields(fields:&[String])->String{fields.join("\t")}
''',r'''mod solution{include!("solution.rs");}use solution::*;#[test]fn cases(){let v=vec!["a\tb".into(),"c\\d".into(),"x\ny\r".into()];assert_eq!(escape_log_fields(&v),"a\\tb\tc\\\\d\tx\\ny\\r");assert_eq!(escape_log_fields(&[]),"");assert_eq!(escape_log_fields(&["\\n".into()]),"\\\\n")}
''',"joins-without-escaping"),
"parse-quoted-list":spec(r'''pub fn parse_quoted_list(s:&str)->Option<Vec<String>>{if s.is_empty(){return Some(vec![])}let b=s.as_bytes();let mut i=0;let mut out=vec![];loop{if b.get(i)!=Some(&b'"'){return None}i+=1;let mut v=String::new();let mut closed=false;while i<b.len(){if b[i]==b'"'{if b.get(i+1)==Some(&b'"'){v.push('"');i+=2}else{i+=1;closed=true;break}}else{v.push(b[i]as char);i+=1}}if !closed{return None}out.push(v);if i==b.len(){return Some(out)}if b.get(i)!=Some(&b',')||i+1==b.len(){return None}i+=1}}
''',r'''pub fn parse_quoted_list(s:&str)->Option<Vec<String>>{if s.is_empty(){return Some(vec![])}Some(s.split(',').map(|x|x.trim().replace('"',"")).collect())}
''',r'''mod solution{include!("solution.rs");}use solution::*;#[test]fn cases(){assert_eq!(parse_quoted_list(""),Some(vec![]));assert_eq!(parse_quoted_list("\"a\",\"b\"\"c\",\"\""),Some(vec!["a".into(),"b\"c".into(),"".into()]));assert_eq!(parse_quoted_list("\"a,b\""),Some(vec!["a,b".into()]));for x in ["a"," \"a\"","\"a\"x","\"a","\"a\","]{assert_eq!(parse_quoted_list(x),None)}}
''',"strip-and-split-parser"),
}

def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC",text).casefold().split())

def make_task(language: str, slug: str, kind: str) -> dict[str,Any]:
    item=LANG[language][slug]
    lead="Implement the following API." if kind=="generation" else "Repair the buggy source below without changing the required API."
    prompt=f"{lead}\n\nFile contract: {FILE_CONTRACT[language]}\nRequired API: {API[language][slug]}\nBehavior: {BEHAVIOR[slug]}\nVisible example: {EXAMPLE[slug]}\n"
    if kind=="repair": prompt+=f"\nBuggy source to repair:\n\n{item['bad']}"
    prompt+="\nReturn only the complete source file; do not include Markdown fences or prose."
    files=[]
    if language=="go":
        module="module private.invalid/ganesh/development/tranche2\n\ngo 1.22\n";files.append({"path":"go.mod","role":"support","content":module,"sha256":sha256_text(module)})
    test_path={"go":"solution_test.go","java":"SolutionTest.java","javascript":"solution.test.js","typescript":"solution.test.ts","python":"test_solution.py","rust":"solution_test.rs"}[language]
    files.append({"path":test_path,"role":"test","content":item["test"],"sha256":sha256_text(item["test"])})
    return validate_task({"schema_version":"1.0","task_id":f"dev-t2-{language}-{slug}","surface":"development","language":language,"family":LANGUAGE_FAMILY[language],"task_type":kind,"prompt":{"text":prompt,"sha256":sha256_text(prompt)},"rendered_prompt":{"text":prompt,"sha256":sha256_text(prompt)},"candidate_path":CANDIDATE_PATH[language],"files":files,"runtime_id":RUNTIME[language],"limits":{"timeout_seconds":30,"memory_mb":512,"cpus":1,"pids":64,"output_bytes":65536},"validation":{"reference":{"label":"author-reference","code":item["reference"],"sha256":sha256_text(item["reference"])},"known_bad":[{"label":item["bad_label"],"code":item["bad"],"sha256":sha256_text(item["bad"])}]}})

def all_evaluation_fingerprints() -> tuple[set[str],set[str],int,list[str]]:
    exact:set[str]=set();norm:set[str]=set();count=0;sources=[]
    seed_exact,seed_norm,seed_count=set(),set(),0
    for relative in ("data/seed/ganesh_v01/train.jsonl","data/seed/ganesh_v01/validation.jsonl"):
        for line in (ROOT/relative).read_text(encoding="utf-8").splitlines():
            text=json.loads(line)["messages"][0]["content"];seed_exact.add(sha256_text(text));seed_norm.add(sha256_text(normalized(text)));seed_count+=1
    exact|=seed_exact;norm|=seed_norm;count+=seed_count;sources.append("manifests/datasets/ganesh_v01_seed.json")
    for path in sorted((ROOT/"manifests/evaluation/private").glob("development-tranche*.json")):
        if path==MANIFEST or path.name.endswith(("-overlap.json","-directionality.json")):continue
        manifest=load_json(path)
        for entry in manifest.get("tasks",[]):
            task=load_json(ROOT/entry["path"]);text=task["prompt"]["text"];exact.add(sha256_text(text));norm.add(sha256_text(normalized(text)));count+=1
        sources.append(str(path.relative_to(ROOT)))
    return exact,norm,count,sources

def build()->tuple[dict[str,Any],dict[str,Any]]:
    OUT.mkdir(parents=True,exist_ok=True);tasks=[]
    for language,kinds in KINDS.items():tasks.extend(make_task(language,slug,kind) for slug,kind in zip(SLUGS,kinds))
    exact,norm,inspected,sources=all_evaluation_fingerprints()
    exact_hits=[t["task_id"] for t in tasks if t["prompt"]["sha256"] in exact];norm_hits=[t["task_id"] for t in tasks if sha256_text(normalized(t["prompt"]["text"])) in norm]
    own_exact=[t["task_id"] for i,t in enumerate(tasks) if t["prompt"]["sha256"] in {x["prompt"]["sha256"] for x in tasks[:i]}]
    own_norm=[t["task_id"] for i,t in enumerate(tasks) if sha256_text(normalized(t["prompt"]["text"])) in {sha256_text(normalized(x["prompt"]["text"])) for x in tasks[:i]}]
    if exact_hits or norm_hits or own_exact or own_norm:raise RuntimeError("private prompt overlap detected")
    entries=[]
    for task in tasks:
        path=OUT/f"{task['task_id']}.task.json";write_json(path,task);entries.append({"task_id":task["task_id"],"language":task["language"],"task_type":task["task_type"],"path":str(path.relative_to(ROOT)),"sha256":sha256_object(task),"prompt_sha256":task["prompt"]["sha256"],"rendered_prompt_sha256":task["rendered_prompt"]["sha256"]})
    counts=Counter((t["language"],t["task_type"]) for t in tasks)
    manifest={"schema_version":"ganesh-mini-private-eval-manifest/v1","surface":"development","tranche":"tranche2","status":"authored","task_count":len(tasks),"counts_by_lane":{l:{k:counts[(l,k)] for k in ("generation","repair")} for l in RUNTIME},"runtime_config":"configs/eval/runtimes.json","tasks":entries};manifest["manifest_sha256"]=sha256_object(manifest)
    overlap={"schema_version":"ganesh-mini-evaluation-overlap/v1","evaluation_manifest":str(MANIFEST.relative_to(ROOT)),"evaluation_manifest_sha256":manifest["manifest_sha256"],"comparison_sources":sources,"records_and_prompts_inspected":inspected,"seed_records_inspected":1449,"evaluation_prompts_inspected":len(tasks),"normalization":"NFKC + Unicode casefold + whitespace collapse","exact_prompt_overlaps":exact_hits+own_exact,"normalized_prompt_overlaps":norm_hits+own_norm,"status":"passed"};overlap["report_sha256"]=sha256_object(overlap)
    write_json(MANIFEST,manifest);write_json(OVERLAP,overlap);return manifest,overlap

if __name__=="__main__":
    m,o=build();print(json.dumps({"tasks":m["task_count"],"manifest_sha256":m["manifest_sha256"],"overlap_sha256":o["report_sha256"]},sort_keys=True))
