from panda3d.core import *
import random
import math

from config import *


class StarField:

    def __init__(self, base):

        self.base = base
        self.root = base.render.attachNewNode("Galaxy")

        self.rotation = 0.0

        self.star_brightness = []
        self.star_positions = []

        self.create()

    # ---------------------------------------------------------

    def create(self):

        fmt = GeomVertexFormat.getV3c4()

        self.vdata = GeomVertexData(
            "Galaxy",
            fmt,
            Geom.UHDynamic
        )

        vertex = GeomVertexWriter(self.vdata,"vertex")
        color = GeomVertexWriter(self.vdata,"color")

        self.star_brightness.clear()

        # ---------------------------------------------------------
        # Spiral Galaxy Parameters
        # ---------------------------------------------------------

        ARM_COUNT = 4

        ARM_TIGHTNESS = 2.8

        CORE_RADIUS = 140

        CLUSTER_CHANCE = 0.03

        DUST_WIDTH = 0.18

        created = 0

        while created < STAR_COUNT:

            # ---------------------------------------
            # Galaxy Distribution
            # ---------------------------------------

            if random.random() < MILKY_WAY_RATIO:

                radius = random.uniform(20.0, STAR_RADIUS)

                arm = random.randint(0, ARM_COUNT - 1)
                arm_offset = arm * (2.0 * math.pi / ARM_COUNT)

                spiral = (radius / STAR_RADIUS) * ARM_TIGHTNESS

                theta = (
                    arm_offset
                    + spiral
                    + random.gauss(0.0, 0.25)
                )

                dust = abs(math.sin(theta * 2.0))

                if dust < DUST_WIDTH:
                    radius *= 1.15

                x = radius * math.cos(theta)
                z = radius * math.sin(theta)

                y = random.gauss(0.0, GALAXY_THICKNESS)

                if radius < CORE_RADIUS:
                    y *= 0.35
                    x *= random.uniform(0.85, 1.05)
                    z *= random.uniform(0.85, 1.05)

                if random.random() < CLUSTER_CHANCE:
                    cluster_radius = random.uniform(4.0, 12.0)
                    x += random.gauss(0.0, cluster_radius)
                    y += random.gauss(0.0, cluster_radius * 0.3)
                    z += random.gauss(0.0, cluster_radius)

            else:

                r = random.uniform(STAR_RADIUS * 0.7, STAR_RADIUS)
                theta = random.uniform(0.0, math.tau)
                phi = math.acos(random.uniform(-1.0, 1.0))

                x = r * math.sin(phi) * math.cos(theta)
                y = r * math.cos(phi)
                z = r * math.sin(phi) * math.sin(theta)

            vertex.addData3(x, y, z)
            self.star_positions.append(LVector3f(x, y, z))

            created += 1
            # ---------------------------------------
            # Stellar Colours
            # ---------------------------------------

            t = random.random()

            if t < 0.50:

                # White
                r, g, b = (
                    1.0,
                    1.0,
                    1.0
                )

            elif t < 0.70:

                # Blue-white
                r, g, b = (
                    0.78,
                    0.86,
                    1.0
                )

            elif t < 0.88:

                # Yellow
                r, g, b = (
                    1.0,
                    0.95,
                    0.82
                )

            elif t < 0.97:

                # Orange
                r, g, b = (
                    1.0,
                    0.70,
                    0.45
                )

            else:

                # Rare blue giant
                r, g, b = (
                    0.55,
                    0.72,
                    1.0
                )

            # ---------------------------------------
            # Brightness
            # ---------------------------------------

            brightness = random.uniform(
                STAR_MIN_BRIGHTNESS,
                STAR_MAX_BRIGHTNESS
            )

            # Very bright giants
            if random.random() < 0.01:
                brightness *= 2.5

            self.star_brightness.append(
                (
                    r,
                    g,
                    b,
                    brightness
                )
            )

            color.addData4(
                min(r * brightness, 1.0),
                min(g * brightness, 1.0),
                min(b * brightness, 1.0),
                1.0
            )

        geom = Geom(self.vdata)

        prim = GeomPoints(
            Geom.UHStatic
        )

        for i in range(created):
            prim.addVertex(i)

        prim.closePrimitive()

        geom.addPrimitive(prim)

        node = GeomNode("Galaxy")
        node.addGeom(geom)

        self.node = self.root.attachNewNode(node)
        shader = Shader.load(Shader.SL_GLSL,"shaders/stars.vert","shaders/stars.frag")
        self.node.setShader(shader)
        self.node.setShaderInput("bhNDC", Vec2(0.0, 0.0))  # updated every frame

        self.node.setRenderModeThickness(3)

        self.node.setLightOff()

        self.node.setDepthWrite(False)

    # -----------------------------------------------------

    def update(self):
        self.rotation += STAR_ROTATION_SPEED
        self.root.setH(self.rotation)
        self.node.setShaderInput("time", globalClock.getFrameTime())

        # Project black hole world origin → NDC [-1, 1] for lensing shader
        pt = Point2()
        if self.base.camLens.project(Point3(0, 0, 0), pt):
            self.node.setShaderInput("bhNDC", Vec2(pt.x, pt.y))
        else:
            # BH behind camera — park it far off-screen so no lensing
            self.node.setShaderInput("bhNDC", Vec2(99.0, 99.0))


    # Future gravitational lensing
    #
    # This will be handled by the star shader.