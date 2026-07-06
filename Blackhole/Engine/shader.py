from panda3d.core import Shader


class ShaderManager:

    def __init__(self):
        self.cache = {}

    def load(self, vertex, fragment):

        key = (vertex, fragment)

        if key not in self.cache:

            shader = Shader.load(
                Shader.SL_GLSL,
                vertex=vertex,
                fragment=fragment
            )

            if shader is None:
                raise RuntimeError(
                    f"Failed to load shader:\n"
                    f"Vertex : {vertex}\n"
                    f"Fragment : {fragment}"
                )

            self.cache[key] = shader

        return self.cache[key]