from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText

class PhysicsGuide:
    def __init__(self, base):
        self.base = base
        self.visible = True
        
        # Help banner at the bottom left (always visible)
        self.hint = OnscreenText(
            text="Press [H] to toggle Physics Guide",
            pos=(0.05, 0.05),
            scale=0.035,
            fg=(1, 1, 1, 0.8),
            shadow=(0, 0, 0, 0.8),
            align=TextNode.ALeft,
            parent=base.a2dBottomLeft
        )
        
        # ── Sidebar Container parented to TopRight ──────────────────
        cm = CardMaker("guide_bg")
        # Frame: left, right, bottom, top
        cm.setFrame(-0.85, -0.02, -1.95, -0.02)
        self.bg = base.a2dTopRight.attachNewNode(cm.generate())
        self.bg.setColor(0.01, 0.01, 0.02, 0.85)  # 85% opacity very dark blue-grey
        self.bg.setTransparency(TransparencyAttrib.MAlpha)
        
        # Create a border line (parented to self.bg so it inherits visibility)
        border_cm = CardMaker("guide_border")
        border_cm.setFrame(-0.86, -0.85, -1.95, -0.02)
        self.border = self.bg.attachNewNode(border_cm.generate())
        self.border.setColor(0.9, 0.4, 0.0, 0.9)  # Glowing orange line
        self.border.setTransparency(TransparencyAttrib.MAlpha)
        
        # Text entries inside the sidebar
        wrap = 24.0
        
        # Helper to add text parented to self.bg
        def add_text(text, pos, scale=0.032, fg=(1,1,1,1), shadow=None):
            return OnscreenText(
                text=text,
                pos=pos,
                scale=scale,
                fg=fg,
                shadow=shadow,
                align=TextNode.ALeft,
                parent=self.bg,
                wordwrap=wrap
            )

        # Title
        add_text(
            "KERR BLACK HOLE PHYSICS",
            pos=(-0.80, -0.10),
            scale=0.045,
            fg=(1, 0.45, 0.0, 1),
            shadow=(0, 0, 0, 0.5)
        )
        
        # Section 1: Event Horizon
        add_text("1. Event Horizon (Horizon)", pos=(-0.80, -0.20), scale=0.034, fg=(0.9, 0.9, 1.0, 1.0))
        add_text(
            "The boundary of no return, where gravity is so strong that escape speed exceeds light speed. Rotation (spin) shrinks this horizon size.",
            pos=(-0.80, -0.25),
            scale=0.028,
            fg=(0.7, 0.7, 0.75, 1.0)
        )

        # Section 2: Ergosphere
        add_text("2. Ergosphere & Frame-Dragging", pos=(-0.80, -0.47), scale=0.034, fg=(0.9, 0.9, 1.0, 1.0))
        add_text(
            "An oblate region outside the horizon where rotating spacetime drags all matter and light. Energy can be extracted here via Penrose process.",
            pos=(-0.80, -0.52),
            scale=0.028,
            fg=(0.7, 0.7, 0.75, 1.0)
        )

        # Section 3: Photon Sphere & Ring
        add_text("3. Photon Ring & Lensing", pos=(-0.80, -0.74), scale=0.034, fg=(0.9, 0.9, 1.0, 1.0))
        add_text(
            "A spherical shell of unstable photon orbits. Relativistic light bending wraps background stars and accretion disk light into a thin ring.",
            pos=(-0.80, -0.79),
            scale=0.028,
            fg=(0.7, 0.7, 0.75, 1.0)
        )

        # Section 4: Accretion Disk (ISCO)
        add_text("4. Accretion Disk & ISCO", pos=(-0.80, -1.01), scale=0.034, fg=(0.9, 0.9, 1.0, 1.0))
        add_text(
            "Friction heats orbiting plasma, emitting thermal radiation. The disk's inner boundary is the ISCO, where stable orbits cease.",
            pos=(-0.80, -1.06),
            scale=0.028,
            fg=(0.7, 0.7, 0.75, 1.0)
        )

        # Section 5: Doppler Beaming
        add_text("5. Relativistic Beaming", pos=(-0.80, -1.28), scale=0.034, fg=(0.9, 0.9, 1.0, 1.0))
        add_text(
            "Plasma orbiting towards us appears bluer and up to 4x brighter due to beaming; plasma moving away appears redder and much dimmer.",
            pos=(-0.80, -1.33),
            scale=0.028,
            fg=(0.7, 0.7, 0.75, 1.0)
        )

        # Section 6: Relativistic Jets
        add_text("6. Relativistic Jets", pos=(-0.80, -1.55), scale=0.034, fg=(0.9, 0.9, 1.0, 1.0))
        add_text(
            "Magnetic fields and rotational energy eject ionized matter along the poles at near-light speeds, forming huge glowing plumes.",
            pos=(-0.80, -1.60),
            scale=0.028,
            fg=(0.7, 0.7, 0.75, 1.0)
        )

        # Footer Hint
        add_text(
            "Press [H] to hide this panel\nScroll to zoom | Drag to rotate",
            pos=(-0.80, -1.85),
            scale=0.026,
            fg=(0.5, 0.5, 0.6, 1.0)
        )

    def toggle(self):
        self.visible = not self.visible
        if self.visible:
            self.bg.show()
        else:
            self.bg.hide()
