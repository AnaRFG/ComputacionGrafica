import glm

class Hit:
    def __init__(self, position=(0,0,0), scale=(1,1,1), get_model_matrix=None, hittable=True):
        self.position = glm.vec3(*position)
        self.scale = glm.vec3(*scale)
        self.get_model_matrix = get_model_matrix
        self.hittable = hittable

    def check_hit(self, origin, direction):
        #"""Método abstracto: debe implementarse en las subclases."""
        raise NotImplementedError("Subclasses should implement this method.")


class HitBox(Hit):
    def __init__(self, position=(0,0,0), scale=(1,1,1), get_model_matrix=None, hittable=True):
        super().__init__(position, scale, get_model_matrix, hittable)

    def check_hit(self, origin, direction):
        #"""Chequea si un rayo intersecta con la caja delimitadora (AABB)."""
        if not self.hittable:
            return False

        origin = glm.vec3(origin)
        direction = glm.normalize(glm.vec3(direction))

        # Calculamos límites del cubo
        min_bounds = self.position - self.scale
        max_bounds = self.position + self.scale

        # Intersección de rayos con planos
        tmin = (min_bounds - origin) / direction
        tmax = (max_bounds - origin) / direction

        t1 = glm.min(tmin, tmax)
        t2 = glm.max(tmin, tmax)

        t_near = max(t1.x, t1.y, t1.z)
        t_far = min(t2.x, t2.y, t2.z)

        return t_near <= t_far and t_far >= 0
