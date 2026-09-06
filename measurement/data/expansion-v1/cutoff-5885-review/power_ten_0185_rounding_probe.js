const { isPowerOfTen } = require('./solution');
for (const value of [999999999999999, 1000000000000001]) {
  if (isPowerOfTen(value) !== false) throw new Error('Non-power safe integer accepted: ' + value);
}
