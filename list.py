import glob
import sys

if len(sys.argv) < 2:
    print(
"""Usage: python list.py [element name]

This will list all elements required (not including
ignored elements) to make the specified element.
The list will also be written to list.txt.
"""
    )
    exit()

def get_ingredients(element, ingredients=None):
    if ingredients is None:
        ingredients = set()
    ingredients.add(element)
    for ingredient in elements.get(element, []):
        if ingredient not in ingredients:
            get_ingredients(ingredient, ingredients)
    return ingredients

elements = {}
with open("ignored.txt") as f:
    ignored = set(f.read().rstrip().splitlines())
for file in glob.glob("elements/**/*.txt", recursive=True):
    with open(file) as f:
        content = f.read().rstrip()
    if content == "":
        continue

    recipes = content.split("\n\n")
    for recipe in recipes:
        lines = recipe.splitlines()
        name = lines[0]
        ingredients = list(map(lambda a: a[2:], lines[1:]))
        elements[name] = ingredients

master = " ".join(sys.argv[1:])
if master not in elements:
    print(f"{master} is not a valid element!")
    exit()
l = get_ingredients(master) - ignored
with open("list.txt", "w+") as f:
    f.write("\n".join(sorted(l)))
print(", ".join(sorted(l)))