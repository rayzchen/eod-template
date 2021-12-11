import glob
import os
import sys

master = "NDTec Rocket"

def capitalize(s):
    return " ".join(map(lambda x: x[0].capitalize() + x[1:], s.split(" ")))

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

for name in os.listdir("archived"):
    if not os.path.isdir(os.path.join("archived", "name")):
        continue
    with open("archived/" + name + "/ignored.txt") as f:
        ignored.update(f.read().rstrip().splitlines())
    with open("archived/" + name + "/list.txt") as f:
        ignored.update(f.read().rstrip().splitlines())

for file in glob.glob("elements/**/in.txt", recursive=True):
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

tiers = [[]]
tierlist = {}
names = list(filter(lambda a: all(b in elements or b in ignored for b in (get_ingredients(a) or [None])), get_ingredients(master) - ignored))
print(len(names), "elements")
for i in range(len(names) - 1, -1, -1):
    elem_ignored = ignored & set(elements[names[i]])
    if not set(elements[names[i]]) - ignored:
        tierlist[names[i]] = 0
        tiers[0].append(names.pop(i))

while names:
    for j in range(len(names) - 1, -1, -1):
        nums = []
        for ingr in elements[names[j]]:
            if ingr not in tierlist and ingr not in ignored:
                break
            nums.append(tierlist[ingr] if ingr not in ignored else -1)
        else:
            tier = max(nums)
            if tier == len(tiers) - 1:
                tiers.append([])
            tierlist[names[j]] = tier + 1
            tiers[tier + 1].append(names.pop(j))

for i in range(len(tiers)):
    tiers[i].sort()

for i, tier in enumerate(tiers):
    print("Tier", str(i + 1) + ": " + ", ".join(tier))

if len(sys.argv) > 1 and "-w" in sys.argv:
    offset = 35
    i = 0
    with open("commands.txt", "w+") as f:
        for tier in tiers:
            i += 1
            if i <= offset:
                continue
            for elem in tier:
                f.write(", ".join(elements[elem]) + "\n!s " + capitalize(elem) + "\n")
            f.write("\n")
