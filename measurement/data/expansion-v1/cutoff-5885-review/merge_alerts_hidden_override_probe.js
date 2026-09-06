'use strict';
const assert = require('node:assert/strict');
const { mergePreferences } = require('./solution');
const alerts = {};
Object.defineProperty(alerts, 'email', { value: false });
const result = mergePreferences({ theme: 'dark', compact: true, alerts: { email: true, push: true } }, { alerts });
assert.equal(result.alerts.email, false);
