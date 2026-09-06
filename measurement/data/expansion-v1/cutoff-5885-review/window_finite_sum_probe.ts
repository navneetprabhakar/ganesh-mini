import { visibleWindow } from './solution';
const m = Number.MAX_VALUE;
const result = visibleWindow({totalRows: 10, rowHeight: m, scrollTop: m, viewportHeight: m, overscan: 0});
// All accepted dimensions are finite integers. One full row is visible:
// start = m/m = 1; end = (m+m)/m = 2, without intermediate overflow.
if (result.start !== 1 || result.endExclusive !== 2) throw new Error(`finite dimensions produced ${JSON.stringify(result)}`);
