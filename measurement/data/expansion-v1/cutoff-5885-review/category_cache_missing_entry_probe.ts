import {CategoryCache,type ShelfCategory} from './solution';
async function main(){const c=new CategoryCache(async()=>new Array<ShelfCategory>(1),0);let rejected=false;try{await c.refresh(0);}catch(e){if(!(e instanceof TypeError))throw e;rejected=true;}if(!rejected)throw new Error('Missing category accepted');}
main().catch(e=>{throw e;});
