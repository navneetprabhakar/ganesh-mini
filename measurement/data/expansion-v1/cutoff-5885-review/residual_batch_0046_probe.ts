import { BatchRegistry, type ProductionBatch } from './solution';
type Equal<A, B> = (<T>() => T extends A ? 1 : 2) extends (<T>() => T extends B ? 1 : 2) ? true : false;
const exactReturnContract: Equal<ReturnType<BatchRegistry['get']>, ProductionBatch | undefined> = true;
void exactReturnContract;
