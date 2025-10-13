import glm

class Hit:
    def __init__(self, position=(0,0,0), scale=(1,1,1)):
        self._position = glm.vec3(*position)
        self._scale = glm.vec3(*scale)
        
    @property
    def position(self):
        return self._position

    @property
    def scale(self):
        return self._scale

    def check_hit(self, origin, direction):
        raise NotImplementedError("Subclasses should implement this method.")


class HitBox(Hit):
    def __init__(self, position=(0,0,0), scale=(1,1,1), get_model_matrix=None):
        super().__init__(position, scale)
        self.get_model_matrix = get_model_matrix  # ✅ agregado para compatibilidad

    def check_hit(self, origin, direction):
        origin = glm.vec3(origin)
        direction = glm.normalize(glm.vec3(direction))

        # ✅ usar la matriz del modelo si está disponible
        if self.get_model_matrix:
            model = self.get_model_matrix()
            position = glm.vec3(model[3])  # tomar traslación del modelo
        else:
            position = self.position

        min_bounds = position - self.scale
        max_bounds = position + self.scale

        tmin = (min_bounds - origin) / direction
        tmax = (max_bounds - origin) / direction

        t1 = glm.min(tmin, tmax)
        t2 = glm.max(tmin, tmax)

        t_near = max(t1.x, t1.y, t1.z)
        t_far = min(t2.x, t2.y, t2.z)

        return t_near <= t_far and t_far >= 0
