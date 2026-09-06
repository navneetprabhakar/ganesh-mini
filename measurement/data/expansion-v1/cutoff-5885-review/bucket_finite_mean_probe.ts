import { averageBuckets } from "./solution";
const result = averageBuckets([Number.MAX_VALUE, Number.MAX_VALUE], 2);
if (result.length !== 1 || result[0] !== Number.MAX_VALUE) {
  throw new Error(`Mean of two identical finite values must equal that value; got ${result[0]}`);
}
