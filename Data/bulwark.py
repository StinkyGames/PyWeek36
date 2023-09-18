import arcade

#Bulwark boss
class Bulwark(Enemy):
    def __init__(self, health, spritepath, speed):
        Enemy.__init__(self, health, spritepath, speed)

    def __str__(self):
        return f"Bulwark: {self.health}, {self.spritepath}, {self.speed}"