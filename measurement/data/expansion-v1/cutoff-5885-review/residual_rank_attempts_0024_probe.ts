import { rankAttempts, Attempt } from './solution';
const attempt: Attempt = {id: 1, participant: 'a', score: 90};
Object.defineProperty(attempt, 'id', {value: 1, enumerable: false});
if (rankAttempts([attempt])[0].id !== 1) throw new Error('copied attempt lost validated id');
