import {mergeSettings,type Settings} from './solution';
let value:Settings = {leaf:1};
for(let i=0;i<12000;i++) value = {nested:value};
try {mergeSettings([value]);}
catch(error) {
  console.log(error instanceof Error ? error.name+': '+error.message : String(error));
  throw new Error('finite acyclic settings failed');
}
