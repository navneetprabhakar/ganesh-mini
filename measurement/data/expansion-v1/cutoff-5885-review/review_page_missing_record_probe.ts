import { ReviewRecord, buildReviewPage } from './solution';
let caught: unknown;
try { buildReviewPage('reviewer', new Array<ReviewRecord>(1)); } catch (error) { caught = error; }
if (!(caught instanceof TypeError)) throw new Error('Missing review record must not bypass validation');
