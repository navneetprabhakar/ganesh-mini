import { verifyAccount } from './solution';
async function run(): Promise<void> {
  try {
    await verifyAccount([{ id: 'id', name: 'Name', email: '', secret: '', image: '' }], '', '');
  } catch (error) {
    if (error instanceof Error && error.message === 'Verification failed') return;
    throw error;
  }
  throw new Error('Empty credentials matched stored empty strings instead of rejecting');
}
run().catch(error => { throw error; });
