import msvcrt
from colorama import Fore, Style
import time
import os
from modules.Models import dwarf
import sys
import threading

dwarfs = {}
timeSlow = 6
timeMedium = 3
timeFast = 2
# dwarfList = []

def availableDwarfs():
    print("\n\tSzabad törpök listája:")
    availableDwarf = 0
    for value in dwarfs.values():
        if not value.busy:
            print(f"Törp: {value.name} - Lvl: {value.level}")
            availableDwarf += 1
    if not availableDwarf:
        print("Nincs szabad törp.")
        time.sleep(timeMedium)
        os.system('cls')
        mainMenu()

def mainMenu():
    print("""
        Szia!
        Mit szeretnél csinálni?
          1.) Felbérelni egy törpöt
          2.) Bányászni küldeni az egyik törpöt
          3.) Gyártani küldeni az egyik törpöt
          4.) Törpök listája
          5.) Törp elküldése
          0.) Kilépés""")
    
    # A menüpont kiválasztásakor a karakter azonnal beolvasásra kerül, nem kell hozzá 'ENTER'-t ütni.
    msvcrt.kbhit()
    choose = msvcrt.getch().decode()
    
    # Ha a játékos nagyobb számot ad meg, mint ahány ajánlat van vagy az a 9-es, akkor a program tájékoztatja és újratölti a menüt.
    if choose.isdigit():
        if int(choose) < 0 or int(choose) > 5:
            print(Fore.RED + "\n\tNincs ilyen számú ajánlat!" + Fore.RESET)
            time.sleep(timeFast)
            os.system('cls')
            mainMenu()
    
    match choose:
        case "1":
            hireDwarfMenu()
        case "2":
            sendToMiningMenu()
        case "3":
            sendToCraftingMenu()
        case "4":
            if dwarfs:
                for value in dwarfs.values():
                    print(f"Törp: {value.name} - Lvl: {value.level}")
            else:
                print("Nincsenek még felbérelt törpjeid.")
            time.sleep(timeSlow)
            os.system('cls')
            mainMenu()
        case "5":
            terminateDwarfMenu()
        case "0":
            sys.exit()
        # Nem megfelelő karakter leütése után tájékoztatás, majd a menü újratöltése.
        case _:
            print(Fore.RED + "\n\tHibás bevitel..." + Fore.RESET)
            time.sleep(timeFast)
            os.system('cls')
            mainMenu()

def hireDwarfMenu():
    
    global dwarfList

    print("""
        1.) Törp nevének megadása
        0.) Visszalépés""")
    
    msvcrt.kbhit()
    choose = msvcrt.getch().decode()
    
    # Ha a játékos nagyobb számot ad meg, mint ahány ajánlat van vagy az a 9-es, akkor a program tájékoztatja és újratölti a menüt.
    if choose.isdigit():
        if int(choose) < 0 or int(choose) > 1:
            print(Fore.RED + "\n\tNincs ilyen számú ajánlat!" + Fore.RESET)
            time.sleep(timeFast)
            os.system('cls')
            mainMenu()
    
    match choose:
        case "1":
            name = input("\n\tA törp neve: ")
            if name in dwarfs:
                print(Fore.RED + f"\n\tIlyen nevű törp ({name}) már létezik. Kérlek válassz másik nevet!" + Fore.RESET)
                time.sleep(timeFast)
                os.system('cls')
                hireDwarfMenu()
            else:
                dwarfs[name] = dwarf.Dwarf(name)
                print(Fore.GREEN + f"\n\tSikeresen felbérelted a {name} nevű törpöt." + Fore.RESET)
                # dwarfList = list(dwarfs.keys())
                print("\n\tVisszalépés a főmenübe.")
                time.sleep(timeSlow)
                os.system('cls')
                mainMenu()
        case "0":
            print("Visszalépés a főmenübe.")
            time.sleep(timeFast)
            os.system('cls')
            mainMenu()
        # Nem megfelelő karakter leütése után tájékoztatás, majd a menü újratöltése.
        case _:
            print(Fore.RED + "\n\tHibás bevitel..." + Fore.RESET)
            time.sleep(timeFast)
            os.system('cls')
            hireDwarfMenu()


