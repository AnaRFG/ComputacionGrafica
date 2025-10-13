import math
import glm
from graphics import Graphics
import moderngl

class Scene:
    def __init__(self, ctx, camera):
        self.ctx = ctx
        self.objects = []
        self.graphics = {}
        self.camera = camera
        self.model = glm.mat4(1)
        self.view = camera.get_view_matrix()
        self.projection = camera.get_perspective_matrix()
        self.time = 0
        #para depth test
        self.ctx.enable(moderngl.DEPTH_TEST)

    def add_object(self, model, material):
        self.objects.append(model)
        self.graphics[model.name] = Graphics(self.ctx, model, material)

    def render(self): 
        self.time += 0.01 # en el constructor self.time = 0
        for obj in self.objects:
            if(obj.name != "Sprite"):
                obj.rotation += glm.vec3(0.8, 0.6, 0.4)
                obj.position.x += math.sin(self.time) * 0.01

            model = obj.get_model_matrix()
            mvp = self.projection * self.view * model
            self.graphics[obj.name].render({'Mvp': mvp})

    def on_mouse_click(self, u, v):
        ray = self.camera.raycast(u,v)

        for obj in self.objects:
            if obj.check_hit(ray.origin, ray.direction):
                print(f"¡Golpeaste el objeto {obj.name}!")

    def on_resize(self, width, height):
        self.ctx.viewport = (0, 0 , width, height)
        self.camera.projection = glm.perspective(glm.radians(45), width / height, 0.1, 100.0)
