import arcade
#Enemy class that serves as base class for all enemies
class Enemy(arcade.Sprite):
    def __init__(self, health, speed):
        self.health = health
        self.speed = speed
    
    def follow_sprite(self, player_sprite):
        if self.center_y < player_sprite.center_y:
            self.center_y += min(self.speed, player_sprite.center_y - self.center_y)
        elif self.center_y > player_sprite.center_y:
            self.center_y -= min(self.speed, self.center_y - player_sprite.center_y)

        if self.center_x < player_sprite.center_x:
            self.center_x += min(self.speed, player_sprite.center_x - self.center_x)
        elif self.center_x > player_sprite.center_x:
            self.center_x -= min(self.speed, self.center_x - player_sprite.center_x)

#Generic drone enemy
class Drone(Enemy):
    def __init__(self, health, speed):
        Enemy.__init__(self, health, speed)
        arcade.Sprite.__init__(self, "Sprites/player.png", 0.2)

    def __str__(self):
        return f"Drone: {self.health}, {self.spritepath}, {self.speed}"
    
#Reaver boss
class Reaver(Enemy):
    def __init__(self, health, spritepath, speed):
        Enemy.__init__(self, health, spritepath, speed)

    def __str__(self):
        return f"Reaver: {self.health}, {self.spritepath}, {self.speed}"

#Onslaught boss    
class Onslaught(Enemy):
    def __init__(self, health, spritepath, speed):
        Enemy.__init__(self, health, spritepath, speed)

    def __str__(self):
        return f"Onslaught: {self.health}, {self.spritepath}, {self.speed}"

#Bulwark boss
class Bulwark(Enemy):
    def __init__(self, health, spritepath, speed):
        Enemy.__init__(self, health, spritepath, speed)

    def __str__(self):
        return f"Bulwark: {self.health}, {self.spritepath}, {self.speed}"

#Sunbeam boss
class Sunbeam(Enemy):
    def __init__(self, health, spritepath, speed):
        Enemy.__init__(self, health, spritepath, speed)

    def __str__(self):
        return f"Sunbeam: {self.health}, {self.spritepath}, {self.speed}"



