import pyglet
import moderngl

class Window(pyglet.window.Window):
    def __init__(self, width, heigth, title):
        super().__init__(width, heigth, title, resizable=True)
        self.ctx = moderngl.create_context()
        self.scene = None
        self._started = False  # bandera para evitar bloqueo

    def set_scene(self, scene):
        self.scene = scene
        # No llamamos scene.start() aquí (bloquea la ventana)

    def on_draw(self):  # por cada frame
        self.clear()
        self.ctx.clear(0.1, 0.1, 0.1, 1.0, depth=1.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        if self.scene:
            # llamamos start solo una vez, luego renderizamos normalmente
            if not self._started:
                print("Iniciando escena...")
                self.scene.start()
                self._started = True

            self.scene.render()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.scene is None:
            return

        # Convertir posición del mouse a u,v [0,1]
        u = x / self.width
        v = y / self.height
        self.scene.on_mouse_click(u, v)

    def on_resize(self, width, height):
        if self.scene:
            self.scene.on_resize(width, height)

    def run(self):
        pyglet.app.run()
