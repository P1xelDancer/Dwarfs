class Resource:
    def __init__(self, name, rarity, base_value=1):
        self.name = name
        self.rarity = rarity
        self.base_value = base_value

    def __str__(self):
        return self.name