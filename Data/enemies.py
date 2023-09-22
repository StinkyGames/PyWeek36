import arcade, random, math
from .player import Bullet

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
        self.hit_sound = arcade.load_sound(':resources:sounds/hit1.wav')
        self.death_sound = arcade.load_sound(':resources:sounds/hurt4.wav')
        self.health = health

    def move(self, player_sprite, time):
        # Position the start at the enemy's current location
        start_x = self.center_x
        start_y = self.center_y

        # Get the destination location for the bullet
        dest_x = player_sprite.center_x
        dest_y = player_sprite.center_y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Set the enemy to face the player.
        self.angle = math.degrees(angle) - 90

        if self.center_y < player_sprite.center_y:
            self.center_y += min(self.speed, player_sprite.center_y - self.center_y)
        elif self.center_y > player_sprite.center_y:
            self.center_y -= min(self.speed, self.center_y - player_sprite.center_y)
        if self.center_x < player_sprite.center_x:
            self.center_x += min(self.speed, player_sprite.center_x - self.center_x)
        elif self.center_x > player_sprite.center_x:
            self.center_x -= min(self.speed, self.center_x - player_sprite.center_x)

        self.physics_engine.sprites[self].body.position = (self.center_x, self.center_y)
        self.physics_engine.sprites[self].body.angle = self.angle
    
#Reaver boss
class Reaver(Enemy):
    def __init__(self, health, speed, physics_engine, screen_width, screen_height, enemy_bullet_list):
        Enemy.__init__(self, health, speed, physics_engine)
        arcade.Sprite.__init__(self, ":resources:images/space_shooter/playerShip1_green.png", 1.3)

        self.health = health
        self.speed = speed
        self.physics_engine = physics_engine
        self.screen_width = screen_width
        self.scree_height = screen_height
        self.enemy_bullet_list = enemy_bullet_list

        position_offset = 100 #This offset used to pad the jump point locations so that enemy doesn't clip outside of play area

        self.jump_interval = 7 #Time in seconds between jump to cardinal points
        self.jump_timer = 0
        self.move_point_incrementor = 0

        self.hit_sound = arcade.load_sound(':resources:sounds/hit1.wav')
        self.death_sound = arcade.load_sound(':resources:sounds/explosion2.wav')

        self.move_points = [
            [screen_width/2, screen_height - position_offset],
            [screen_width - position_offset, screen_height/2],
            [screen_width/2, 0 + position_offset],
            [0 + position_offset, screen_height/2]
        ]

        self.jump_sound = arcade.load_sound(':resources:sounds/fall3.wav')

        self.shoot_interval = 1
        self.shoot_timer = 0
        self.shoot_delay = 0 #Number used to delay the enmy from shooting for certain reasons (i.e. jumping)  

        self.shoot_sound = arcade.load_sound(':resources:sounds/laser2.wav')

    # Just put in the default enemy behavior code as a placeholder
    def move(self, player_sprite, time):
        # Position the start at the enemy's current location
        start_x = self.center_x
        start_y = self.center_y

        # Get the destination location for the bullet
        dest_x = player_sprite.center_x
        dest_y = player_sprite.center_y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Set the enemy to face the player.
        self.angle = math.degrees(angle) - 90

        if self.center_y < self.move_points[self.move_point_incrementor][1]:
            self.center_y += min(self.speed, self.move_points[self.move_point_incrementor][1] - self.center_y)
        elif self.center_y > self.move_points[self.move_point_incrementor][1]:
            self.center_y -= min(self.speed, self.center_y - self.move_points[self.move_point_incrementor][1])
        if self.center_x < self.move_points[self.move_point_incrementor][0]:
            self.center_x += min(self.speed, self.move_points[self.move_point_incrementor][0] - self.center_x)
        elif self.center_x > self.move_points[self.move_point_incrementor][0]:
            self.center_x -= min(self.speed, self.center_x - self.move_points[self.move_point_incrementor][0])

        self.jump_timer += time
        if self.jump_timer >= self.jump_interval:
            if(self.move_point_incrementor == 0):
                self.center_x = self.move_points[2][0] #Set new x
                self.center_y = self.move_points[2][1] #Set new y
                self.move_point_incrementor += 1
            elif(self.move_point_incrementor == 1):
                self.center_x = self.move_points[3][0] #Set new x
                self.center_y = self.move_points[3][1] #Set new y
                self.move_point_incrementor += 1
            elif(self.move_point_incrementor == 2):
                self.center_x = self.move_points[0][0] #Set new x
                self.center_y = self.move_points[0][1] #Set new y
                self.move_point_incrementor += 1
            elif(self.move_point_incrementor == 3):
                self.center_x = self.move_points[1][0] #Set new x
                self.center_y = self.move_points[1][1] #Set new y
                self.move_point_incrementor = 0
            arcade.play_sound(self.jump_sound)
            self.jump_timer = 0 #Reset timer
            self.shoot_delay = 1 #Add delay to shooting to let the player adjust

        self.shoot_timer += time
        if self.shoot_timer >= self.shoot_interval + self.shoot_delay:
            bullet = Bullet()
            bullet.center_x = start_x
            bullet.center_y = start_y
            bullet.angle = math.degrees(angle)
            bullet.angle = self.angle
            bullet.change_x = math.cos(angle) * bullet.speed
            bullet.change_y = math.sin(angle) * bullet.speed
            self.enemy_bullet_list.append(bullet)
            arcade.play_sound(self.shoot_sound)
            self.shoot_timer = 0
            self.shoot_delay = 0
            
        self.physics_engine.sprites[self].body.position = (self.center_x, self.center_y)
        self.physics_engine.sprites[self].body.angle = self.angle

#Onslaught boss    
class Onslaught(Enemy):
    def __init__(self, health, speed, physics_engine):
        Enemy.__init__(self, health, speed, physics_engine)
        arcade.Sprite.__init__(self, ":resources:images/space_shooter/playerShip1_green.png", 1.3)

        self.physics_engine = physics_engine

    def move(self, player_sprite, timer):
        print("No movement")


#Bulwark boss
class Bulwark(Enemy):
    def __init__(self, health, speed, physics_engine):
        Enemy.__init__(self, health, speed, physics_engine)
        arcade.Sprite.__init__(self, ":resources:images/space_shooter/playerShip1_green.png", 1.3)

        self.physics_engine = physics_engine
        
    def move(self, player_sprite, timer):
        print("No movement")


#Sunbeam boss
class Sunbeam(Enemy):
    def __init__(self, health, speed, physics_engine):
        Enemy.__init__(self, health, speed, physics_engine)
        arcade.Sprite.__init__(self, ":resources:images/space_shooter/playerShip1_green.png", 1.3)

        self.physics_engine = physics_engine

    def move(self, player_sprite, timer):
        print("No movement")



