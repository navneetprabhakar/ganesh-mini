import { reduceMessages, Message } from './solution';
const message: Message = { id: 'm', body: 'retain', authorId: 'u', reactions: 0 };
Object.defineProperty(message, 'body', { value: 'retain', enumerable: false });
const result = reduceMessages([message], { userId: 'u' }, { type: 'react', messageId: 'm' });
if (result[0].body !== 'retain') throw new Error('Reaction lost required message body');
