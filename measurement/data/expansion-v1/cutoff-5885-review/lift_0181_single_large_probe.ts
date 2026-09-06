import { LiftShaft } from './solution';
const floor = Number.MAX_SAFE_INTEGER + 1;
const lift = new LiftShaft(floor, floor);
lift.install();
if (lift.advance() !== false) throw new Error('One-floor shaft reports successful movement at finite integer bound');
