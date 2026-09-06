import { groupPresets, type Preset } from './solution';
const preset: Preset = { id: 'a', label: 'A', status: 'available' };
Object.defineProperty(preset, 'label', { value: 'A', enumerable: false });
const result = groupPresets([preset]);
if (result.available[0].label !== 'A') throw new Error('copied preset lost its required label');
