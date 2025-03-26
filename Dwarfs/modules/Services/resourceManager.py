from modules.Models.resource import Resource

class ResourceManager:
    def __init__(self):
        # Alapértelmezett nyersanyagok definiálása
        self.resource_types = {
            'rock': Resource('Kő', 1, 1),
            'iron': Resource('Vasérc', 30, 5),
            'coal': Resource('Szén', 50, 8),
            'titan': Resource('Titánérc', 300, 20),
            'mythrill': Resource('Mythrillérc', 1000, 50)
        }
        
        # Nyersanyagok tárolása
        self.inventory = {resource_id: 0 for resource_id in self.resource_types}
    
    def add_resource(self, resource_id, amount):
        """Nyersanyag hozzáadása a készlethez"""
        if resource_id in self.inventory:
            self.inventory[resource_id] += amount
            return True
        return False
    
    def get_resource_amount(self, resource_id):
        """Lekérdezi egy adott nyersanyag mennyiségét"""
        return self.inventory.get(resource_id, 0)
    
    def get_all_resources(self):
        """Visszaadja az összes nyersanyag nevét és mennyiségét"""
        result = {}
        for resource_id, amount in self.inventory.items():
            resource = self.resource_types[resource_id]
            result[resource.name] = amount
        return result
    
    def add_new_resource_type(self, resource_id, name, rarity, base_value=1):
        """Új nyersanyagtípus hozzáadása a rendszerhez"""
        if resource_id not in self.resource_types:
            self.resource_types[resource_id] = Resource(name, rarity, base_value)
            self.inventory[resource_id] = 0
            return True
        return False
    
    def get_resources_by_rarity(self):
        """Visszaadja a nyersanyagtípusokat ritkaság szerinti sorrendben"""
        return sorted(self.resource_types.items(), key=lambda x: x[1].rarity, reverse=True)