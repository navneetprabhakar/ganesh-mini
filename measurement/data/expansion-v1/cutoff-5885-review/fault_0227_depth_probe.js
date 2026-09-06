const { renderFaultTree } = require('./solution');
let node = { code: 'C', note: 'N' };
for (let i = 1; i < 12000; i++) node = { code: 'C', note: 'N', children: [node] };
try {
  const output = renderFaultTree([node]);
  if (output.split('\n').length !== 12000) throw new Error('Incorrect node count');
} catch (error) {
  console.error(error.name + ': ' + error.message);
  process.exitCode = 1;
}
