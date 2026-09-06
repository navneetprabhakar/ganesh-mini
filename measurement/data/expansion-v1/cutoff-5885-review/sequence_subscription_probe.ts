import { SequenceChooser } from './solution';
const chooser = new SequenceChooser({kind: 'choice', options: ['x']});
const calls: string[] = [];
let removeChild = () => {};
let installed = false;
const removeParent = chooser.subscribe(() => {
  if (!installed) {
    installed = true;
    removeChild = chooser.subscribe(() => { calls.push('child-a'); });
    chooser.subscribe(() => { calls.push('child-b'); });
  }
});
chooser.next();
removeParent();
removeChild();
chooser.next();
if (calls.join(',') !== 'child-b') throw new Error(`sibling subscription removed: ${calls}`);
