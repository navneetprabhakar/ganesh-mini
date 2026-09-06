import { buildWorkshopSubmission } from './solution';
const result = buildWorkshopSubmission({ organizer: 'A', email: 'a@b', title: 'T', format: 'onsite', venue: 'V', summary: 'S', registrationCloses: '0099-01-01' }, '0099-01-01');
if (!result.ok) throw new Error('Real Gregorian year 0099 must be accepted: ' + result.errors.join(','));
