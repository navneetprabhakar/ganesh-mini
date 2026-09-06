import { ConversionHub, type DataRecord } from "./solution";
const source: DataRecord = {key: "k", fields: {required: "value"}};
Object.defineProperty(source.fields, "required", {enumerable: false});
const result = new ConversionHub().convert([source]);
if (!result[0].ok || result[0].record.fields.required !== "value") {
  throw new Error("No-transform conversion must preserve valid required field values");
}
