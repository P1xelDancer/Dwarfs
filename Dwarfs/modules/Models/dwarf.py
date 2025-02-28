import random
import time
from colorama import Fore, Style
from modules.Views import menu
from modules.globals import GlobalVars

globalV = GlobalVars()

class Dwarf:
    def __init__(self, name):
        self.level = 1
        self.name = name
        self.needXP = 100
        self.currentXP = 0
        self.nextLvlMultiplier = 1.2
        self.busy = 0
        self.remainingTurns = 0

    def mining(self, globalV, mimingTime):
        capInd = 0
        miningXP = 20
        sumRock = 0
        sumIron = 0
        sumTitan = 0
        chanceTitan = 200
        chanceIron = 40

        self.busy = 1

        print(Fore.GREEN + f"\n\t{self.name} törp elindult {mimingTime} órát gürcölni a bányába." + Fore.RESET)
        time.sleep(globalV.timeMedium)

        for i in range(1, mimingTime + 1):
            
            if self.level == 1:
                miningLimit = 100
            else:
                miningLimit = 100 + 100 * ((20 * (self.level - 1)) / 100)
            
            if capInd == 0:
                print(f"\n{self.name} óránként {miningLimit} egységnyi nyersanyagot tud kitermelni")
                capInd = 1
            
            qRock = 0
            qIron = 0
            qTitan = 0
            
            for j in range(1, int(miningLimit) + 1):
                if random.randrange(1, chanceTitan) == 1:
                    qTitan += 1
                elif random.randrange(1, chanceIron) == 1:
                    qIron += 1
                else:
                    qRock += 1
            
            #print(f"Az {i}. órában a kitermelt nyersanyagok:\n\t- Titán: {qTitan}\t- Vas: {qIron}\t- Kő: {qRock}")
            if self.leveling(miningXP):
                capInd = 0
            
            sumRock += qRock
            sumIron += qIron
            sumTitan += qTitan
        
        mimingTime = mimingTime * 60
        time.sleep(mimingTime-globalV.timeFast)
        print(f"{self.name} törp befejezte a bányászást. {mimingTime/60} óra alatt kitermelt:\n\t{sumTitan} Titánt, {sumIron} Vasat és {sumRock} Követ")
        self.busy = 0
        

    def crafting(self, item):
        # items = {'badshortsword': [4, 2, 50], 'goodshortsword': [5, 3, 80]}
        print(f"{self.name} elkészített egy {item.name}-t ami {item.craftingTime} óráig tartott, {item.resource} vasba került és {item.giveXP} XP-t kapott érte.")
        self.leveling(item.giveXP)
    
    def leveling(self, gainXP):
        lvlUp = False
        self.currentXP += gainXP
        while (self.currentXP >= self.needXP):
            self.currentXP -= self.needXP
            self.needXP = self.needXP * self.nextLvlMultiplier
            self.level += 1
            lvlUp = True
        print(f"{self.name} az akciója után kapott {gainXP} XP-t, most {self.level}. szintű.")
        return lvlUp
    