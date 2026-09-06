import {flattenOutline, type OutlineNode} from './solution';
let node: OutlineNode = {id:'n0',label:'leaf'};
for (let i=1;i<12000;i++) node = {id:'n'+i,label:'node',children:[node]};
try {
  const rows = flattenOutline([node],new Set<string>(),'p');
  if(rows.length !== 1) throw new Error('expected one closed root');
} catch(error) {
  console.log(error instanceof Error ? error.name+': '+error.message : String(error));
  throw new Error('valid finite outline failed');
}
