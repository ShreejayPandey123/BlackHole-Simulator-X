from panda3d.core import *
from engine.objects.ring import DiskRing


class AccretionDisk:

    def __init__(self, base):

        self.base = base
        self.root = base.render.attachNewNode("AccretionDisk")

        # Load the disk shader through the ShaderManager
        self.shader = self.base.shader_manager.load(
            "shaders/disk.vert",
            "shaders/disk.frag"
        )

        self.rings = []

        self.create()

    def create(self):

        ring_count = 40

        inner_radius = 2.3
        outer_radius = 7.0       # slightly wider for reference look

        width = (outer_radius - inner_radius) / ring_count

        for i in range(ring_count):

            r1 = inner_radius + i * width
            r2 = r1 + width * 1.08

            # Keplerian rotation
            speed = 45.0 / (r1 ** 0.5)

            # heat = 1 at inner, 0 at outer
            heat = 1.0 - (i / ring_count)

            # -------------------------------------------------------
            # Reference image palette:
            #   inner rings  → bright white / pale yellow
            #   mid rings    → orange / amber
            #   outer rings  → deep red
            # -------------------------------------------------------
            if heat > 0.75:
                # Very hot inner zone — white / yellow-white
                inner_color = (1.0, 1.0, 0.85, 0.98)
                outer_color = (1.0, 0.85, 0.30, 0.20)
            elif heat > 0.45:
                # Mid zone — orange
                inner_color = (1.0, 0.55 + heat * 0.45, 0.05, 0.95)
                outer_color = (0.90, 0.18, 0.01, 0.12)
            else:
                # Outer zone — deep red
                inner_color = (0.85, 0.10, 0.01, 0.92)
                outer_color = (0.50, 0.02, 0.00, 0.05)

            ring = DiskRing(
                parent=self.root,
                shader=self.shader,
                inner_radius=r1,
                outer_radius=r2,
                speed=speed,
                color_inner=inner_color,
                color_outer=outer_color
            )

            self.rings.append(ring)

    def update(self, dt):

        shader_time = globalClock.getFrameTime()

        camera_position = self.base.camera.getPos(
            self.base.render
        )

        for ring in self.rings:

            ring.node.setShaderInput(
                "time",
                shader_time
            )

            ring.node.setShaderInput(
                "cameraPos",
                camera_position
            )

            ring.update(dt)