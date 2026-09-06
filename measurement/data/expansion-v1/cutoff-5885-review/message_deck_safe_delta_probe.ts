import { MessageDeck } from './solution';
const deck = new MessageDeck(['A','B','C'], [], '');
deck.move(2);
if (deck.move(Number.MAX_SAFE_INTEGER) !== 'A') throw new Error('Wrapping must preserve exact safe-integer delta modulo three');
