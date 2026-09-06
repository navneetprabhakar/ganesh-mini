import { redeemVoucher } from './solution';
async function run(): Promise<void> {
  let calls = 0;
  let error: unknown;
  try { await redeemVoucher('ABCDEF\n', '1234', async () => { calls++; return 'receipt'; }); }
  catch (caught) { error = caught; }
  if (!(error instanceof Error) || error.message !== 'Invalid voucher code.' || calls !== 0) {
    throw new Error('trailing newline accepted; verifier calls=' + calls);
  }
}
void run().catch(error => { throw error; });
