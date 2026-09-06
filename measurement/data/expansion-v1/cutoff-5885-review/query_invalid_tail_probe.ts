import { parseWorkReference } from './solution';
const config = { mockMode: false, caseDeskUrl: '/cases', messageDeskUrl: '/messages' };
for (const query of ['case=valid&message=%ZZ', 'ignored=%ZZ&case=valid', 'case=valid&%ZZ=x']) {
  let error: unknown;
  try { parseWorkReference(query, config); } catch (caught) { error = caught; }
  if (!(error instanceof URIError)) throw new Error('Malformed escape accepted: ' + query);
}
