from panda3d.core import *
from config import *

import random
import math


class PlasmaParticles:

    def __init__(self, base):

        self.base = base

        self.root = base.render.attachNewNode("Plasma")

        self.count = PLASMA_PARTICLES

        self.particles = []

        self.build()

    # -------------------------------------------------

    def build(self):

        fmt = GeomVertexFormat.getV3c4()

        self.vdata = GeomVertexData(
            "Plasma",
            fmt,
            Geom.UHDynamic
        )

        self.vdata.setNumRows(self.count)

        vertex = GeomVertexWriter(
            self.vdata,
            "vertex"
        )

        color = GeomVertexWriter(
            self.vdata,
            "color"
        )

        for _ in range(self.count):

            radius = random.uniform(
                DISK_INNER_RADIUS,
                DISK_OUTER_RADIUS
            )

            angle = random.uniform(
                0,
                math.tau
            )

            speed = random.uniform(
                0.8,
                3.5
            )

            height = random.uniform(
                -0.25,
                0.25
            )

            brightness = random.uniform(
                0.4,
                1.4
            )

            phase = random.uniform(
                0,
                math.tau
            )

            drift = random.uniform(
                0.010,
                0.040
            )

            self.particles.append(
                {
                    "radius": radius,
                    "angle": angle,
                    "speed": speed,
                    "height": height,
                    "brightness": brightness,
                    "phase": phase,
                    "drift": drift
                }
            )

            x = radius * math.cos(angle)
            z = radius * math.sin(angle)

            vertex.addData3(
                x,
                height,
                z
            )

            # --------------------------------------
            # Colour
            # --------------------------------------

            t = random.random()

            if t < 0.45:

                colour = (
                    1.0,
                    0.95,
                    0.85
                )

            elif t < 0.80:

                colour = (
                    1.0,
                    0.65,
                    0.12
                )

            else:

                colour = (
                    1.0,
                    0.30,
                    0.02
                )

            color.addData4(
                colour[0],
                colour[1],
                colour[2],
                brightness
            )

        geom = Geom(self.vdata)

        prim = GeomPoints(
            Geom.UHDynamic
        )

        for i in range(self.count):
            prim.addVertex(i)

        prim.closePrimitive()

        geom.addPrimitive(prim)

        node = GeomNode("Plasma")
        node.addGeom(geom)

        self.node = self.root.attachNewNode(node)

        self.node.setRenderModeThickness(4)

        self.node.setTransparency(
            TransparencyAttrib.MAlpha
        )

        self.node.setDepthWrite(False)

        self.node.setLightOff()

    # -------------------------------------------------

    def update(self, dt):

        vertex = GeomVertexRewriter(
            self.vdata,
            "vertex"
        )

        colour = GeomVertexRewriter(
            self.vdata,
            "color"
        )

        t = globalClock.getFrameTime()

        for p in self.particles:

            # Keplerian rotation
            p["angle"] += (
                p["speed"] /
                math.sqrt(p["radius"])
            ) * dt

            # Spiral inward
            p["radius"] -= (
                p["drift"] * dt
            )

            if p["radius"] < DISK_INNER_RADIUS:

                p["radius"] = DISK_OUTER_RADIUS

                p["angle"] = random.uniform(
                    0,
                    math.tau
                )

            # Vertical oscillation

            h = (
                p["height"]
                +
                math.sin(
                    t * 4.0
                    + p["phase"]
                ) * 0.04
            )

            # Turbulence

            r = (
                p["radius"]
                +
                math.sin(
                    p["angle"] * 6.0
                    + t * 2.5
                ) * 0.03
            )

            x = r * math.cos(
                p["angle"]
            )

            z = r * math.sin(
                p["angle"]
            )

            vertex.setData3(
                x,
                h,
                z
            )

            # Flickering brightness

            b = (
                p["brightness"]
                *
                (
                    0.8
                    +
                    0.2
                    *
                    math.sin(
                        t * 6.0
                        + p["phase"]
                    )
                )
            )

            colour.setData4(
                1.0,
                min(1.0, 0.55 + b * 0.45),
                0.08,
                b
            )