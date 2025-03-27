from modules.Models.resource import Resource

class ResourceManager:
    def __init__(self):
        # Alapértelmezett nyersanyagok definiálása
        self.resourceTypes = {
            'rock': Resource('Kő', 1, 1),
            'iron': Resource('Vasérc', 30, 5),
            'coal': Resource('Szén', 50, 8),
            'titan': Resource('Titánérc', 300, 20),
            'mythrill': Resource('Mythrillérc', 1000, 50)
        }
        
        # Nyersanyagok tárolása
        self.inventory = {resourceId: 0 for resourceId in self.resourceTypes}
    
    def addResource(self, resourceId, amount):
        """Nyersanyag hozzáadása a készlethez"""
        if resourceId in self.inventory:
            self.inventory[resourceId] += amount
            return True
        return False
    
    def getResourceAmount(self, resourceId):
        """Lekérdezi egy adott nyersanyag mennyiségét"""
        return self.inventory.get(resourceId, 0)
    
    def getAllResources(self):
        """Visszaadja az összes nyersanyag nevét és mennyiségét"""
        result = {}
        for resource_id, amount in self.inventory.items():
            resource = self.resourceTypes[resource_id]
            result[resource.name] = amount
        return result
    
    # def addNewResourceType(self, resourceId, name, rarity, base_value=1):
    #     """Új nyersanyagtípus hozzáadása a rendszerhez"""
    #     if resourceId not in self.resourceTypes:
    #         self.resourceTypes[resourceId] = Resource(name, rarity, base_value)
    #         self.inventory[resourceId] = 0
    #         return True
    #     return False
    
    def getResourcesByRarity(self):
        """Visszaadja a nyersanyagtípusokat ritkaság szerinti sorrendben"""
        return sorted(self.resourceTypes.items(), key=lambda x: x[1].rarity, reverse=True)