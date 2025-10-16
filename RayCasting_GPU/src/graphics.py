import glm
import numpy as np


class Graphics:
    def __init__(self, ctx, model, material):
        self.__ctx = ctx
        self.__model = model
        self.__material = material   # cambie la definicion 
       
        self.__vbo = self.create_buffers()
        self.__ibo = self.__ctx.buffer(model.indices.tobytes())

        vao_content = []
        for attr_name, vbo in self.__vbo:
            vao_content.append((vbo, '3f', attr_name))  # formato de atributo (3 floats)

        self.__vao = self.__ctx.vertex_array(material.shader_program.prog, vao_content, self.__ibo)


        self.__textures = self.load_textures(material.textures_data)

    def create_buffers(self):
        buffers = []
        shader_attributes = self.__material.shader_program.attributes  # usar self.material

        for attr_name, attr_data in self.__model.vertex_layout.get_attributes():
            if attr_name in shader_attributes:
                vbo = self.__ctx.buffer(attr_data.astype('f4').tobytes())  # 🔧 corregido: __ctx
                buffers.append((attr_name, vbo)) 
        return buffers

    def load_textures(self, textures_data):
        textures = {}
        for texture in textures_data:  
            if texture.image_data:
                texture_ctx = self.__ctx.texture(texture.size, texture.channels_amount, texture.get_bytes())

            if texture.build_mipmaps:
                texture_ctx.build_mipmaps()

            texture_ctx.repeat_x = texture.repeat_x
            texture_ctx.repeat_y = texture.repeat_y

            textures[texture.name] = (texture, texture_ctx)

        return textures

    def bind_to_image(self, name = "u_texture", unit = 0, read = False, write = True):
        self.__textures[name][1].bind_to_image(unit, read, write)

    def render(self, uniforms):
        for name, value in uniforms.items():
            if name in self.__material.shader_program.prog:
                self.__material.set_uniform(name, value)

        for i, (name, (texture_obj, texture_ctx)) in enumerate(self.__textures.items()):
            texture_ctx.use(i)
            self.__material.shader_program.set_uniform(name, i)

        self.__vao.render()

    def update_texture(self, texture_name, new_data):
        if texture_name not in self.__textures:
            raise ValueError(f"No existe la textura {texture_name}")

        texture_obj, texture_ctx = self.__textures[texture_name]
        texture_obj.update_data(new_data)
        texture_ctx.write(new_data.tobytes())

        self.__vao.render()

class ComputeGraphics(Graphics):
    def __init__(self, ctx, model,material):
        self.__ctx = ctx
        self.__model = model
        self.__material = material
        self.textures = material.textures_data
        super().__init__(ctx, model, material)

    def create_primitive(self, primitives):
        amin, amax = self.__model.aabb
        primitives.append({"aabb_min": [amin.x, amin.y, amin.z], "aabb_max": [amax.x, amax.y, amax.z]})

    def create_transformation_matrix(self, transformations_matrix, index):
        m = self.__model.get_model_matrix()
        transformations_matrix[index, :] = np.array(m.to_list(), dtype="f4").reshape(16)

    def create_inverse_transformation_matrix(self, inverse_transformations_matrix, index):
        m = self.__model.get_model_matrix()
        inverse = glm.inverse(m)
        inverse_transformations_matrix[index, :] = np.array(inverse.to_list(), dtype="f4").reshape(16)

    def create_material_matrix(self, materials_matrix, index):
        reflectivity = self.__material.reflectivity
        r, g, b= self.__material.colorRGB

        r = r /255.0 if r > 1.0 else r
        g = g /255.0 if g > 1.0 else g
        b = b /255.0 if b > 1.0 else b

        materials_matrix[index, :] = np.array([r,g,b,reflectivity], dtype="f4")
        