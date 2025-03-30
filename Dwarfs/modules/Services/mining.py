import random

class Mining:
    def __init__(self, resourceManager):
        self.resourceManager = resourceManager
    
    def mine(self, miningLimit):
        """
        Bányászási folyamat végrehajtása
        
        Args:
            mining_limit: A kibányászható nyersanyagok maximális száma
            
        Returns:
            dict: A kibányászott nyersanyagok és mennyiségük
        """
        results = {}
        
        # Nyersanyagok lekérése ritkaság szerint csökkenő sorrendben
        resourcesByRarity = self.resourceManager.getResourcesByRarity()
        
        for _ in range(miningLimit):
            # Véletlenszám generálás 1-től 1000-ig
            roll = random.randint(1, 1000)
            resourceFound = False
            
            # Végigmegyünk a nyersanyagokon a legritkábbtól a leggyakoribbig
            for resourceId, resource in resourcesByRarity:
                # Ha a dobott érték kisebb vagy egyenlő, mint a nyersanyag ritkaságának reciproka * 1000
                # (pl. 1/1000 * 1000 = 1, tehát 0.1% esély)
                if roll <= 1000 / resource.rarity:
                    results[resourceId] = results.get(resourceId, 0) + 1
                    resourceFound = True
                    break
            
            # Ha semmit nem találtunk, akkor az alapértelmezett nyersanyagot adjuk (kő)
            if not resourceFound:
                results['rock'] = results.get('rock', 0) + 1
        
        return results
    
    def processMiningResults(self, dwarf, miningHours, miningResults):
        """
        Feldolgozza a bányászat eredményét, frissíti a készleteket
        
        Args:
            dwarf: A bányászó törp
            mining_hours: Bányászással töltött órák
            mining_results: A bányászat eredménye

        Returns:
            str: Üzenet az eredményről
        """
        message = f"\n\t{dwarf.name} törp befejezte a bányászást. {miningHours} óra alatt kitermelt:"
        
        # Nyersanyagok hozzáadása a készlethez
        for resourceId, amount in miningResults.items():
            self.resourceManager.addResource(resourceId, amount)
            resource = self.resourceManager.resourceTypes[resourceId]
            message += f"\n\t\t{amount} {resource.name}-t"
        
        return message
    
    def miningRewardXp(self, miningHours, miningResults):
        """
        Kiszámítja a bányászatért járó XP-t
        
        Args:
            mining_hours: Bányászással töltött órák
            mining_results: A bányászat eredménye
            
        Returns:
            int: A kapott XP mennyisége
        """
        baseXp = 30 * miningHours  # Alapvető XP óránként
        
        # Bónusz XP a ritkább nyersanyagokért
        bonusXp = 0
        for resourceId, amount in miningResults.items():
            resource = self.resourceManager.resourceTypes[resourceId]
            # A ritkább nyersanyagok több bónusz XP-t adnak
            bonusXp += amount * (resource.rarity / 30)
        
        return baseXp + int(bonusXp)