import { LabelCounter } from './solution';
async function main() {
  const result = await new LabelCounter({read:async () => new Array(1)}).count();
  if (result.ok || result.message !== 'Invalid label data') throw new Error('Missing provider label must be invalid');
}
main().catch(error => { throw error; });
