const {createArchive}=require('./solution');
const archive=createArchive();archive.createDocument({id:'d',title:'D'});
const changes={};Object.defineProperty(changes,'id',{value:'other',enumerable:false});
require('node:assert').throws(() => archive.updateDocument('d',changes),{name:'TypeError',message:'Invalid changes'});
