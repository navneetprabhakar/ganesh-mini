import { DeliveryPreferenceCoordinator } from './solution';
const calls: string[] = [];
const coordinator = new DeliveryPreferenceCoordinator({ success: m => calls.push('success:' + m), failure: m => calls.push('failure:' + m) });
let rejected = false;
try { coordinator.submit({ maximumFee: 0, carriers: new Array<string>(1) }); }
catch (error) { rejected = error instanceof TypeError && error.message === 'Invalid preferences'; }
if (!rejected) throw new Error('Missing carrier must throw specified TypeError');
if (calls.join() !== 'failure:Invalid preferences' || coordinator.current() !== null) throw new Error('Invalid input must fail atomically');
