from panda3d.core import *


class FrameBuffer:

    def __init__(self, base):

        self.base = base

        # ----------------------------------------------------
        # Textures
        # ----------------------------------------------------

        self.color_texture = Texture()
        self.depth_texture = Texture()

        self.color_texture.setMinfilter(
            SamplerState.FTLinear
        )

        self.color_texture.setMagfilter(
            SamplerState.FTLinear
        )

        self.depth_texture.setMinfilter(
            SamplerState.FTLinear
        )

        self.depth_texture.setMagfilter(
            SamplerState.FTLinear
        )

        # Floating-point colour texture (future HDR)
        self.color_texture.setComponentType(
            Texture.TFloat
        )

        self.color_texture.setFormat(
            Texture.FRgba16
        )

        # ----------------------------------------------------
        # Buffer Properties
        # ----------------------------------------------------

        props = FrameBufferProperties()

        props.setRgbColor(True)
        props.setAlphaBits(8)

        props.setDepthBits(32)

        props.setStencilBits(8)

        props.setFloatColor(True)

        # ----------------------------------------------------
        # Create Buffer
        # ----------------------------------------------------

        self.buffer = base.graphicsEngine.makeOutput(

            base.pipe,

            "SceneBuffer",

            -2,

            props,

            WindowProperties.size(
                base.win.getXSize(),
                base.win.getYSize()
            ),

            GraphicsPipe.BFRefuseWindow,

            base.win.getGsg(),

            base.win

        )

        if self.buffer is None:
            raise RuntimeError(
                "Failed to create framebuffer."
            )

        # ----------------------------------------------------
        # Attach textures
        # ----------------------------------------------------

        self.buffer.addRenderTexture(

            self.color_texture,

            GraphicsOutput.RTMBindOrCopy,

            GraphicsOutput.RTPColor

        )

        self.buffer.addRenderTexture(

            self.depth_texture,

            GraphicsOutput.RTMBindOrCopy,

            GraphicsOutput.RTPDepth

        )

        # ----------------------------------------------------
        # Camera
        # ----------------------------------------------------

        self.camera = base.makeCamera(
            self.buffer
        )

        self.camera.reparentTo(
            base.camera
        )

        # ----------------------------------------------------
        # Clear
        # ----------------------------------------------------

        self.buffer.setClearColor(
            (0.0, 0.0, 0.0, 1.0)
        )

        self.buffer.setClearColorActive(True)

        self.buffer.setClearDepthActive(True)

    # ----------------------------------------------------

    def getColorTexture(self):

        return self.color_texture

    # ----------------------------------------------------

    def getDepthTexture(self):

        return self.depth_texture

    # ----------------------------------------------------

    def getBuffer(self):

        return self.buffer

    # ----------------------------------------------------

    def getCamera(self):

        return self.camera

    # ----------------------------------------------------

    def resize(self):

        width = self.base.win.getXSize()

        height = self.base.win.getYSize()

        self.buffer.setSize(
            width,
            height
        )