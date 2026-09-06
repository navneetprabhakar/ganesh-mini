import { AccessDirectory } from './solution';
const directory = new AccessDirectory();
directory.enroll('a', '1234'); directory.enroll('A', '1234');
if (directory.listUserIds().join(',') !== 'A,a') throw new Error('Locale ordering differs from ascending code-unit lexicographic order: ' + directory.listUserIds().join(','));
