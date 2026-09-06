import { LabSubmissionStore, EMPTY_LAB_SUBMISSION } from './solution';
async function main(): Promise<void> {
  const store = new LabSubmissionStore([EMPTY_LAB_SUBMISSION]);
  if (await store.findById('') !== undefined) throw new Error('empty ID must be not found even when supplied to constructor');
}
main().catch(error => { throw error; });
