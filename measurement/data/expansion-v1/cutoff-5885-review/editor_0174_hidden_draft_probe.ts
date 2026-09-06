import { reduceEditor, EditorState } from './solution';
const state: EditorState = { dialog: 'none', groupDraft: 'group', passDraft: 'preserve', groups: [], passes: [] };
Object.defineProperty(state, 'passDraft', { value: 'preserve', enumerable: false });
const result = reduceEditor(state, { type: 'open', dialog: 'group' });
if (result.passDraft !== 'preserve') throw new Error('Opening group lost untouched required passDraft: ' + JSON.stringify(result));
