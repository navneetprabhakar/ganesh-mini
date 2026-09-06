import { decodeInlineNotes } from './solution';
const input = '{{unknown:a\\*b}}';
const actual = decodeInlineNotes(input);
const expected = [{ type: 'text', text: '{{unknown:a*b}}' }];
if (JSON.stringify(actual) !== JSON.stringify(expected)) throw new Error('Ordinary fallback did not unescape: ' + JSON.stringify(actual));
