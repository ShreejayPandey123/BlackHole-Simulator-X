from panda3d.core import *
from config import *
import math


class BlackHole:

    def __init__(self, base):

        self.base = base
        self.root = base.render.attachNewNode("BlackHole")

        # ==================================================
        # Event Horizon
        # ==================================================

        self.horizon = base.loader.loadModel("models/misc/sphere")
        self.horizon.reparentTo(self.root)

        self.horizon.setScale(BLACK_HOLE_RADIUS)
        self.horizon.setColor(0, 0, 0, 1)

        # Better rendering
        self.horizon.setShaderAuto()
        self.horizon.setBin("fixed", 10)
        self.horizon.setDepthWrite(False)
        self.horizon.setTwoSided(True)

        self.horizon.setLightOff()
        self.horizon.setMaterialOff()
        self.horizon.setTextureOff()

        # ==================================================
        # Photon Ring
        # ==================================================

        self.ring = self.create_ring(
            BLACK_HOLE_RADIUS * 1.08,
            BLACK_HOLE_RADIUS * 1.35,
            720,
            (1.0, 0.85, 0.25, 0.98),
            (1.0, 0.25, 0.0, 0.0)
        )

        self.ring.reparentTo(self.root)
        self.ring.setTransparency(TransparencyAttrib.MAlpha)
        self.ring.setTwoSided(True)
        self.ring.setDepthWrite(False)
        self.ring.setLightOff()
        self.ring.setP(90)

        # ==================================================
        # Outer Halo
        # ==================================================

        self.halo = self.create_ring(
            BLACK_HOLE_RADIUS * 1.40,
            BLACK_HOLE_RADIUS * 1.95,
            720,
            (1.0, 0.55, 0.05, 0.30),
            (1.0, 0.25, 0.0, 0.0)
        )

        self.halo.reparentTo(self.root)
        self.halo.setTransparency(TransparencyAttrib.MAlpha)
        self.halo.setTwoSided(True)
        self.halo.setDepthWrite(False)
        self.halo.setLightOff()
        self.halo.setP(90)

        self.rotation = 0.0

    # ======================================================

    def create_ring(
        self,
        inner_radius,
        outer_radius,
        segments,
        inner_color,
        outer_color
    ):

        fmt = GeomVertexFormat.getV3c4()

        vdata = GeomVertexData(
            "PhotonRing",
            fmt,
            Geom.UHStatic
        )

        vertex = GeomVertexWriter(vdata, "vertex")
        color = GeomVertexWriter(vdata, "color")

        triangles = GeomTriangles(Geom.UHStatic)

        for i in range(segments + 1):

            angle = (2.0 * math.pi * i) / segments

            c = math.cos(angle)
            s = math.sin(angle)

            # Small brightness ripple
            ripple = (
                0.85
                + 0.15 * math.sin(angle * 24.0)
            )

            # Inner Vertex
            vertex.addData3(
                inner_radius * c,
                0.0,
                inner_radius * s
            )

            color.addData4(
                inner_color[0],
                inner_color[1] * ripple,
                inner_color[2],
                inner_color[3]
            )

            # Outer Vertex
            vertex.addData3(
                outer_radius * c,
                0.0,
                outer_radius * s
            )

            color.addData4(
                outer_color[0],
                outer_color[1],
                outer_color[2],
                outer_color[3]
            )

        for i in range(segments):

            a = i * 2
            b = a + 1
            c = a + 2
            d = a + 3

            triangles.addVertices(a, b, c)
            triangles.addVertices(b, d, c)

        geom = Geom(vdata)
        geom.addPrimitive(triangles)

        node = GeomNode("PhotonRing")
        node.addGeom(geom)

        return NodePath(node)

    # ======================================================

    def update(self, dt):

        self.rotation += dt * 25.0

        # Rotate the photon ring
        self.ring.setH(self.rotation)

        # Rotate halo in opposite direction
        self.halo.setH(-self.rotation * 0.35)

        # ----------------------------
        # Gentle breathing animation
        # ----------------------------

        t = globalClock.getFrameTime()

        pulse = 1.0 + 0.015 * math.sin(t * 3.0)
        self.ring.setScale(pulse)

        haloPulse = 1.0 + 0.03 * math.sin(t * 1.8)
        self.halo.setScale(haloPulse)