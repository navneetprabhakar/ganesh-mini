const {createInventory}=require('./solution');
const stock=createInventory(JSON.parse('{"__proto__":3}')).snapshot().stock;
require('node:assert').strictEqual(Object.prototype.hasOwnProperty.call(stock,'__proto__'),true);
require('node:assert').strictEqual(stock.__proto__,3);
