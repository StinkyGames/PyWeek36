import arcade

#Onslaught boss    
class Onslaught(Enemy):
    def __init__(self, health, spritepath, speed):
        Enemy.__init__(self, health, spritepath, speed)

    def __str__(self):
        return f"Onslaught: {self.health}, {self.spritepath}, {self.speed}"
    