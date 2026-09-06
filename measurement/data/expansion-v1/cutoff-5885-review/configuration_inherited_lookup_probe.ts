import { ConfigurationCatalog } from './solution';
if (new ConfigurationCatalog([]).get('constructor') !== undefined) throw new Error('Missing setting must not return inherited Object constructor');
