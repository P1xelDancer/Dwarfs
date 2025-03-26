import random

class Mining:
    def __init__(self, resources_manager):
        self.resources_manager = resources_manager
    
    def mine(self, mining_limit):
        """
        Bányászási folyamat végrehajtása
        
        Args:
            mining_limit: A kibányászható nyersanyagok maximális száma
            
        Returns:
            dict: A kibányászott nyersanyagok és mennyiségük
        """
        results = {}
        
        # Nyersanyagok lekérése ritkaság szerint csökkenő sorrendben
        resources_by_rarity = self.resources_manager.get_resources_by_rarity()
        
        for _ in range(mining_limit):
            # Véletlenszám generálás 1-től 1000-ig
            roll = random.randint(1, 1000)
            resource_found = False
            
            # Végigmegyünk a nyersanyagokon a legritkábbtól a leggyakoribbig
            for resource_id, resource in resources_by_rarity:
                # Ha a dobott érték kisebb vagy egyenlő, mint a nyersanyag ritkaságának reciproka * 1000
                # (pl. 1/1000 * 1000 = 1, tehát 0.1% esély)
                if roll <= 1000 / resource.rarity:
                    results[resource_id] = results.get(resource_id, 0) + 1
                    resource_found = True
                    break
            
            # Ha semmit nem találtunk, akkor az alapértelmezett nyersanyagot adjuk (kő)
            if not resource_found:
                results['rock'] = results.get('rock', 0) + 1
        
        return results
    
    def process_mining_results(self, dwarf, mining_hours, mining_results):
        """
        Feldolgozza a bányászat eredményét, frissíti a készleteket
        
        Args:
            dwarf: A bányászó törp
            mining_hours: Bányászással töltött órák
            mining_results: A bányászat eredménye

        Returns:
            str: Üzenet az eredményről
        """
        message = f"\n\t{dwarf.name} törp befejezte a bányászást. {mining_hours} óra alatt kitermelt:"
        
        # Nyersanyagok hozzáadása a készlethez
        for resource_id, amount in mining_results.items():
            self.resources_manager.add_resource(resource_id, amount)
            resource = self.resources_manager.resource_types[resource_id]
            message += f"\n\t\t{amount} {resource.name}-t"
        
        return message
    
    def mining_reward_xp(self, mining_hours, mining_results):
        """
        Kiszámítja a bányászatért járó XP-t
        
        Args:
            mining_hours: Bányászással töltött órák
            mining_results: A bányászat eredménye
            
        Returns:
            int: A kapott XP mennyisége
        """
        base_xp = 30 * mining_hours  # Alapvető XP óránként
        
        # Bónusz XP a ritkább nyersanyagokért
        bonus_xp = 0
        for resource_id, amount in mining_results.items():
            resource = self.resources_manager.resource_types[resource_id]
            # A ritkább nyersanyagok több bónusz XP-t adnak
            bonus_xp += amount * (resource.rarity / 30)
        
        return base_xp + int(bonus_xp)