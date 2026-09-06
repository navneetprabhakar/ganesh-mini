const {describeReading}=require('./solution');
const angle=1e-20;
const r=describeReading({hour:0,condition:'clear',temperature:0,feelsLike:0,windSpeed:0,windDegrees:angle,pressure:0,humidity:0});
require('node:assert').strictEqual(r.windRotation,angle);
