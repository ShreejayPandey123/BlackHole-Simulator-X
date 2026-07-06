from direct.filter.CommonFilters import CommonFilters

from config import (
    ENABLE_BLOOM,
    BLOOM_INTENSITY,
    BLOOM_SIZE,
)


class PostProcessor:

    def __init__(self, base):

        self.base = base

        self.filters = CommonFilters(
            base.win,
            base.cam
        )

        self.enable()

    # --------------------------------------------------

    def enable(self):

        if ENABLE_BLOOM:
            self.filters.setBloom(
                blend=(0.35, 0.45, 0.80, 0.00),
                desat=-0.45,
                intensity=BLOOM_INTENSITY,
                size=BLOOM_SIZE
            )

        self.filters.setExposureAdjust(1.25)
        self.filters.setGammaAdjust(1.08)

    # --------------------------------------------------

    def update(self):
        pass