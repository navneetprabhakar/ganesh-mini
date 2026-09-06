import { updateWindow, type WindowState } from './solution';
const state: WindowState = {totalItems:20,pageSize:10,page:1};
Object.defineProperty(state, 'totalItems', {enumerable:false});
const result = updateWindow(state, {type:'page',page:2});
if (result.state.totalItems !== 20 || result.rangeStart !== 11 || result.rangeEnd !== 20) throw new Error('validated typed totalItems lost on copy, corrupting result range');
