import { DecisionPrompt } from './solution';
const snapshot = new DecisionPrompt('Title', 'Message', 'constructor').snapshot();
if (snapshot.confirmLabel !== 'Confirm' || snapshot.cancelLabel !== 'Cancel') {
  throw new Error('Unsupported constructor locale did not fall back to English: ' + JSON.stringify(snapshot));
}
