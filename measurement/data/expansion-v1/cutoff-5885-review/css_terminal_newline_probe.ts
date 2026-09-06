import { makeReadingLayoutStyles } from './solution';
for (const prefix of ['valid\n', 'valid\r', 'valid\u2028', 'valid\u2029']) {
  let error: unknown;
  try { makeReadingLayoutStyles(prefix); } catch (caught) { error = caught; }
  if (!(error instanceof TypeError)) throw new Error('Terminal newline accepted in prefix: ' + JSON.stringify(prefix));
}
