import { FeatureCatalog } from "./solution";

const catalog = new FeatureCatalog();
try {
  catalog.amend(" ", {});
  throw new Error("Expected invalid-code rejection");
} catch (error) {
  if (!(error instanceof Error) || error.message !== "Feature code must not be empty") {
    throw new Error(`Wrong blank-code rejection: ${String(error)}`);
  }
}
