'use strict';
const { createBindingLifecycle } = require('./solution');
const hooks = { mount() { if (this !== hooks) throw new Error('Hook receiver not preserved as hooks.mount(target,value)'); } };
createBindingLifecycle(hooks).mount({}, 1);
