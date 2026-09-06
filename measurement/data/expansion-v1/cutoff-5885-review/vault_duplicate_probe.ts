import { FixedScaleVault } from './solution';
const vault = new FixedScaleVault(0, 'T');
const calls: string[] = [];
const a = () => { calls.push('a'); };
vault.subscribe('account', a);
vault.subscribe('account', () => { calls.push('b'); });
const removeLast = vault.subscribe('account', a);
calls.length = 0; // Discard required immediate notifications.
removeLast();
removeLast();
vault.setBalance('account', 1n);
if (calls.join(',') !== 'a,b') throw new Error(`last unsubscribe removed wrong registration: ${calls}`);
