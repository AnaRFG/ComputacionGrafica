from window import Window
from texture import Texture
from material import Material
from shader_program import ShaderProgram
from cube import Cube
from camera import Camera
from scene import Scene
import numpy as np

WIDTH, HEIGHT = 800, 600
window = Window(WIDTH, HEIGHT, "Basic Graphic Engine")

shader_program = ShaderProgram(window.ctx, 'shaders/basic.vert', 'shaders/basic.frag')

material = Material(shader_program)

cube1 = Cube((-2, 0, 0),(0, 45, 0),(1, 1, 1), name="Cube1")
cube2 = Cube((2, 0, 0),(0, 45, 0),(1, 1, 1), name="Cube2")

camera = Camera((0,0,6), (0,0,0), (0,1,0), 45, window.width / window.height, 0.1, 100.0)

scene = Scene(window.ctx, camera)

scene.add_object(cube1, material)
scene.add_object(cube2, material)
window.set_scene(scene)

window.run()