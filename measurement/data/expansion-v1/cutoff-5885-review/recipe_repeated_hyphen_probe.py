from solution import RecipeShelf

recipe = {"slug": "a--b", "title": "Dish", "tags": []}
shelf = RecipeShelf([recipe])
assert shelf.detail("a--b") == recipe
