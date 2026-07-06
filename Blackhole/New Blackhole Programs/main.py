import os

if __name__ == "__main__":
    print("Current Directory:", os.getcwd())

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *

from config import *

from engine.objects.bh_renderer import BHRenderer


class BlackHoleSimulator(ShowBase):

    def __init__(self):

        super().__init__()

        self.disableMouse()

        # ---------------- Window ----------------

        props = WindowProperties()
        props.setTitle(TITLE)
        props.setSize(WIDTH, HEIGHT)
        props.setCursorHidden(False)       # cursor visible so mouse drag feels natural

        self.win.requestProperties(props)
        self.setBackgroundColor(0, 0, 0, 1)

        # ---------------- Ray-traced renderer ----------------
        #
        # BHRenderer handles everything:
        #   • fullscreen quad → blackhole.frag (Kerr ray-tracer)
        #   • orbit controls  → left-drag, scroll, arrow keys, = / -
        #
        self.bh_renderer = BHRenderer(self)

        # ---------------- Controls ----------------

        self.accept("escape", self.userExit)

        # ---------------- Update loop ----------------

        self.taskMgr.add(self.update, "Update")

    # ----------------------------------------------------------

    def update(self, task):

        dt = globalClock.getDt()
        self.bh_renderer.update(dt)

        return Task.cont


if __name__ == "__main__":
    app = BlackHoleSimulator()
    app.run()