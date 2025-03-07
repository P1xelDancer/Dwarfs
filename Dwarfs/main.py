from modules.Views import menu
from modules.globals import GlobalVars
from modules.Models import dwarf
from colorama import Fore, Style
import threading, time

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

def main():
    createDwarfs()
    schedulerThread = threading.Thread(target=scheduler, daemon=True)
    schedulerThread.start()
    menu.mainMenu(globalV)

def createDwarfs():
    playableDwarfsNumber = 2
    globalV.timeSlow = 15
    while len(globalV.dwarfs) < playableDwarfsNumber:
        name = input("\n\tKérek egy törp nevet: ")
        if name in globalV.dwarfs:
            print(Fore.RED + f"\n\tIlyen nevű törp ({name}) már létezik. Kérlek válassz másik nevet!" + Fore.RESET)
            continue
        else:
            globalV.dwarfs[name] = dwarf.Dwarf(name)
            print(Fore.GREEN + f"\n\t{name} örül, hogy részt vehet a kalandban." + Fore.RESET)
            print(globalV.dwarfs[name].busy, globalV.dwarfs[name].busyUntil)
            print(globalV.timeSlow)



# Itt kell definiálni, hogy mi fusson le a scheduler() után:
def completeTask(dwarf):
    if dwarf.currentTask == "mining":
        dwarf.mining(globalV)
    #     print(f"{dwarf.name} befejezte a bányászatot.")
    #     dwarf.state = 'idle'
    #     dwarf.current_task = None
    #     dwarf.busy_until = None
    #     # itt adhatod hozzá az alapanyagokat, XP-t stb.

    # elif dwarf.current_task == 'crafting':
    #     print(f"{dwarf.name} befejezte a craftingot.")
    #     dwarf.state = 'idle'
    #     dwarf.current_task = None
    #     dwarf.busy_until = None
    #     # itt adhatod hozzá a tárgyat az inventoryhoz

# # Időzítő:
def scheduler():
    while True:
        now = time.time()
        for dwarf in globalV.dwarfs.values():
            if dwarf.busyUntil and now >= dwarf.busyUntil:
                completeTask(dwarf)
        time.sleep(2)

# --------------------------------
# Állapotmentés és visszatöltés:
# import json

# with open('savegame.json', 'w') as f:
#     dwarfs_state = {name: dwarf.__dict__ for name, dwarf in globalV.dwarfs.items()}
#     json.dump(dwarfs_state, f)

# with open('savegame.json', 'r') as f:
#     data = json.load(f)
#     for name, attrs in data.items():
#         dwarf = Dwarf(name)
#         dwarf.__dict__.update(attrs)
#         globalV.dwarfs[name] = dwarf

#   -> Figyelni kell rá, hogy a visszatöltéskor a busyUntil jövőbeni-e vagy sem
# if dwarf.busy_until and dwarf.busy_until > time.time():
#     dwarf.busy = True
# else:
#     dwarf.busy = False
#     dwarf.current_task = None
# -------------------------------

main()