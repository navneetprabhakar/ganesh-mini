import { dismissBanner, type Banner } from './solution';
const banner: Banner = {id:'a',kind:'neutral',text:'A',ttlMs:10};
Object.defineProperty(banner, 'id', {enumerable:false});
if (dismissBanner([banner], 'other')[0].id !== 'a') throw new Error('Required banner ID lost');
