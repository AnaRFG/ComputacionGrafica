import math
import glm
from graphics import Graphics, ComputeGraphics
import moderngl
from raytracer import RayTracer, RayTracerGPU
import numpy as np
from model import Model

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

    def start(self):
        print("Start!!")

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

class RaySceneGPU(Scene):
    def __init__(self, ctx, camera, width, height, output_model, output_material):
        
        self.output_graphics = Graphics(ctx, output_model, output_material)
        self.raytracer = RayTracerGPU(ctx, camera, width, height, self.output_graphics)
        
        super().__init__(ctx, camera)

    def add_object(self, model, material):
        self.objects.append(model)
        self.graphics[model.name] = ComputeGraphics(self.ctx, model, material)  

    def start(self):
        print("Start Raytracing!")
        self.primitives = []
        n = len(self.objects)
        self.models_f = np.zeros((n, 16), dtype='f4')
        self.inv_f = np.zeros((n, 16), dtype='f4')
        self.mats_f = np.zeros((n, 4), dtype='f4') # reflectividad + colorRGB
        
        self._update_matrix()
        self._matrix_to_ssbo()
        self.started = True

    def render(self):
        self.time += 0.01
        for obj in self.objects:
            if obj.animated:
                obj.rotation += glm.vec3(0.8, 0.6, 0.4)
                obj.position.x += math.sin(self.time) * 0.01

        if(self.raytracer is not None):
            self._update_matrix()
            self._matrix_to_ssbo()
            self.raytracer.run()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.width, self.height = width, height
        self.camera.aspect = width / height

    def _update_matrix(self):
        self.primitives = []

        for i, (name, graphics) in enumerate(self.graphics.items()):
            graphics.create_primitive(self.primitives)
            graphics.create_transformation_matrix(self.models_f, i)
            graphics.create_material_matrix(self.mats_f, i)
            
             #FORZAMOS A GENERAR MATRIZ INVERSA REAL
            model_matrix = graphics._Graphics__model.get_model_matrix()
            inverse_matrix = glm.inverse(model_matrix)
            self.inv_f[i, :] = np.array(inverse_matrix.to_list(), dtype="f4").reshape(16)


    def _matrix_to_ssbo(self):
        self.raytracer.matrix_to_ssbo(np.array(self.models_f, dtype="f4"), 0)
        self.raytracer.matrix_to_ssbo(np.array(self.inv_f, dtype="f4"), 1)
        self.raytracer.matrix_to_ssbo(np.array(self.mats_f, dtype="f4"), 2)
        self.raytracer.primitives_to_ssbo(self.primitives, 3)

class RayScene(Scene):
    def __init__(self, ctx, camera, width, height):
        super().__init__(ctx, camera)
        self.raytracer = RayTracer(camera, width, height)

    def start(self):
        self.raytracer.render_frame(self.objects)
        if "Sprite" in self.graphics:
            self.graphics["Sprite"].update_texture("u_texture", self.raytracer.get_texture())

    def render(self):
       super().render()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.raytracer = RayTracer(self.camera, width, height)
        self.start()