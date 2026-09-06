import { validateRegistration } from "./solution";
const result = validateRegistration({contact: "a@b..c", organization: "O", role: "R", givenName: "G", familyName: "F", summary: "1234567890", attachment: {name: "a.txt"}});
if (!result.valid || result.errors.contact !== null) {
  throw new Error("Contact meets stated one-@, non-whitespace, dot-containing non-dot-edge domain rules");
}
