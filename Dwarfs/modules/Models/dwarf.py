import random
import time
from colorama import Fore, Style
from modules.Views import menu

class Dwarf:
    def __init__(self, name):
        self.level = 1
        self.name = name
        self.needXP = 100
        self.currentXP = 0
        self.nextLvlMultiplier = 1.2
        self.busy = False
        self.busyUntil = None
        self.currentTask = None
        self.miningLimit = 100
        self.eventMessage = ""

    def miningBeginCheck(self, globalV, miningHour):
        # - felszerelés ellenőrzés
        print(Fore.GREEN + f"\n\t{self.name} törp elindult {miningHour} órát gürcölni a bányába." + Fore.RESET)
        self.busy = True
        realTime = miningHour * globalV.realTimeMultiplier
        self.busyUntil = time.time() + realTime
        self.currentTask = "mining"
        

    def craftingBeginCheck(self, globalV, craftingHour):
        # - felszerelés ellenőrzés
        self.busy = True
        realTime = craftingHour * globalV.realTimeMultiplier
        self.busyUntil = time.time() + realTime
        self.currentTask = "crafting"
    
    def mining(self, globalV, miningHour):
        miningXP = 20
        sumRock = 0
        sumIron = 0
        sumTitan = 0
        chanceTitan = 200
        chanceIron = 40

        # # Csak ezeket állítani, hogy elinduljon a scheduler()-ben a szimulált idő
        # self.busy = True
        # self.busy_until = time.time() + 3600  # 1 óra szimulált idő
        # self.current_task = 'mining'

        # now = time.time()
        # miningTime = 30
        # dwarf.busy_until = now + miningTime
        
        time.sleep(globalV.timeMedium)

        for i in range(1, miningHour + 1):
            
            # if self.level == 1:
            #     miningLimit = 100
            # else:
            #     miningLimit = 100 + 100 * ((20 * (self.level - 1)) / 100)
            
            # if capInd == 0:
            #     print(f"\n{self.name} óránként {miningLimit} egységnyi nyersanyagot tud kitermelni")
            #     capInd = 1
            
            qRock = 0
            qIron = 0
            qTitan = 0
            
            for j in range(1, int(self.miningLimit) + 1):
                if random.randrange(1, chanceTitan) == 1:
                    qTitan += 1
                elif random.randrange(1, chanceIron) == 1:
                    qIron += 1
                else:
                    qRock += 1
            
            #print(f"Az {i}. órában a kitermelt nyersanyagok:\n\t- Titán: {qTitan}\t- Vas: {qIron}\t- Kő: {qRock}")
            if self.leveling(globalV, miningXP):
                self.eventMessage = f"{self.name} törp az {i}. óra után szintet lépett, ezért a hátralevő időben már {self.miningLimit} egységnyi ércet tudott kibányászni."
                globalV.messages.append(self.eventMessage)
            
            sumRock += qRock
            sumIron += qIron
            sumTitan += qTitan
    
        self.eventMessage = f"{self.name} törp befejezte a bányászást. {miningHour} óra alatt kitermelt:\n\t{sumTitan} Titánt, {sumIron} Vasat és {sumRock} Követ"
        globalV.messages.append(self.eventMessage)
        self.busy = 0
        self.busyUntil = None
        

    def crafting(self, item):
        # items = {'badshortsword': [4, 2, 50], 'goodshortsword': [5, 3, 80]}
        print(f"{self.name} elkészített egy {item.name}-t ami {item.craftingTime} óráig tartott, {item.resource} vasba került és {item.giveXP} XP-t kapott érte.")
        self.leveling(item.giveXP)
    
    def leveling(self, globalV, gainXP):
        lvlUp = False
        self.currentXP += gainXP
        while (self.currentXP >= self.needXP):
            self.currentXP -= self.needXP
            self.needXP = self.needXP * self.nextLvlMultiplier
            self.level += 1
            self.miningLimit = 100 + 100 * ((20 * (self.level - 1)) / 100)
            lvlUp = True
        self.eventMessage = f"{self.name} az akciója után kapott {gainXP} XP-t, most {self.level}. szintű."
        globalV.messages.append(self.eventMessage)
        return lvlUp
    
    
