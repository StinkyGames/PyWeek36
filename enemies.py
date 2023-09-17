#Enemy class that serves as base class for all enemies
class Enemy:
    def __init__(self, name, health, spritepath):
        self.name = name
        self.health = health
        self.spritepath = spritepath

    def __str__(self):
        return f"{self.name}: {self.health}, {self.spritepath}"

#Generic drone enemy
class Drone(Enemy):
    def __init__(self, name, health, spritepath):
        super().__init__(self, name, health, spritepath)
    
#Reaver boss
class Reaver(Enemy):
    def __init__(self, name, health, spritepath):
        super().__init__(self, name, health, spritepath)

#Onslaught boss    
class Onslaught(Enemy):
    def __init__(self, name, health, spritepath):
        super().__init__(self, name, health, spritepath)

#Bulwark boss
class Bulwark(Enemy):
    def __init__(self, name, health, spritepath):
        super().__init__(self, name, health, spritepath)

#Sunbeam boss
class Sunbeam(Enemy):
    def __init__(self, name, health, spritepath):
        super().__init__(self, name, health, spritepath)



