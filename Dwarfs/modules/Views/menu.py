import msvcrt
from colorama import Fore, Style
import time
import os
from modules.Models import dwarf
from modules.globals import GlobalVars
import sys
import threading

#dwarfs = {}
globalV = GlobalVars()

def availableDwarfs(globalV):
    print("\n\tSzabad törpök listája:")
    availableDwarf = 0
    #for value in dwarfs.values():
    for value in globalV.dwarfs.values():
        if not value.busy:
            print(f"Törp: {value.name} - Lvl: {value.level}")
            availableDwarf += 1
    if not availableDwarf:
        print("Nincs szabad törp.")
        time.sleep(globalV.timeMedium)
        os.system('cls')
        mainMenu(globalV)

def mainMenu(globalV):
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
            time.sleep(globalV.timeFast)
            os.system('cls')
            mainMenu(globalV)
    
    match choose:
        case "1":
            hireDwarfMenu(globalV)
        case "2":
            sendToMiningMenu(globalV)
        case "3":
            sendToCraftingMenu(globalV)
        case "4":
            if globalV.dwarfs:
                #for value in dwarfs.values():
                for value in globalV.dwarfs.values():
                    print(f"Törp: {value.name} - Lvl: {value.level}")
            else:
                print("Nincsenek még felbérelt törpjeid.")
            time.sleep(globalV.timeSlow)
            os.system('cls')
            mainMenu(globalV)
        case "5":
            terminateDwarfMenu(globalV)
        case "0":
            sys.exit()
        # Nem megfelelő karakter leütése után tájékoztatás, majd a menü újratöltése.
        case _:
            print(Fore.RED + "\n\tHibás bevitel..." + Fore.RESET)
            time.sleep(globalV.timeFast)
            os.system('cls')
            mainMenu()

def hireDwarfMenu(globalV):
    
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
            time.sleep(globalV.timeFast)
            os.system('cls')
            mainMenu(globalV)
    
    match choose:
        case "1":
            name = input("\n\tA törp neve: ")
            #if name in dwarfs:
            if name in globalV.dwarfs:
                print(Fore.RED + f"\n\tIlyen nevű törp ({name}) már létezik. Kérlek válassz másik nevet!" + Fore.RESET)
                time.sleep(globalV.timeFast)
                os.system('cls')
                hireDwarfMenu(globalV)
            else:
                #dwarfs[name] = dwarf.Dwarf(name)
                globalV.dwarfs[name] = dwarf.Dwarf(name)
                print(Fore.GREEN + f"\n\tSikeresen felbérelted a {name} nevű törpöt." + Fore.RESET)
                # dwarfList = list(dwarfs.keys())
                print("\n\tVisszalépés a főmenübe.")
                time.sleep(globalV.timeSlow)
                os.system('cls')
                mainMenu(globalV)
        case "0":
            print("Visszalépés a főmenübe.")
            time.sleep(globalV.timeFast)
            os.system('cls')
            mainMenu(globalV)
        # Nem megfelelő karakter leütése után tájékoztatás, majd a menü újratöltése.
        case _:
            print(Fore.RED + "\n\tHibás bevitel..." + Fore.RESET)
            time.sleep(globalV.timeFast)
            os.system('cls')
            hireDwarfMenu(globalV)


