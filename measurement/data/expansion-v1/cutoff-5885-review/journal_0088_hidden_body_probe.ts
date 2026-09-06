import { buildJournalRecord, type JournalDraft } from './solution';
const draft: JournalDraft = { body: 'text', writerKey: '0000000000000000' };
Object.defineProperty(draft, 'body', { value: 'text', enumerable: false });
if (buildJournalRecord(draft, 0).body !== 'text') throw new Error('returned record lost validated required body');
