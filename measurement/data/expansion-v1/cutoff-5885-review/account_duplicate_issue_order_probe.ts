import { validateAccount } from './solution';
const issues = validateAccount('UPDATE', {email:'a@b.com',accessLevel:''}, [{id:'a',email:'a@b.com'}]);
if (issues[0]?.field !== 'accessLevel' || issues[1]?.message !== 'Email is already in use') throw new Error('Duplicate email issue must follow format/required issues');
