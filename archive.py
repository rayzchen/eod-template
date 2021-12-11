import os
import sys
import shutil

sys.argv = [sys.argv[0], "-w"]

import gen

with open("master.txt") as f:
    sys.argv = [sys.argv[0], f.read().rstrip()]

import list as _list

print()
name = input("Enter suitable folder name similar to master.txt: ")
os.makedirs(os.path.join("archived", name), exist_ok=True)
os.rename("list.txt", os.path.join("archived", name, "list.txt"))
os.rename("out.txt", os.path.join("archived", name, "out.txt"))
os.rename("ignored.txt", os.path.join("archived", name, "ignored.txt"))
os.rename("elements", os.path.join("archived", name, "elements"))
os.mkdir("elements")
open("ignored.txt", "w+").close()
open("elements/in.txt", "w+").close()
