from modules.Services.resourceManager import ResourceManager
from modules.Services.mining import Mining

class GlobalVars:
    def __init__(self):
        self.timeSlow = 6
        self.timeMedium = 3
        self.timeFast = 2
        self.realTimeMultiplier = 5
        self.dwarfs = {}
        self.messages = []
        self.resources = ResourceManager()
        self.mining = Mining(self.resources)
        self.miningLimitMultiplier = 1.2