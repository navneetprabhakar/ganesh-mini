import { Initiative, createInitiativeSnapshot } from './solution';
const initiative: Initiative = { id: 1, name: 'One' };
Object.defineProperty(initiative, 'name', { value: 'One', enumerable: false });
if (createInitiativeSnapshot(1, [initiative], []).initiative.name !== 'One') throw new Error('Required initiative name must survive copying');
