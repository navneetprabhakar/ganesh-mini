const { HandlerRegistry } = require('./solution');
const registry = new HandlerRegistry();
if (Reflect.ownKeys(registry).some(key => registry[key] instanceof Map)) throw new Error('Internal maps exposed as public own properties despite non-exposure requirement');
