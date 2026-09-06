import { SubscriberStore, type Subscriber } from "./solution";
const subscriber: Subscriber = { id: "a", name: "A", email: "a@example.test", active: true };
Object.defineProperty(subscriber, "id", {enumerable: false});
const store = new SubscriberStore([subscriber]);
if (store.list()[0].id !== "a") throw new Error("Valid required non-enumerable ID lost during constructor copy");
