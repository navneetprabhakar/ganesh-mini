import { dashboardReducer, createInitialDashboardState, type Metric } from './solution';
const metric: Metric = {id:'m', label:'Metric', unit:'count'};
Object.defineProperty(metric, 'id', {enumerable:false});
const state = dashboardReducer(createInitialDashboardState(), {type:'SET_METRICS', metrics:[metric]});
if (state.metrics[0].id !== 'm') throw new Error('Required metric ID lost during copy');
