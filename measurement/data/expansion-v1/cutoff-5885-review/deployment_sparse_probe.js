'use strict';
const assert = require('node:assert/strict');
const { assembleDeploymentRegistry } = require('./solution');
async function main() {
  await assert.rejects(async () => assembleDeploymentRegistry([], new Array(1)), TypeError);
}
main().catch(error => { console.error(error); process.exitCode = 1; });
