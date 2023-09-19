import arcade, random
from enemies import Drone
from player import Player
from arcade.pymunk_physics_engine import PymunkPhysicsEngine

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Pymunk test"

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.setup()

        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

    def setup(self):
        self.enemy_list = arcade.SpriteList()
        self.player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)

        for i in range(5):
            x = random.randrange(SCREEN_WIDTH)
            y = random.randrange(SCREEN_HEIGHT)
            drone = Drone(10, 1)
            drone.center_x = x
            drone.center_y = y
            self.enemy_list.append(drone)

        damping = 0.5
        gravity = (0, 0)
        self.physics_engine = PymunkPhysicsEngine(damping=damping, gravity=gravity)

        #Found this code at https://api.arcade.academy/en/latest/examples/pymunk_demo_top_down.html#pymunk-demo-top-down

        # def enemy_enemy_hit_handler(sprite_a, sprite_b, arbiter, space, data):
        #     shape = arbiter.shapes[0]
        #     sprite = self.physics_engine.get_sprite_for_shape(shape)

        # self.physics_engine.add_collision_handler("enemy", "enemy", post_handler=enemy_enemy_hit_handler)
        
        self.physics_engine.add_sprite(self.player, friction=0.6, moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF, damping=0.05, collision_type="player", max_velocity=225)
        self.physics_engine.add_sprite_list(self.enemy_list, friction=0.8, moment_of_intertia=PymunkPhysicsEngine.MOMENT_INF, damping=0.1, collision_type="enemy")


    def on_draw(self):
        self.clear()
        self.player.draw()
        self.enemy_list.draw()

    def on_update(self, delta_time):
        self.player.change_x = 0
        self.player.change_y = 0

        self.physics_engine.step()

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

        print()
        # Apply acceleration based on the keys pressed
        if self.up_pressed and not self.down_pressed:
            force = (9, 1000)
            self.physics_engine.apply_force(self.player, force)

        elif self.down_pressed and not self.up_pressed:
            force = (0, -1000)
            self.physics_engine.apply_force(self.player, force)

        if self.left_pressed and not self.right_pressed:
            #self.player.change_x = -5
            force = (-1000, 0)
            self.physics_engine.apply_force(self.player, force)

        elif self.right_pressed and not self.left_pressed:
            force = (1000, 0)
            self.physics_engine.apply_force(self.player, force)


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

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False

def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    arcade.run()


if __name__ == "__main__":
    main()