const { tracePlan } = require('./solution');
let node = { label: 'x', children: [] };
for (let i = 1; i < 12000; i++) node = { label: 'x', children: [node] };
try {
  if (tracePlan([node]).length !== 12000) throw new Error('Incorrect node count');
} catch (error) { console.error(error.name + ': ' + error.message); process.exitCode = 1; }
