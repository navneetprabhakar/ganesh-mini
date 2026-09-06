import { addBook, type Book } from "./solution";
const book: Book = {id: "old", ownerId: "o", title: "T", author: "A", publishedYear: 2000, genre: "G"};
Object.defineProperty(book, "id", {enumerable: false});
const result = addBook([book], "o", "new", {title: "New", author: "A", publishedYear: 2000, genre: "G"});
if (!result.ok || result.books[0].id !== "old") throw new Error("Existing required ID must survive independent book copy");
