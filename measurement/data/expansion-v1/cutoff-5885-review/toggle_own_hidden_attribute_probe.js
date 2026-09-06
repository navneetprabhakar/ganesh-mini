const buildToggleDescriptor=require('./solution');
const attributes={};Object.defineProperty(attributes,'data-count',{value:3,enumerable:false});
require('node:assert').strictEqual(buildToggleDescriptor({label:'x',attributes}).props['data-count'],3);
