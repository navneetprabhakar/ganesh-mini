import { ColumnShape, removeAuditTable } from './solution';
const column: ColumnShape = { name: 'id', kind: 'integer', primary: true, autoIncrement: false, unique: true, nullable: false };
Object.defineProperty(column, 'name', { value: 'id', enumerable: false });
if (removeAuditTable([{ name: 'users', columns: [column] }])[0].columns[0].name !== 'id') throw new Error('Required column name must survive copying');
