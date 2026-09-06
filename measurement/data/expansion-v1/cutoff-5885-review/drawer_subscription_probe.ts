import { DrawerService } from './solution';
const drawer = new DrawerService();
const calls: string[] = [];
let removeFirstChild = () => {};
let added = false;
drawer.subscribe(() => {
  if (!added) {
    added = true;
    removeFirstChild = drawer.subscribe(() => calls.push('first-child'));
    drawer.subscribe(() => calls.push('second-child'));
  }
});
drawer.toggle();
removeFirstChild();
drawer.toggle();
if (JSON.stringify(calls) !== '["second-child"]') throw new Error('Unsubscribe removed sibling registration: ' + JSON.stringify(calls));
