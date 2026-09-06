import { AllowListPolicy } from './solution';
let rejected = false;
try { new AllowListPolicy(new Array<string>(1)); }
catch (error) { if (error instanceof TypeError) rejected = true; else throw error; }
if (!rejected) throw new Error('sparse allow-list accepted');
