import numpy as np
import glm

class VertexLayout:
    def __init__(self, attributes):
        self.attributes = attributes

    def get_attributes(self):
        return self.attributes


class Model:
    def __init__(self, vertices, indices, colors=None, normals=None, texcoords=None):
        self.vertices = vertices
        self.indices = indices
        self.colors = colors if colors is not None else np.zeros_like(vertices)
        self.normals = normals if normals is not None else np.zeros_like(vertices)
        self.texcoords = texcoords if texcoords is not None else np.zeros_like(vertices)

        # --- Layout de atributos de vértices ---
        self.vertex_layout = VertexLayout([
            ("in_pos", self.vertices),
            ("in_color", self.colors),
            ("in_normal", self.normals),
            ("in_uv", self.texcoords)
        ])

    # Métodos auxiliares
    def get_vertices(self):
        return self.vertices

    def get_indices(self):
        return self.indices

    def get_colors(self):
        return self.colors

    def get_normals(self):
        return self.normals

    def get_texcoords(self):
        return self.texcoords
