const assert = require('node:assert/strict');
const { validateBuildPolicy } = require('./solution');
class Policy {
  constructor() {
    this.engine = 'node'; this.targets = ['server', 'browser'];
    this.checks = ['format', 'unit']; this.options = { strict: true };
    this.metadata = { mode: 'automatic' };
  }
}
assert.throws(() => validateBuildPolicy(new Policy()), Error, 'Policy must be plain');
