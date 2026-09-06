import { ChoiceDeck, type DeckOption } from './solution';
const option: DeckOption = {value:'A', label:'A'};
Object.defineProperty(option, 'value', {enumerable:false});
if (!new ChoiceDeck([option]).choose('A')) throw new Error('Required choice value lost');
