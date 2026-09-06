import { ArchiveService, ArchiveRepository } from './solution';
let calls = 0;
const repository: ArchiveRepository = {
  list: async () => [], find: async () => undefined,
  create: async draft => { calls++; return draft; },
  createMany: async drafts => { calls++; return drafts; },
};
async function main(): Promise<void> {
  const service = new ArchiveService(repository);
  const result = await service.create({id: 'a', title: 'valid', rank: 0, tags: new Array<string>(1)});
  if (result.ok || result.reason !== 'invalid' || calls !== 0) {
    throw new Error(`sparse tags accepted or repository called: ${JSON.stringify(result)}, calls=${calls}`);
  }
}
void main();
