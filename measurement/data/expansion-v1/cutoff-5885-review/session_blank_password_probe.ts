import { signIn } from "./solution";
const result = signIn([{username:"u", password:"   ", disabled:false}], [], "u", "   ", "t");
if (result.ok || result.reason !== "invalid-credentials") throw new Error("Blank password must be invalid credentials");
