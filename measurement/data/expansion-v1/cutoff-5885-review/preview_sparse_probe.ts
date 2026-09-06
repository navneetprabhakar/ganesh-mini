import { DocumentPreviewController } from './solution';
const controller = new DocumentPreviewController();
controller.select({ name: 'valid', mediaType: 'text/plain', bytes: [1] });
const accepted = controller.select({ name: 'holes', mediaType: 'text/plain', bytes: new Array<number>(1) });
if (accepted !== false) throw new Error('Nonempty sparse byte array accepted: ' + JSON.stringify(controller.snapshot()));
const state = controller.snapshot();
if (state.preview !== undefined || state.visible || !state.error) throw new Error('Invalid selection did not clear preview');
