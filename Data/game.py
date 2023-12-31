import arcade, arcade.gui, random, math
from .player import *
from .enemies import *
from .level_select import *
from .explosion import ExplosionMaker
from arcade.pymunk_physics_engine import PymunkPhysicsEngine

class GameView(arcade.View):
    def __init__(self, screen_width, screen_height, boss):
        super().__init__()
        self.window.set_mouse_visible(True)
        self.window.set_location(int((arcade.get_display_size()[0] - screen_width) / 2),
                          int((arcade.get_display_size()[1] - screen_height) / 2))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.boss = boss
        self.background = arcade.load_texture(f'Assets/{self.boss}.png')
        self.shoot_sound = arcade.load_sound(':resources:sounds/laser1.wav')

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.mouse_x = (int)(self.screen_width / 2)
        self.mouse_y = self.screen_height

        self.explosion_list = []
        self.num_enemies_spawned = 0

        self.setup()

    def setup(self):
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.spawn_timer = 0  # Timer to control drone spawning
        self.spawn_interval = 1  # Time in seconds between drone spawns
        self.kill_count = 0 # Tracks the number of drones killed
        self.max_kills = 50 # Number of drones to die before boss spawns
        self.boss_spawned = False # Flag to spawn the boss
        self.boss_spawn_timer = 0  # Initialize a timer for boss spawning
        self.boss_spawn_delay = 3  # Set the delay in seconds
        
        damping = 0.5
        gravity = (0, 0)
        self.physics_engine = PymunkPhysicsEngine(damping=damping, gravity=gravity)

        self.player = Player(self.screen_width, self.screen_height, self.physics_engine)
        self.player_max_health = self.player.hull

        if self.boss == "Bulwark":
            self.boss_class = Bulwark(75, 0.5, self.physics_engine, self.screen_width, self.screen_height)
            self.boss_max_health = self.boss_class.health
        elif self.boss == "Reaver":
            self.boss_class = Reaver(50, 1.7, self.physics_engine, self.screen_width, self.screen_height, self.enemy_bullet_list)
            self.boss_max_health = self.boss_class.health
        elif self.boss == "Onslaught":
            self.boss_class = Onslaught(50, 4, self.physics_engine, self.screen_width, self.screen_height, self.enemy_bullet_list)
            self.boss_max_health = self.boss_class.health

        #Found this code at https://api.arcade.academy/en/latest/examples/pymunk_demo_top_down.html#pymunk-demo-top-down
        self.physics_engine.add_sprite(self.player, collision_type="player")
        self.physics_engine.add_sprite_list(self.enemy_list, collision_type="enemy")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(
            self.screen_width // 2, self.screen_height // 2,
            self.screen_width, self.screen_height,
            self.background
        )

        self.player.draw()
        self.enemy_list.draw()
        self.enemy_bullet_list.draw()
        self.bullet_list.draw()

        for explosion in self.explosion_list:
            explosion.render()

        arcade.draw_text(f'Drive Recharge: {round((self.kill_count / self.max_kills) * 100)}%', 10, self.screen_height - 30, arcade.color.WHITE, 14)
        arcade.draw_text(f"Player Hull: {round((self.player.hull / self.player_max_health) * 100)}%", self.screen_width - 200, self.screen_height - 30, arcade.color.WHITE, 14)
        arcade.draw_text(f'Boss: {self.boss}', self.screen_width - 200, 30, arcade.color.WHITE, 14)
        if self.kill_count >= self.max_kills:
            arcade.draw_text(f'Boss Hull: {round((self.boss_class.health / self.boss_max_health) * 100)}%', (self.screen_width // 2) - 50, self.screen_height - 30, arcade.color.WHITE, 14)
        if self.kill_count >= self.max_kills and self.boss_spawned == False:
            arcade.draw_text(f'{self.boss} Incoming!', (self.screen_width // 2) - 100, self.screen_height // 2, arcade.color.WHITE, 24)

    def on_update(self, delta_time):
        self.physics_engine.step()
        self.bullet_list.update()
        self.enemy_bullet_list.update()
        self.enemy_list.update()
        self.player.move(self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed, self.mouse_x, self.mouse_y)

        # Spawn boss
        if self.kill_count >= self.max_kills and not self.boss_spawned:
            self.boss_spawn_timer += delta_time
            if self.boss_spawn_timer >= self.boss_spawn_delay:
                self.boss_spawned = True
                self.spawn_boss()

        # Check if boss dies
        if self.boss_spawned:
            if self.boss_class.health <= 0:
                from .level_select import LevelSelectView
                from . import values
                values.hide_boss.append(self.boss) # Add boss name to a dictionary to remove it from level select
                level_select_view = LevelSelectView(self.screen_width, self.screen_height, values.hide_boss)
                self.window.show_view(level_select_view)

        # Spawn drones over time
        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_interval and self.num_enemies_spawned < self.max_kills:
            max_drones_to_spawn = min(self.max_kills - self.num_enemies_spawned, 4)
            drones_to_spawn = random.randint(1, max_drones_to_spawn)
            for _ in range(drones_to_spawn):
                drone = Drone(1, 2, self.physics_engine)
                #Define edges of screen
                edge = random.choice(["top", "bottom", "left", "right"])
                if edge == "top":
                    drone.center_x = random.randrange(self.screen_width)
                    drone.center_y = self.screen_height
                elif edge == "bottom":
                    drone.center_x = random.randrange(self.screen_width)
                    drone.center_y = 0
                elif edge == "left":
                    drone.center_x = 0
                    drone.center_y = random.randrange(self.screen_height)
                elif edge == "right":
                    drone.center_x = self.screen_width
                    drone.center_y = random.randrange(self.screen_height)
                self.physics_engine.add_sprite(drone, collision_type="enemy")
                self.enemy_list.append(drone)
            self.num_enemies_spawned += drones_to_spawn
            self.spawn_timer = 0  # Reset the timer


        for enemy in self.enemy_list:
            enemy.move(self.player, delta_time)

        # Bullets kill drones
        for bullet in self.bullet_list:
            drone_hit = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            for enemy in drone_hit:
                enemy.health -= 1
                if enemy.health <= 0:
                    arcade.play_sound(enemy.death_sound)
                    enemy.remove_from_sprite_lists()
                    self.explosion_list.append(ExplosionMaker(self.window.get_size(), enemy.position))
                    self.kill_count += 1
                else:
                    arcade.play_sound(enemy.hit_sound)
                bullet.remove_from_sprite_lists()

        # Enemy bullets hurt player
        for bullet in self.enemy_bullet_list:
            player_hit = arcade.check_for_collision(bullet, self.player)
            if player_hit:
                arcade.play_sound(self.player.hit_sound)
                self.player.hull -= 1
                bullet.remove_from_sprite_lists()

        for explosion in self.explosion_list:
            explosion.update(delta_time)
            if explosion.time > .9:
                self.explosion_list.remove(explosion)

        hit_list = arcade.check_for_collision_with_list(self.player, self.enemy_list)

        for enemy in hit_list:
            if isinstance(enemy, Drone):
                enemy.health -= 1
                self.player.hull -= 1
                if enemy.health <= 0:
                    arcade.play_sound(self.player.hit_sound)
                    enemy.remove_from_sprite_lists()
                    self.explosion_list.append(ExplosionMaker(self.window.get_size(), enemy.position))
                    self.kill_count += 1
                else:
                    arcade.play_sound(enemy.hit_sound)
            else:
                self.player.hull = 0

        if self.player.hull <= 0:
            arcade.play_sound(self.player.death_sound)
            from .gameover import GameOverView
            game_over_view = GameOverView(self.screen_width, self.screen_height)
            self.window.show_view(game_over_view)

        for bullet in self.bullet_list:
            if bullet.bottom > self.screen_width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.screen_width:
                bullet.remove_from_sprite_lists()

        for bullet in self.enemy_bullet_list:
            if bullet.bottom > self.screen_width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.screen_width:
                bullet.remove_from_sprite_lists()

    def spawn_boss(self):
        boss = self.boss_class
        # Set the boss's initial position and other attributes as needed
        boss.center_x = self.screen_width // 2
        boss.center_y = self.screen_height
        # Add the boss to the appropriate sprite list
        self.enemy_list.append(boss)
        self.physics_engine.add_sprite(boss, collision_type="enemy")
        # Move to the center of the screen
        target_x = self.screen_width // 2
        target_y = self.screen_height // 2
        angle = math.atan2(target_y - boss.center_y, target_x - boss.center_x)
        velocity = boss.speed  # Adjust this value for boss's speed
        boss.change_x = math.cos(angle) * velocity
        boss.change_y = math.sin(angle) * velocity

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True
         # for easy restart - can remove from final release
        if key == arcade.key.X:
            from .gameover import GameOverView
            game_over_view = GameOverView(self.screen_width, self.screen_height)
            self.window.show_view(game_over_view)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            bullet = Bullet()
            bullet.center_x = self.player.center_x
            bullet.center_y = self.player.center_y
            # the math for where and how the bullets shoot
            x_diff = x - self.player.center_x
            y_diff = y - self.player.center_y
            angle = math.atan2(y_diff, x_diff)
            bullet.angle = math.degrees(angle)
            bullet.change_x = math.cos(angle) * bullet.speed
            bullet.change_y = math.sin(angle) * bullet.speed
            self.bullet_list.append(bullet)
            arcade.play_sound(self.shoot_sound)