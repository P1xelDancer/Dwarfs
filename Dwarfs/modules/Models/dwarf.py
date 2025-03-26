#import random
import time
from colorama import Fore, Style

class Dwarf:
    def __init__(self, name):
        self.level = 1
        self.name = name
        self.needXP = 120
        self.currentXP = 0
        self.sumXP = 0
        self.nextLvlMultiplier = 1.3
        self.busy = False
        self.busyUntil = None
        self.currentTask = None
        self.miningLimit = 60
        self.eventMessage = ""
        self.eventTime = 0

    def miningBeginCheck(self, globalV):
        # - felszerelés ellenőrzés
        print(Fore.GREEN + f"\n\t{self.name} törp elindult {self.eventTime} órát gürcölni a bányába." + Fore.RESET)
        self.busy = True
        realTime = self.eventTime * globalV.realTimeMultiplier
        self.busyUntil = time.time() + realTime
        self.currentTask = "mining"
        

    def craftingBeginCheck(self, globalV, craftingHour):
        # - felszerelés ellenőrzés
        self.busy = True
        realTime = craftingHour * globalV.realTimeMultiplier
        self.busyUntil = time.time() + realTime
        self.currentTask = "crafting"
    
    # def mining(self, globalV):
    #     miningXP = 30
    #     sumRock = 0
    #     sumIron = 0
    #     sumCoal = 0
    #     sumTitan = 0
    #     sumMythrill = 0
    #     chanceIron = 30
    #     chanceCoal = 50
    #     chanceTitan = 300
    #     chanceMythrill = 1000

    #     # # Csak ezeket állítani, hogy elinduljon a scheduler()-ben a szimulált idő
    #     # self.busy = True
    #     # self.busy_until = time.time() + 3600  # 1 óra szimulált idő
    #     # self.current_task = 'mining'

    #     # now = time.time()
    #     # miningTime = 30
    #     # dwarf.busy_until = now + miningTime
        
    #     time.sleep(globalV.timeMedium)

    #     for i in range(1, self.eventTime + 1):
            
    #         # if self.level == 1:
    #         #     miningLimit = 100
    #         # else:
    #         #     miningLimit = 100 + 100 * ((20 * (self.level - 1)) / 100)
            
    #         # if capInd == 0:
    #         #     print(f"\n{self.name} óránként {miningLimit} egységnyi nyersanyagot tud kitermelni")
    #         #     capInd = 1
            
    #         qRock = 0
    #         qIron = 0
    #         qCoal = 0
    #         qTitan = 0
    #         qMythrill = 0
            
    #         for j in range(1, int(self.miningLimit) + 1):
    #             if random.randrange(1, chanceMythrill) == 1:
    #                 qMythrill += 1
    #             elif random.randrange(1, chanceTitan) == 1:
    #                 qTitan += 1
    #             elif random.randrange(1, chanceCoal) == 1:
    #                 qCoal += 1
    #             elif random.randrange(1, chanceIron) == 1:
    #                 qIron += 1
    #             else:
    #                 qRock += 1
            
    #         self.sumXP += miningXP
            
    #         if self.leveling(globalV, miningXP):
    #             self.eventMessage = f"\n\t{self.name} törp az eddigi munkájának köszönhetően {self.sumXP} XP-t gyűjtött és a(z) {i}. óra után szintet lépett,\n\tezért innentől kezdve már óránként {self.miningLimit} egységnyi ércet tud kibányászni.\n"
    #             globalV.messages.append(self.eventMessage)
    #             self.sumXP = 0
            
    #         sumRock += qRock
    #         sumIron += qIron
    #         sumCoal += qCoal
    #         sumTitan += qTitan
    #         sumMythrill += qMythrill

    #     globalV.globalRock += sumRock
    #     globalV.globalIron += sumIron
    #     globalV.globalCoal += sumCoal
    #     globalV.globalTitan += sumTitan
    #     globalV.globalMythrill += sumMythrill
    
    #     self.eventMessage = f"\n\t{self.name} törp befejezte a bányászást. {self.eventTime} óra alatt kitermelt:\n\t\t{sumMythrill} Mythrillércet, {sumTitan} Titánércet, {sumIron} Vasércet és {sumRock} Követ"
    #     globalV.messages.append(self.eventMessage)
    #     self.eventMessage = f"\n\tA kemény munkája után, az előző szintlépése óta kapott {self.sumXP} XP-t, most {self.level}. szintű."
    #     globalV.messages.append(self.eventMessage)
    #     self.sumXP = 0
    #     self.eventMessage = f"\n\tA törp tábor összes nyersanyaga:\n\t\t{globalV.globalMythrill} Mythrillérc, {globalV.globalTitan} Titánérc, {globalV.globalIron} Vasérc, {globalV.globalRock} Kő\n"
    #     globalV.messages.append(self.eventMessage)
    #     self.busy = 0
    #     self.busyUntil = None

    def mining(self, globalV):
        time.sleep(globalV.timeMedium)
        
        total_mined_resources = {}
        total_xp = 0
        
        # Minden órára külön bányászunk
        for i in range(1, self.eventTime + 1):
            # Az aktuális mining limit alapján bányászunk
            hour_results = globalV.mining_system.mine(self.miningLimit)
            
            # Összesítjük az eredményeket
            for resource_id, amount in hour_results.items():
                total_mined_resources[resource_id] = total_mined_resources.get(resource_id, 0) + amount
            
            # XP számítás erre az órára
            hour_xp = globalV.mining_system.mining_reward_xp(1, hour_results)
            total_xp += hour_xp
            self.sumXP += hour_xp
            
            # Ellenőrizzük a szintlépést minden óra után
            if self.leveling(globalV, hour_xp):
                self.eventMessage = f"\n\t{self.name} törp az eddigi munkájának köszönhetően {self.sumXP} XP-t gyűjtött és a(z) {i}. óra után szintet lépett,\n\tezért innentől kezdve már óránként {self.miningLimit} egységnyi ércet tud kibányászni.\n"
                globalV.messages.append(self.eventMessage)
                self.sumXP = 0
        
        # Eredmények feldolgozása és üzenet generálása
        result_message = globalV.mining_system.process_mining_results(self, self.eventTime, total_mined_resources)
        globalV.messages.append(result_message)
        
        # XP üzenet
        self.eventMessage = f"\n\tA kemény munkája után, az előző szintlépése óta kapott {self.sumXP} XP-t, most {self.level}. szintű."
        globalV.messages.append(self.eventMessage)
        self.sumXP = 0
        
        # Nyersanyag készlet összesítés
        resources_summary = "\n\tA törp tábor összes nyersanyaga:"
        for resource_id, resource in globalV.resources.resource_types.items():
            amount = globalV.resources.get_resource_amount(resource_id)
            resources_summary += f"\n\t\t{amount} {resource.name}"
        globalV.messages.append(resources_summary + "\n")
        
        # Törp felszabadítása
        self.busy = False
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
            self.needXP += round(self.needXP * self.nextLvlMultiplier)
            self.level += 1
            self.miningLimit = round(self.miningLimit * globalV.miningLimitMultiplier)
            lvlUp = True
        return lvlUp
    
    
