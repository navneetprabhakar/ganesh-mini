import { SensorArchive, type SensorReading } from './solution';
let caught = false;
try { new SensorArchive(new Array<SensorReading>(1)); }
catch (error) { if (!(error instanceof Error)) throw error; caught = true; }
if (!caught) throw new Error('Invalid missing reading must be rejected by constructor');
