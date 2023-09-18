import arcade

#Reaver boss
class Reaver(Enemy):
    def __init__(self, health, spritepath, speed):
        Enemy.__init__(self, health, spritepath, speed)

    def __str__(self):
        return f"Reaver: {self.health}, {self.spritepath}, {self.speed}"
    