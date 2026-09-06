import { MemberDirectory, MembershipState, type Member } from "./solution";
const member: Member = {id: 1, handle: "one", email: "", givenName: "", familyName: "", state: MembershipState.Active, verified: true, zone: ""};
Object.defineProperty(member, "id", {enumerable: false});
const directory = new MemberDirectory([member], 1);
if (directory.current().id !== 1) throw new Error("Constructor must preserve current member's valid required ID");
