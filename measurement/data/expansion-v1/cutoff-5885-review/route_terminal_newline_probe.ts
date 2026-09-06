import { orderPatterns } from "./solution";
for (const pattern of ["/abc\n", "/:id\n"]) {
  let rejected = false;
  try { orderPatterns([pattern]); }
  catch (error) {
    if (!(error instanceof Error) || error.message !== "invalid pattern") throw error;
    rejected = true;
  }
  if (!rejected) throw new Error("Non-ASCII-segment newline accepted: " + JSON.stringify(pattern));
}
