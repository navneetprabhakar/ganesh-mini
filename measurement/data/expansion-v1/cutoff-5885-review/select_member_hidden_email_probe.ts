import { selectMembers, type Member } from "./solution";
const member: Member = {email:"a@b", role:"user", lastSeen:null};
Object.defineProperty(member, "email", {enumerable:false});
if (selectMembers([member], "a", 0, 10).items[0].email !== "a@b") throw new Error("Required email must survive member copy");
