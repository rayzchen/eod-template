import itertools
import glob
import os
import sys

with open("master.txt") as f:
    master = f.read().rstrip()

def check_recursive(element, tree=[], seen=[]):
    for ingredient in elements.get(element, []):
        if ingredient in tree:
            print(element, "references", ingredient)
            return False
        if ingredient in seen:
            continue
        tree.append(ingredient)
        if not check_recursive(ingredient, tree, seen):
            tree.pop()
            return False
        tree.pop()
        seen.append(ingredient)
    return True

def get_ingredients(element, ingredients=None):
    if ingredients is None:
        ingredients = set()
    ingredients.add(element)
    for ingredient in elements.get(element, []):
        if ingredient not in ingredients:
            get_ingredients(ingredient, ingredients)
    return ingredients

def save_elements(elems, file):
    with open(file, "w+") as f:
        if not len(elems):
            return
        text = ""
        for elem in sorted(elems):
            ingredients = elements.get(elem, [])
            if not len(ingredients):
                continue
            text += elem + "\n- " + "\n- ".join(ingredients) + "\n\n"
        text = text[:-2]
        f.write(text)

elements = {}
with open("ignored.txt") as f:
    ignored = set(f.read().rstrip().splitlines())

for name in os.listdir("archived"):
    if not os.path.isdir(os.path.join("archived", name)):
        continue
    with open("archived/" + name + "/ignored.txt") as f:
        ignored.update(f.read().rstrip().splitlines())
    for file in glob.glob("archived/" + name + "/elements/**/*.txt", recursive=True):
        with open(file) as f:
            ignored.update([line for line in f.read().rstrip().splitlines() if not line.startswith("- ")])

for file in glob.glob("elements/**/*.txt", recursive=True):
    with open(file) as f:
        content = f.read().rstrip()
    if content == "":
        continue

    recipes = content.split("\n\n")
    for recipe in recipes:
        lines = recipe.splitlines()
        name = lines[0]
        if name in elements or name in ignored:
            print("Element", name, "declared twice")
        ingredients = list(map(lambda a: a[2:], lines[1:]))
        elements[name] = ingredients

element_pairs = list(elements.items())
i = 0
for a1, a2 in element_pairs[:-1]:
    i += 1
    for b1, b2 in element_pairs[i:]:
        if a2 == b2:
            print(a1, "has the same recipe as", b1)

ingredients = list(set(itertools.chain(*list(elements.values()))))
ingredients.sort()
print("List of undefined elements:")
for ingredient in ingredients:
    if ingredient not in elements and ingredient not in ignored:
        print(ingredient)
print()

elements2 = []
used = [master]
for element in elements:
    elements2.append({"name": element, "ingredients": []})
for element in elements2:
    for ingredient in elements[element["name"]]:
        used.append(ingredient)

for element in elements:
    if element not in used:
        print(element, "is not used")

elements2 = []
used = [master]
for element in elements:
    elements2.append({"name": element, "ingredients": []})
for element in elements2:
    for ingredient in elements[element["name"]]:
        used.append(ingredient)
print(len(elements), "new elements")
print(len(elements) + len(ignored), "total elements")

check_recursive(master)

if len(sys.argv) > 1:
    if "-w" in sys.argv:
        total = get_ingredients(master)
        remaining = set(elements.keys()) - total
        
        save_elements(total, "out.txt")
        print(f"{len(remaining)} unused elements")
    if "-g" in sys.argv:
        for file in glob.glob("archived/*/elements/*.txt", recursive=True):
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
        with open("graph.dot", "w+") as f:
            f.write("digraph tree {\n\t")
            f.write("node [ fontname=\"Arial\", shape=\"box\", style=\"rounded\" ];\n\t")
            f.write("edge [ dir=\"none\" ];\n\t")
            f.write("graph [ splines=ortho ];\n\t")
            f.write(f"\"{master}\" [ style=\"rounded,filled\", fontcolor=\"#ffffff\", fillcolor=\"#000000\" ]\n\t")
            text = ""
            for element in elements:
                for ingredient in elements[element]:
                    text += f"\"{element}\" -> \"{ingredient}\"\n\t"
            text = text[:-1]
            f.write(text + "}")
