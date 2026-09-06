import {Navigator,Heading} from './solution';
const navigator = new Navigator(2 ** 54, 2);
if(!navigator.place(2 ** 53,0,Heading.East)) throw new Error('valid placement refused');
const before = navigator.snapshot()!.x;
const moved = navigator.advance();
console.log('moved',moved,'before',before,'after',navigator.snapshot()!.x);
if(!moved || navigator.snapshot()!.x === before) throw new Error('one-cell advance made no progress');
