import { PreferencesSession, type Preferences } from './solution';
const current: Preferences = {nickname:'x',theme:'day',labels:[]};
Object.defineProperty(current, 'nickname', {enumerable:false});
const session = new PreferencesSession(current, {save:async () => {}, signOut:async () => {}});
if (session.draft.nickname !== 'x') throw new Error('deep copy loses non-enumerable required nickname');
