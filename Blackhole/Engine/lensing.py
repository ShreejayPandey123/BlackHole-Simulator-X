from panda3d.core import *


class GravitationalLens:

    def __init__(self, base):

        self.base = base

        self.shader = Shader.load(
            Shader.SL_GLSL,
            vertex="shaders/lensing.vert",
            fragment="shaders/lensing.frag"
        )

        self.black_hole_uv = Vec2(0.5, 0.5)

        self.radius = 0.20
        self.strength = 0.12

    def update(self):

        point = Point2()

        if self.base.camLens.project(
            Point3(0, 0, 0),
            point
        ):

            self.black_hole_uv = Vec2(
                (point.x + 1.0) * 0.5,
                (point.y + 1.0) * 0.5
            )

    def apply(self, node):

        node.setShader(self.shader)

        node.setShaderInput(
            "blackHolePos",
            self.black_hole_uv
        )

        node.setShaderInput(
            "lensRadius",
            self.radius
        )

        node.setShaderInput(
            "strength",
            self.strength
        )