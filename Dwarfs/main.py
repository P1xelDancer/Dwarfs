from modules.Views import menu
from modules.globals import GlobalVars

globalV = GlobalVars()

# Balin = Dwarf("Balin")
# Dwalin = Dwarf("Dwalin")
# BadShortsword = Item('Bad Shortsword', 5, 4, 200, 60)
# GoodShortsword = Item('Good Shortsword', 7, 6, 350, 100)
# Balin.mining(chanceTitan, chanceIron, 8)
# Dwalin.mining(chanceTitan, chanceIron, 16)
# Balin.crafting(BadShortsword)
# Dwalin.crafting(GoodShortsword)

# Dwarf.hireDwarf("Balin")
# print(f"Az első törp neve: {Dwarf.name}")

menu.mainMenu(globalV)