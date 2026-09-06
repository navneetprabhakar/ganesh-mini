import { validateContactDraft } from './solution';
const result = validateContactDraft({ name: 'Ada', email: 'a@.b.c' });
if (!result.valid) throw new Error('Domain contains an interior dot but was rejected: ' + JSON.stringify(result));
