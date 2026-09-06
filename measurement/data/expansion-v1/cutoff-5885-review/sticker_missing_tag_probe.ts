import {buildStickerGallery} from './solution';
const tags=['match'];tags.length=2;
if(buildStickerGallery('match',[{id:1,imageBase64:'x',tags}]).kind!=='empty')throw new Error('Record with missing tag not ignored');
