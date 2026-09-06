const { getTextTransformer } = require('./solution');
if (getTextTransformer('constructor') !== getTextTransformer('plain')) throw new Error('Unknown constructor name resolved inherited property instead of plain transformer');
