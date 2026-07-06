from panda3d.core import *
import math
import random


class DiskRing:

    def __init__(
        self,
        parent,
        shader,
        inner_radius,
        outer_radius,
        speed,
        color_inner,
        color_outer,
        segments=360
    ):

        self.speed = speed
        self.rotation = random.uniform(0.0, 360.0)

        fmt = GeomVertexFormat.getV3c4()

        vdata = GeomVertexData(
            "Ring",
            fmt,
            Geom.UHDynamic
        )

        vertex = GeomVertexWriter(vdata, "vertex")
        color = GeomVertexWriter(vdata, "color")

        triangles = GeomTriangles(Geom.UHStatic)

        # Different random pattern for every ring
        phase1 = random.uniform(0.0, math.tau)
        phase2 = random.uniform(0.0, math.tau)

        thickness = random.uniform(0.07, 0.11)

        for i in range(segments + 1):

            angle = (2.0 * math.pi * i) / segments

            c = math.cos(angle)
            s = math.sin(angle)

            # ----------------------------------------
            # Organic radial distortion
            # ----------------------------------------

            noise1 = (
                math.sin(angle * 8.0 + phase1)
                * 0.04
            )

            noise2 = (
                math.sin(angle * 12.0 + phase2)
                * 0.07
            )

            r1 = inner_radius + noise1
            r2 = outer_radius + noise2

            offset = random.uniform(-0.015, 0.015)

            r1 += offset
            r2 += offset

            # ----------------------------------------
            # Vertical thickness
            # ----------------------------------------

            height1 = (
                math.sin(angle * 14.0 + phase1)
                * thickness
                + random.uniform(-0.03, 0.03)
            )

            height2 = (
                math.sin(angle * 18.0 + phase2)
                * thickness
                + random.uniform(-0.03, 0.03)
            )

            # Slight bulge
            height1 *= 1.20
            height2 *= 0.85

            # ----------------------------------------
            # Alpha variation
            # ----------------------------------------

            alpha_inner = random.uniform(0.90, 1.00)
            alpha_outer = random.uniform(0.05, 0.15)

            # ----------------------------------------
            # Inner Vertex
            # ----------------------------------------

            vertex.addData3(
                r1 * c,
                height1,
                r1 * s
            )

            color.addData4(
                color_inner[0],
                color_inner[1],
                color_inner[2],
                alpha_inner
            )

            # ----------------------------------------
            # Outer Vertex
            # ----------------------------------------

            vertex.addData3(
                r2 * c,
                height2,
                r2 * s
            )

            color.addData4(
                color_outer[0],
                color_outer[1],
                color_outer[2],
                alpha_outer
            )

        # ----------------------------------------
        # Build triangles
        # ----------------------------------------

        for i in range(segments):

            a = i * 2
            b = a + 1
            c = a + 2
            d = a + 3

            triangles.addVertices(a, b, c)
            triangles.addVertices(b, d, c)

        geom = Geom(vdata)
        geom.addPrimitive(triangles)

        node = GeomNode("Ring")
        node.addGeom(geom)

        self.node = parent.attachNewNode(node)

        self.node.setShader(shader)

        self.node.setTransparency(
            TransparencyAttrib.MAlpha
        )

        self.node.setTwoSided(True)
        self.node.setDepthWrite(False)
        self.node.setLightOff()

        self.node.setHpr(0, 90, 0)

    def update(self, dt):

        self.rotation += self.speed * dt

        self.node.setH(self.rotation)