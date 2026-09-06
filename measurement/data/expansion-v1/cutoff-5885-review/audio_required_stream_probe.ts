import { ParticipantAudio, AudioRoomState } from './solution';
const local: ParticipantAudio = { participantId: 'p', streamKey: 'stream', muted: false };
Object.defineProperty(local, 'streamKey', { value: 'stream', enumerable: false });
const room = new AudioRoomState('', 'relay'); room.join(local);
if (room.snapshot().participants[0].streamKey !== 'stream') throw new Error('Required stream key must survive copying');
