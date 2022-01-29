# eod-template

## Navigation
- `elements/` folder for all elements you want to create, any .txt file inside is processed
- `archived/` for any past projects, any elements defined in there can be used in `elements/` (DO NOT TOUCH THIS FOLDER)
- `master.txt` put the name of your project element inside here, will be used in various files
- `ignored.txt` for any elements you want to use that exist in EoD but not your project (like AEFW or basic elements)
- `gen.py` to check your project works
  - If `element already exists` is printed it means you defined it twice
  - an element name on its own indicates you haven't defined it
  - If `references` is printed that means there is a circular recipe (e.g if element A uses element B which uses element A)
  - the two numbers at the bottom are respectively the number of defined elements in `elements/` and the total number of elements in the archive and `elements/`
- `list.py`: give name of element to see what is required to make this element, output also written to `list.txt`
- `tiers.py`: shows order of complexity to create elements, passing `-w` writes to `commands.txt`
- `archive.py`: puts all relevant files in `archived/`, wipes `master.txt` and makes a clean slate so you can create another element (the input asks what folder name do you want in `archived/`)
