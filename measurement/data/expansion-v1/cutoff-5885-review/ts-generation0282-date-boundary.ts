import { ReadingPlan, ReadingState } from './solution';

for (const suffix of ['\n', '\r', '\r\n', '\u2028', '\u2029']) {
  const plan = new ReadingPlan();
  let rejected = false;
  try { plan.add('Title', '', ReadingState.QUEUED, '2026-09-07' + suffix); }
  catch (error) { if (!(error instanceof TypeError)) throw error; rejected = true; }
  if (!rejected) throw new Error('date accepted forbidden suffix ' + JSON.stringify(suffix));
  if (plan.add('Title', '', ReadingState.QUEUED, '2026-09-07').id !== 1) throw new Error('invalid date consumed ID');
}
