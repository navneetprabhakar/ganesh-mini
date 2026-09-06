import { SlotRegistry } from './solution';
const registry = new SlotRegistry<number>();
registry.attachAll(new Map([['', 1]]));
if (registry.snapshot().has('')) throw new Error('blank slot admitted by attachAll; global nonblank invariant scope requires disposition');
