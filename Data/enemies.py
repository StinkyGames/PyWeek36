import arcade
#Enemy class that serves as base class for all enemies
class Enemy(arcade.Sprite):
    def __init__(self, health, speed, physics_engine):
        self.health = health
        self.speed = speed
        self.physics_engine = physics_engine

#Generic drone enemy
class Drone(Enemy):
    def __init__(self, health, speed, physics_engine):
        Enemy.__init__(self, health, speed, physics_engine)
        arcade.Sprite.__init__(self, ":resources:images/space_shooter/playerShip1_green.png", 0.7)

        self.physics_engine = physics_engine

    def move(self, player_sprite):
        if self.center_y < player_sprite.center_y:
            self.center_y += min(self.speed, player_sprite.center_y - self.center_y)
            self.physics_engine.sprites[self].body.position = (self.center_x, self.center_y)
        elif self.center_y > player_sprite.center_y:
            self.center_y -= min(self.speed, self.center_y - player_sprite.center_y)
            self.physics_engine.sprites[self].body.position = (self.center_x, self.center_y)
        if self.center_x < player_sprite.center_x:
            self.center_x += min(self.speed, player_sprite.center_x - self.center_x)
            self.physics_engine.sprites[self].body.position = (self.center_x, self.center_y)
        elif self.center_x > player_sprite.center_x:
            self.center_x -= min(self.speed, self.center_x - player_sprite.center_x)
            self.physics_engine.sprites[self].body.position = (self.center_x, self.center_y)
        self.face_point((player_sprite.center_x, player_sprite.center_y))
    
#Reaver boss
class Reaver(Enemy):
    def __init__(self, health, speed, physics_engine):
        Enemy.__init__(self, health, speed, physics_engine)
        arcade.Sprite.__init__(self, ":resources:images/space_shooter/playerShip1_green.png", 0.7)

        self.physics_engine = physics_engine


#Onslaught boss    
class Onslaught(Enemy):
    def __init__(self, health, speed, physics_engine):
        Enemy.__init__(self, health, speed, physics_engine)
        arcade.Sprite.__init__(self, ":resources:images/space_shooter/playerShip1_green.png", 0.7)

        self.physics_engine = physics_engine

    def move(self, player_sprite):
        print("No movement")


#Bulwark boss
class Bulwark(Enemy):
    def __init__(self, health, speed, physics_engine):
        Enemy.__init__(self, health, speed, physics_engine)
        arcade.Sprite.__init__(self, ":resources:images/space_shooter/playerShip1_green.png", 0.7)

        self.physics_engine = physics_engine
        
    def move(self, player_sprite):
        print("No movement")


#Sunbeam boss
class Sunbeam(Enemy):
    def __init__(self, health, speed, physics_engine):
        Enemy.__init__(self, health, speed, physics_engine)
        arcade.Sprite.__init__(self, ":resources:images/space_shooter/playerShip1_green.png", 0.7)

        self.physics_engine = physics_engine

    def move(self, player_sprite):
        print("No movement")



