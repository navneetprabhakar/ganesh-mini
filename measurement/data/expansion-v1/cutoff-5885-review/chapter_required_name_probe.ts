import { ChapterDraft, ChapterComposer } from './solution';
const seed: ChapterDraft = { name: 'Chapter', text: 'Text', references: [] };
Object.defineProperty(seed, 'name', { value: 'Chapter', enumerable: false });
if (new ChapterComposer(seed, () => {}).save().name !== 'Chapter') throw new Error('Required name must survive seed copying');
