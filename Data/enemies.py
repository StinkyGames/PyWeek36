import arcade, random, math

#Enemy class that serves as base class for all enemies
class Enemy(arcade.Sprite):
    def __init__(self, health, speed, physics_engine):
        self.health = health
        self.speed = speed
        self.physics_engine = physics_engine

class EnemyBullet(arcade.Sprite):
    def __init__(self):
        super().__init__(':resources:images/space_shooter/laserRed01.png')
        # set initial values
        self.speed = 10
        self.scale = 1

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
        arcade.Sprite.__init__(self, ":resources:images/space_shooter/playerShip2_orange.png", 1.3)

        self.health = health
        self.speed = speed
        self.physics_engine = physics_engine
        self.screen_width = screen_width
        self.scree_height = screen_height
        self.enemy_bullet_list = enemy_bullet_list

        position_offset = 100 #This offset used to pad the jump point locations so that enemy doesn't clip outside of play area

        self.jump_interval = 3.5 #Time in seconds between jump to cardinal points
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

        self.shoot_interval = 0.5
        self.shoot_timer = 0
        self.shoot_delay = 0 #Number used to delay the enemy from shooting for certain reasons (i.e. jumping)  

        self.shoot_sound = arcade.load_sound(':resources:sounds/laser2.wav')

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
            if self.move_point_incrementor == 0:
                self.center_x = self.move_points[2][0]
                self.center_y = self.move_points[2][1]
            elif self.move_point_incrementor == 1:
                self.center_x = self.move_points[3][0]
                self.center_y = self.move_points[3][1]
            elif self.move_point_incrementor == 2:
                self.center_x = self.move_points[0][0]
                self.center_y = self.move_points[0][1]
            elif self.move_point_incrementor == 3:
                self.center_x = self.move_points[1][0]
                self.center_y = self.move_points[1][1]
            self.move_point_incrementor += 1
            if self.move_point_incrementor > 3:
                self.move_point_incrementor = 0
            arcade.play_sound(self.jump_sound)
            self.jump_timer = 0 #Reset timer
            self.shoot_delay = 1 #Add delay to shooting to let the player adjust

        self.shoot_timer += time
        if self.shoot_timer >= self.shoot_interval + self.shoot_delay:
            bullet = EnemyBullet()
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
    def __init__(self, health, speed, physics_engine, screen_width, screen_height, enemy_bullet_list):
        Enemy.__init__(self, health, speed, physics_engine)
        arcade.Sprite.__init__(self, ":resources:images/space_shooter/playerShip1_orange.png", 1.3)

        self.physics_engine = physics_engine
        self.screen_width = screen_width
        self.scree_height = screen_height
        self.hit_sound = arcade.load_sound(':resources:sounds/hit1.wav')
        self.death_sound = arcade.load_sound(':resources:sounds/explosion2.wav')

        position_offset = 100

        self.move_point_incrementor = 0

        self.enemy_bullet_list = enemy_bullet_list

        self.shoot_interval = 0.3
        self.shoot_timer = 0
        self.shoot_sound = arcade.load_sound(':resources:sounds/laser2.wav')

        self.move_points = [
            [0 + position_offset, screen_height - position_offset], #Top left
            [screen_width - position_offset, screen_height - position_offset] #Top right
        ]

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

        #If we reached the destination, reverse to other point
        if self.center_x == self.move_points[self.move_point_incrementor][0]:
            if self.move_point_incrementor == 1:
                self.move_point_incrementor = 0
            else:
                self.move_point_incrementor = 1

        self.shoot_timer += time
        if self.shoot_timer >= self.shoot_interval:
            bullet = EnemyBullet()
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


#Bulwark boss
class Bulwark(Enemy):
    def __init__(self, health, speed, physics_engine, screen_width, screen_height):
        Enemy.__init__(self, health, speed, physics_engine)
        arcade.Sprite.__init__(self, ":resources:images/space_shooter/playerShip3_orange.png", 1.3)

        self.health = health
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.physics_engine = physics_engine

        self.hit_sound = arcade.load_sound(':resources:sounds/hit1.wav')
        self.death_sound = arcade.load_sound(':resources:sounds/explosion2.wav')

        self.physics_engine = physics_engine

        self.ram_timer = 0
        self.ram_interval = 1.5 # Ram frequency
        self.ram_delay = 0.5 # Ram cooldown
        self.speed_boost = 20 #Multiplicative
        self.charging = False

        self.stored_player_x = 0
        self.stored_player_y = 0
        self.speed_original = self.speed
        
    def move(self, player_sprite, time):
        # Position the start at the enemy's current location
        start_x = self.center_x
        start_y = self.center_y

        self.ram_timer += time

        if self.ram_timer >= self.ram_interval + self.ram_delay and not self.charging:
            self.stored_player_x = player_sprite.center_x
            self.stored_player_y = player_sprite.center_y
            self.charging = True
            self.speed_original = self.speed
            self.speed *= self.speed_boost

        if self.charging:
            dest_x = self.stored_player_x
            dest_y = self.stored_player_y
        else:
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

        if not self.charging:
            if self.center_y < player_sprite.center_y:
                self.center_y += min(self.speed, player_sprite.center_y - self.center_y)
            elif self.center_y > player_sprite.center_y:
                self.center_y -= min(self.speed, self.center_y - player_sprite.center_y)
            if self.center_x < player_sprite.center_x:
                self.center_x += min(self.speed, player_sprite.center_x - self.center_x)
            elif self.center_x > player_sprite.center_x:
                self.center_x -= min(self.speed, self.center_x - player_sprite.center_x)
        else:
            if abs(self.center_x - self.stored_player_x) <= 20 and abs(self.center_y - self.stored_player_y) <= 20:
                self.charging = False
                self.ram_timer = 0
                self.speed = self.speed_original
            else:
                # How far are we?
                distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)
                self.center_x = start_x
                self.center_y = start_y
                speed = min(self.speed, distance)
                self.change_x = math.cos(angle) * speed
                self.change_y = math.sin(angle) * speed

        if self.right > self.screen_width:
            self.right = self.screen_width
            self.change_x = 0 # Zero x speed
        elif self.left < 0:
            self.left = 0
            self.change_x = 0
        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0
        elif self.top > self.screen_height:
            self.top = self.screen_height
            self.change_y = 0

        self.physics_engine.sprites[self].body.position = (self.center_x, self.center_y)
        self.physics_engine.sprites[self].body.angle = self.angle


#Sunbeam boss
class Sunbeam(Enemy):
    def __init__(self, health, speed, physics_engine):
        Enemy.__init__(self, health, speed, physics_engine)
        arcade.Sprite.__init__(self, ":resources:images/space_shooter/playerShip1_green.png", 1.3)

        self.physics_engine = physics_engine

        self.hit_sound = arcade.load_sound(':resources:sounds/hit1.wav')
        self.death_sound = arcade.load_sound(':resources:sounds/explosion2.wav')

    def move(self, player_sprite, timer):
        print("No movement")



