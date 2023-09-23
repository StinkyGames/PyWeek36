from arcade.experimental.shadertoy import Shadertoy


class ExplosionMaker:
    def __init__(self, size, position):
        self.shadertoy: Shadertoy = Shadertoy.create_from_file(size, "Shaders/explosion.glsl")
        self.shadertoy.program['pos'] = position
        self.shadertoy.program['color'] = (0.0, 1.0, 0.7)
        self.time = 0.0
        self.position = position

    def update(self, time):
        self.time += time

    def render(self):
        self.shadertoy.render(time=self.time)