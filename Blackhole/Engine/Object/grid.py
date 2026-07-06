from panda3d.core import *
import math


class GridFloor:
    """
    A perspective grid that bends downward toward the black hole,
    simulating curved spacetime (Schwarzschild funnel).

    Each grid line is tessellated into many short segments so the
    GLSL vertex shader has enough vertices to produce a smooth curve.
    """

    def __init__(self, base):

        self.base  = base
        self.root  = base.render.attachNewNode("GridFloor")
        self._build()

    # ----------------------------------------------------------

    def _build(self):

        # -------------------------------------------------------
        # Grid layout
        # -------------------------------------------------------
        HALF_W     = 38         # half-width  X
        HALF_D     = 38         # half-depth  Z
        GRID_LINES = 30         # number of lines per axis
        SEG        = 80         # segments per line  ← key for smooth bending

        fmt   = GeomVertexFormat.getV3c4()
        vdata = GeomVertexData("Grid", fmt, Geom.UHStatic)

        vw    = GeomVertexWriter(vdata, "vertex")
        cw    = GeomVertexWriter(vdata, "color")
        lines = GeomLines(Geom.UHStatic)

        idx = 0

        def add_seg(x0, z0, x1, z1):
            """Add one line segment (two vertices + one line primitive)."""
            nonlocal idx

            # brightness slightly warmer near origin
            for (x, z) in [(x0, z0), (x1, z1)]:
                d = math.sqrt(x * x + z * z)
                glow = max(0.0, 1.0 - d / 18.0) * 0.30
                b    = 0.70 + glow
                vw.addData3(x, 0.0, z)
                cw.addData4(b, b, b, 0.85)

            lines.addVertices(idx, idx + 1)
            idx += 2

        # ---- Lines running along X  (constant Z) ----
        for i in range(GRID_LINES + 1):
            z = -HALF_D + (i / GRID_LINES) * HALF_D * 2
            for s in range(SEG):
                x0 = -HALF_W + (s      / SEG) * HALF_W * 2
                x1 = -HALF_W + ((s + 1) / SEG) * HALF_W * 2
                add_seg(x0, z, x1, z)

        # ---- Lines running along Z  (constant X) ----
        for i in range(GRID_LINES + 1):
            x = -HALF_W + (i / GRID_LINES) * HALF_W * 2
            for s in range(SEG):
                z0 = -HALF_D + (s      / SEG) * HALF_D * 2
                z1 = -HALF_D + ((s + 1) / SEG) * HALF_D * 2
                add_seg(x, z0, x, z1)

        geom = Geom(vdata)
        geom.addPrimitive(lines)

        node = GeomNode("Grid")
        node.addGeom(geom)

        self.node = self.root.attachNewNode(node)

        # ---- Gravitational-well shader ----
        shader = Shader.load(
            Shader.SL_GLSL,
            "shaders/grid.vert",
            "shaders/grid.frag"
        )
        self.node.setShader(shader)

        self.node.setTransparency(TransparencyAttrib.MAlpha)
        self.node.setLightOff()
        self.node.setDepthWrite(False)
        self.node.setDepthTest(True)
        self.node.setBin("transparent", 5)
        self.node.setTwoSided(True)
        self.node.setPos(0, 0, 0)

    # ----------------------------------------------------------

    def update(self):
        pass
