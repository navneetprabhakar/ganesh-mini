import {LoanLedger,type Equipment} from './solution';
const equipment:Equipment={code:'e',name:'E'}; Object.defineProperty(equipment,'code',{enumerable:false});
const loan=new LoanLedger().createLoan(equipment,{id:'b',name:'B'},{id:'c',name:'C'});
if(loan.equipment.code!=='e') throw new Error('Required equipment code lost');