def sendToMiningMenu(globalV):
    availableDwarfs(globalV)
    name = input("\n\tKit szeretnél elküldeni bányászni?: ")
    
    #if name in dwarfs:
    if name in globalV.dwarfs:
        while True:
            miningTime = input(f"\n\tMeddig bányásszon {name} törp (1-12 óra)?: ")
            
            if miningTime.isdigit() and (1 <= int(miningTime) <= 12):
                miningTime = int(miningTime)
                #miningThread = threading.Thread(target=dwarfs[name].mining, args=(miningTime,))
                miningThread = threading.Thread(target=globalV.dwarfs[name].mining, args=(globalV, miningTime))
                miningThread.start()
                #dwarfs[name].busy = 1
                #dwarfs[name].remainingTurns = turns
                #print(Fore.GREEN + f"\n\t{name} törp elindult {turns} órát gürcölni a bányába." + Fore.RESET)
                print("\n\tVisszalépés a főmenübe.")
                time.sleep(globalV.timeMedium)
                os.system('cls')
                mainMenu(globalV)
            else:
                print(Fore.RED + f"\n\tCsak 1 és 12 óra közötti intervallumot adhatsz meg!" + Fore.RESET)
    else:
        print(Fore.RED + f"\n\tNincs ilyen nevű törp a csapatodban... Még a nevüket sem tudod megjegyezni? ")
        time.sleep(globalV.timeFast)
        print("\n\tNa szedd össze magad és döntsd el, hogy kit akarsz dolgoztatni!." + Fore.RESET)
        time.sleep(globalV.timeMedium)
        os.system('cls')
        sendToMiningMenu(globalV)

def sendToCraftingMenu(globalV):
    availableDwarfs(globalV)
    name = input("\n\tKit szeretnél megbízni a gyártással?: ")
    
    #if name in dwarfs:
    if name in globalV.dwarfs:
        while True:
            craftingTime = input(f"\n\tMeddig gyártson {name} törp (1-12 óra)?: ")

            if craftingTime.isdigit() and (1 <= int(craftingTime) <= 12):
                craftingTime = int(craftingTime)
                craftingThread = threading.Thread(target=crafting, args=(globalV, name, craftingTime))
                craftingThread.start()
                print("\n\tVisszalépés a főmenübe.")
                time.sleep(globalV.timeMedium)
                os.system('cls')
                mainMenu(globalV)
            else:
                print(Fore.RED + f"\n\tCsak 1 és 12 óra közötti intervallumot adhatsz meg!" + Fore.RESET)
    else:
        print(Fore.RED + f"\n\tNincs ilyen nevű törp a csapatodban... Még a nevüket sem tudod megjegyezni? ")
        time.sleep(globalV.timeFast)
        print("\n\tNa szedd össze magad és döntsd el, hogy kit akarsz dolgoztatni!." + Fore.RESET)
        time.sleep(globalV.timeMedium)
        os.system('cls')
        sendToCraftingMenu(globalV)

def terminateDwarfMenu(globalV):
    print("\n\tA felbérelt törpök listája:")
    
    #for value in dwarfs.values():
    for value in globalV.dwarfs.values():
        print(f"Törp: {value.name} - Lvl: {value.level}")
    name = input("\n\tKit küldesz el?: ")
    
    #if name in dwarfs:
    if name in globalV.dwarfs:
        #del dwarfs[name]
        del globalV.dwarfs[name]
        print(Fore.GREEN + f"\n\tSikeresen megszabadultál a ({name}) nevű törptől... Gratulálok Te szívtelen dög!" + Fore.RESET)
        time.sleep(globalV.timeFast)
        print("\n\tRemélem mást nem akarsz elküldeni... Visszalépés a főmenübe.")
        time.sleep(globalV.timeMedium)
        os.system('cls')
        mainMenu(globalV)
    else:
        print(Fore.RED + f"\n\tNincs ilyen nevű törp a csapatodban... Még a nevüket sem tudod megjegyezni? ")
        time.sleep(globalV.timeMedium)
        print("\n\tNa menj és inkább csinálj valami értelmeset... Visszalépés a főmenübe." + Fore.RESET)
        time.sleep(globalV.timeSlow)
        os.system('cls')
        mainMenu(globalV)

def crafting(globalV, name, craftTime):
    #dwarfs[name].busy = 1
    globalV.dwarfs[name].busy = 1
    print(f"{name} törp {craftTime} órán keresztül fog gyártani. (A játékban 1 óra a valóságban 2 percnek felel meg.)")
    craftTime = craftTime * 10
    time.sleep(craftTime)
    #dwarfs[name].busy = 0
    globalV.dwarfs[name].busy = 0
    print(f"{name} törp végzett a gyártással.")