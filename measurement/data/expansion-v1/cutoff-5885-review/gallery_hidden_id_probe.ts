import { GalleryIndex, type GalleryEntry } from './solution';
const entry: GalleryEntry = {id:1, name:'A', note:''};
Object.defineProperty(entry, 'id', {enumerable:false});
if (new GalleryIndex([entry]).list()[0].id !== 1) throw new Error('Required gallery ID lost');
