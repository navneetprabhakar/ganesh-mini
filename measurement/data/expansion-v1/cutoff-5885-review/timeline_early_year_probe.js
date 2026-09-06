const assert = require('node:assert/strict');
const { buildTimeline } = require('./solution');
const entry = {id:'a',date:'0099-01-01',time:'00:00',text:'',city:'',image:null};
assert.deepEqual(buildTimeline([entry], null), [entry]);
