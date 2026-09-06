const compileFeatureManifest = require('./solution');
require('node:assert').throws(() => compileFeatureManifest({label:'x', flags:new Array(1)}), TypeError);
