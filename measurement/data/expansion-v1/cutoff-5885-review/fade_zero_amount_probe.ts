import { fadeToGray } from "./solution";
const result = fadeToGray({r: -Number.MAX_VALUE, g: Number.MAX_VALUE, b: Number.MAX_VALUE, a: 128}, 0);
if (result.r !== 0 || result.g !== 255 || result.b !== 255 || result.a !== 128) {
  throw new Error("Zero fade must return original channels clamped; got " + JSON.stringify(result));
}
