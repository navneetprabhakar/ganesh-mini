import { buildCasePanel } from './solution';
let caught: unknown;
try { buildCasePanel({ title: 'T', bannerUrl: 'b', customer: 'C', category: 'x', completedOn: 'd', paragraphs: new Array<string>(1), attachments: [] }, true); } catch (error) { caught = error; }
if (!(caught instanceof RangeError)) throw new Error('Malformed visible paragraph must throw RangeError');
