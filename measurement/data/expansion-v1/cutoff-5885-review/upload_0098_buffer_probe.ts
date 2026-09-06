declare function require(name: string): any;
import { createUploadGuard } from './solution';
const { Buffer } = require('node:buffer');
const bytes: Uint8Array = Buffer.from([1, 2, 3]);
const result = createUploadGuard('photo', 'image/')({ field: 'photo', mimeType: 'image/png', data: bytes });
result.data[0] = 99;
if (bytes[0] !== 1) throw new Error('Buffer-backed upload copy aliases input');
