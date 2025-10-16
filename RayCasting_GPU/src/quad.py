from model import Model
from hit import HitBox
import numpy as np
import glm


class Quad(Model):
    def __init__(self, position=(0,0,0), rotation=(0,0,0), scale=(1,1,1), name="quad",animated = True, hittable = True):
        self.name = name
        self.animated = animated
        self.position = glm.vec3(*position)
        self.rotation = glm.vec3(*rotation)
        self.scale = glm.vec3(*scale)
        self.__colision = HitBox(get_model_matrix = lambda: self.get_model_matrix())
   
        vertices = np.array([
            -1, -1, 0,
            1, -1, 0,
            1,  1, 0,
            -1,  1, 0,
        ], dtype="f4")


        colors = np.array([
            0,1,1,
            0,0,1,
            1,0,1,
            1,1,0
        ], dtype='f4')


        texcoords = np.array([
            0, 0,
            1, 0,
            1, 1,
            0, 1,
        ], dtype="f4")


        normals = np.array([
            0, 0, 1,
            0, 0, 1,
            0, 0, 1,
            0, 0, 1,
        ], dtype="f4")


        indices = np.array([
            0, 1, 2,
            2, 3, 0
        ], dtype="i4")


        super().__init__(vertices, indices, colors= colors, texcoords=texcoords, normals=normals)

    @property
    def aabb(self):
        # Calcula el AABB en espacio mundial
        # Basado en los 4 vértices del quad (-1 a 1)
        vertices = np.array([
            [-1, -1, 0],
            [1, -1, 0],
            [1, 1, 0],
            [-1, 1, 0]
        ], dtype="f4")

        # Transformar cada vértice por la matriz modelo
        model = self.get_model_matrix()
        transformed = [model * glm.vec4(*v, 1.0) for v in vertices]

        xs = [p.x for p in transformed]
        ys = [p.y for p in transformed]
        zs = [p.z for p in transformed]

        return glm.vec3(min(xs), min(ys), min(zs)), glm.vec3(max(xs), max(ys), max(zs))

    
    def check_hit(self, origin, direction):
        return self.__colision.check_hit(origin, direction)
   
    def get_model_matrix(self):
        model = glm.mat4(1)
        model = glm.translate(model, self.position)
        model = glm.rotate(model, glm.radians(self.rotation.x % 360), glm.vec3(1, 0, 0))
        model = glm.rotate(model, glm.radians(self.rotation.y % 360), glm.vec3(0, 1, 0))
        model = glm.rotate(model, glm.radians(self.rotation.z % 360), glm.vec3(0, 0, 1))
        model = glm.scale(model, self.scale)
        return model


