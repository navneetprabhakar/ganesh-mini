'use strict';
const assert = require('node:assert/strict');
const { createArtifactHeaderController } = require('./solution');
class Options {
  constructor() {
    Object.assign(this, { artifactId: 'a', artifactName: 'n', revision: 'r', ownerName: 'o', collectionId: 'c', editArtifact() {}, deleteArtifact() {}, notify() {} });
  }
}
assert.throws(() => createArtifactHeaderController(new Options()), TypeError, 'class instances are not plain objects');
