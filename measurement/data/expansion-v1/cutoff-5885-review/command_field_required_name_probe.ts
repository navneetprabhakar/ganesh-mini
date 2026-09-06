import { CommandDecoder, CommandField } from './solution';
const field: CommandField = { name: 'value', bytes: 1 };
Object.defineProperty(field, 'name', { enumerable: false });
const decoder = new CommandDecoder({ AA: [{ name: 'command', fields: [field] }] });
if (decoder.decodeFrame('AA01').fields[0].name !== 'value') throw new Error('required command field name lost');
