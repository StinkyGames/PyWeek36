import arcade

#Sunbeam boss
class Sunbeam(Enemy):
    def __init__(self, health, spritepath, speed):
        Enemy.__init__(self, health, spritepath, speed)

    def __str__(self):
        return f"Sunbeam: {self.health}, {self.spritepath}, {self.speed}"