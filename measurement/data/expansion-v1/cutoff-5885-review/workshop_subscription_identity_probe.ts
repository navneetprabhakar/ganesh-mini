import {WorkshopToolbar} from './solution';
const t=new WorkshopToolbar(async()=>[],()=>({key:'k',label:'L',room:'r'}),async()=>false,()=>{});
const calls:string[]=[]; const a=()=>{calls.push('a');}; t.subscribe(a);t.subscribe(()=>{calls.push('b');});const removeLast=t.subscribe(a);removeLast();t.emitFilter({text:'',room:null});
if(calls.join(',')!=='a,b') throw new Error('Unsubscribe removed wrong registration: '+calls);
