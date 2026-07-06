from panda3d.core import *


class CameraController:

    def __init__(self, base):

        self.base = base
        self.camera = base.camera

        # Camera settings
        self.move_speed = 20.0
        self.fast_speed = 60.0
        self.mouse_sensitivity = 0.15

        # Start with the current camera rotation
        self.heading = self.camera.getH()
        self.pitch = self.camera.getP()

        # Key states
        self.keys = {
            "w": False,
            "a": False,
            "s": False,
            "d": False,
            "q": False,
            "e": False,
            "shift": False
        }

        for key in self.keys:
            base.accept(key, self.set_key, [key, True])
            base.accept(f"{key}-up", self.set_key, [key, False])

        # Hide mouse cursor
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

        self.center_mouse()

    def center_mouse(self):

        self.center_x = self.base.win.getXSize() // 2
        self.center_y = self.base.win.getYSize() // 2

        self.base.win.movePointer(
            0,
            self.center_x,
            self.center_y
        )

    def set_key(self, key, value):

        self.keys[key] = value

    def update(self, dt):

        # --------------------
        # Mouse Look
        # --------------------

        if self.base.mouseWatcherNode.hasMouse():

            md = self.base.win.getPointer(0)

            dx = md.getX() - self.center_x
            dy = md.getY() - self.center_y

            self.heading -= dx * self.mouse_sensitivity
            self.pitch -= dy * self.mouse_sensitivity

            self.pitch = max(-89, min(89, self.pitch))

            self.camera.setHpr(
                self.heading,
                self.pitch,
                0
            )

            self.base.win.movePointer(
                0,
                self.center_x,
                self.center_y
            )

        # --------------------
        # Keyboard Movement
        # --------------------

        speed = self.fast_speed if self.keys["shift"] else self.move_speed

        if self.keys["w"]:
            self.camera.setY(self.camera, speed * dt)

        if self.keys["s"]:
            self.camera.setY(self.camera, -speed * dt)

        if self.keys["a"]:
            self.camera.setX(self.camera, -speed * dt)

        if self.keys["d"]:
            self.camera.setX(self.camera, speed * dt)

        if self.keys["q"]:
            self.camera.setZ(self.camera, -speed * dt)

        if self.keys["e"]:
            self.camera.setZ(self.camera, speed * dt)