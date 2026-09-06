const {viewportProgress}=require('./solution');
const metrics=Object.assign(Object.create({custom:true}),{offset:0,viewportSize:1,contentSize:2});
require('node:assert').throws(()=>viewportProgress(metrics),TypeError);
