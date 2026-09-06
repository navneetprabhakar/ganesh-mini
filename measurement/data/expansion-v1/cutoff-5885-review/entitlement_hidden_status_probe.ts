import { EntitlementRegistry, type EntitlementInput } from './solution';
const input: EntitlementInput = {id:'A', product:'P', units:0, intervalSteps:1, intervalCount:1, lastChargedStep:null, status:'enabled'};
Object.defineProperty(input, 'status', {enumerable:false});
if (new EntitlementRegistry([input]).list('enabled').length !== 1) throw new Error('Validated required entitlement status lost');
