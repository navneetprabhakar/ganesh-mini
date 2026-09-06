import { renderMessage, MessageCatalog } from './solution';
const malformed = { common: {}, report: {}, dynamic: { matchCount: () => 42 } } as unknown as MessageCatalog;
if (renderMessage(malformed, 'matchCount', 1) !== 'matchCount') throw new Error('malformed formatter result did not fall back to key');