def sendToMiningMenu():
    availableDwarfs()
    name = input("\n\tKit szeretnél elküldeni bányászni?: ")
    
    if name in dwarfs:
        while True:
            turns = input(f"\n\tMeddig bányásszon {name} törp (1-12 óra)?: ")
            
            if turns.isdigit() and (1 <= int(turns) <= 12):
                dwarfs[name].busy = 1
                dwarfs[name].remainingTurns = turns
                print(Fore.GREEN + f"\n\t{name} törp elindult {turns} órát gürcölni a bányába." + Fore.RESET)
                print("\n\tVisszalépés a főmenübe.")
                time.sleep(timeMedium)
                os.system('cls')
                mainMenu()
            else:
                print(Fore.RED + f"\n\tCsak 1 és 12 óra közötti intervallumot adhatsz meg!" + Fore.RESET)
    else:
        print(Fore.RED + f"\n\tNincs ilyen nevű törp a csapatodban... Még a nevüket sem tudod megjegyezni? ")
        time.sleep(timeFast)
        print("\n\tNa szedd össze magad és döntsd el, hogy kit akarsz dolgoztatni!." + Fore.RESET)
        time.sleep(timeMedium)
        os.system('cls')
        sendToMiningMenu()

def sendToCraftingMenu():
    availableDwarfs()
    name = input("\n\tKit szeretnél megbízni a gyártással?: ")
    
    if name in dwarfs:
        while True:
            craftTime = input(f"\n\tMeddig gyártson {name} törp (1-12 óra)?: ")

            if craftTime.isdigit() and (1 <= int(craftTime) <= 12):
                craftTime = int(craftTime)
                craftingThread = threading.Thread(target=crafting, args=(name, craftTime))
                craftingThread.start()
                print("\n\tVisszalépés a főmenübe.")
                time.sleep(timeMedium)
                os.system('cls')
                mainMenu()
            else:
                print(Fore.RED + f"\n\tCsak 1 és 12 óra közötti intervallumot adhatsz meg!" + Fore.RESET)
    else:
        print(Fore.RED + f"\n\tNincs ilyen nevű törp a csapatodban... Még a nevüket sem tudod megjegyezni? ")
        time.sleep(timeFast)
        print("\n\tNa szedd össze magad és döntsd el, hogy kit akarsz dolgoztatni!." + Fore.RESET)
        time.sleep(timeMedium)
        os.system('cls')
        sendToCraftingMenu()

def terminateDwarfMenu():
    print("\n\tA felbérelt törpök listája:")
    
    for value in dwarfs.values():
        print(f"Törp: {value.name} - Lvl: {value.level}")
    name = input("\n\tKit küldesz el?: ")
    
    if name in dwarfs:
        del dwarfs[name]
        print(Fore.GREEN + f"\n\tSikeresen megszabadultál a ({name}) nevű törptől... Gratulálok Te szívtelen dög!" + Fore.RESET)
        time.sleep(timeFast)
        print("\n\tRemélem mást nem akarsz elküldeni... Visszalépés a főmenübe.")
        time.sleep(timeMedium)
        os.system('cls')
        mainMenu()
    else:
        print(Fore.RED + f"\n\tNincs ilyen nevű törp a csapatodban... Még a nevüket sem tudod megjegyezni? ")
        time.sleep(timeMedium)
        print("\n\tNa menj és inkább csinálj valami értelmeset... Visszalépés a főmenübe." + Fore.RESET)
        time.sleep(timeSlow)
        os.system('cls')
        mainMenu()

def crafting(name, craftTime):
    dwarfs[name].busy = 1
    print(f"{name} törp {craftTime} órán keresztül fog gyártani. (A játékban 1 óra a valóságban 2 percnek felel meg.)")
    craftTime = craftTime * 10
    time.sleep(craftTime)
    dwarfs[name].busy = 0
    print(f"{name} törp végzett a gyártással.")