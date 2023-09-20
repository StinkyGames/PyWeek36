import arcade, arcade.gui, random, math
from .player import *
from .enemies import *
from .level_select import *

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

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.setup()

    def setup(self):
        self.player = Player(self.screen_width, self.screen_height)
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.level = LevelSelectView(self.screen_width, self.screen_height)

        for i in range(0, 10):
            self.drone = Drone(10, 1)
            self.drone.center_x = random.randrange(self.screen_width)
            self.drone.center_y = random.randrange(self.screen_height)

            self.enemy_list.append(self.drone)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(
            self.screen_width // 2, self.screen_height // 2,
            self.screen_width, self.screen_height,
            self.background
        )

        self.player.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()

        hull_display = f"Hull: {self.player.hull}"
        arcade.draw_text(hull_display, 10, 30, arcade.color.WHITE, 14)

        boss_display = f"Boss: {self.boss}"
        arcade.draw_text(boss_display, self.screen_width - 200, 30, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        self.player.update()
        self.enemy_list.update()
        self.bullet_list.update()

        for enemy in self.enemy_list:
            enemy.follow_sprite(self.player)

        # Bullets kill drones
        for bullet in self.bullet_list:
            drone_hit = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            for enemy in drone_hit:
                enemy.remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()

        hit_list = arcade.check_for_collision_with_list(self.player, self.enemy_list)

        for enemy in hit_list:
            enemy.remove_from_sprite_lists()
            self.player.hull -= 1

        if self.player.hull == 0:
            from .gameover import GameOverView
            game_over_view = GameOverView(self.screen_width, self.screen_height)
            self.window.show_view(game_over_view)

        for self.bullet in self.bullet_list:
            if self.bullet.bottom > self.screen_width or self.bullet.top < 0 or self.bullet.right < 0 or self.bullet.left > self.screen_width:
                self.bullet.remove_from_sprite_lists()

        # Add friction
        if self.player.change_x > self.player.friction:
            self.player.change_x -= self.player.friction
        elif self.player.change_x < -self.player.friction:
            self.player.change_x += self.player.friction
        else:
            self.player.change_x = 0

        if self.player.change_y > self.player.friction:
            self.player.change_y -= self.player.friction
        elif self.player.change_y < -self.player.friction:
            self.player.change_y += self.player.friction
        else:
            self.player.change_y = 0

        # Apply acceleration based on the keys pressed
        if self.up_pressed and not self.down_pressed:
            self.player.change_y += self.player.acceleration_rate
        elif self.down_pressed and not self.up_pressed:
            self.player.change_y += -self.player.acceleration_rate
        if self.left_pressed and not self.right_pressed:
            self.player.change_x += -self.player.acceleration_rate
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x += self.player.acceleration_rate

        if self.player.change_x > self.player.max_speed:
            self.player.change_x = self.player.max_speed
        elif self.player.change_x < -self.player.max_speed:
            self.player.change_x = -self.player.max_speed
        if self.player.change_y > self.player.max_speed:
            self.player.change_y = self.player.max_speed
        elif self.player.change_y < -self.player.max_speed:
            self.player.change_y = -self.player.max_speed

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
        self.player.face_point((x,y))
    
    def on_mouse_press(self, x, y, button, modifiers):
        self.bullet = Bullet()
        self.bullet.center_x = self.player.center_x
        self.bullet.center_y = self.player.center_y
        # the math for where and how the bullets shoot
        x_diff = x - self.player.center_x
        y_diff = y - self.player.center_y
        angle = math.atan2(y_diff, x_diff)
        self.bullet.angle = self.player.angle
        self.bullet.change_x = math.cos(angle) * self.bullet.speed
        self.bullet.change_y = math.sin(angle) * self.bullet.speed
        self.bullet_list.append(self.bullet)
