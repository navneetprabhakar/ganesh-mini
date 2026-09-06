import { ReviewLedger, type Review } from "./solution";
const review: Review = {id:"r", productId:"p", reviewerId:"u", comment:"Good", score:3};
Object.defineProperty(review, "score", {enumerable:false});
if (new ReviewLedger().add(review).score !== 3) throw new Error("Required validated score must survive copy");
