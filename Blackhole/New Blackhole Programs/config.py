"""
=========================================
Black Hole Simulation Config
=========================================
"""

# Screen dimensions
WIDTH = 1280
HEIGHT = 720
TITLE = "Black Hole"
BACKGROUND = (0, 0, 0, 1)  # Pure black background (RGBA)

# Camera
FOV = 70           # Field of view (degrees)
NEAR = 0.1         # Near clipping plane
FAR = 10000.0      # Far clipping plane

# Target FPS
FPS = 60

# Initial Simulation Parameters
DEFAULT_MASS = 1.0         # M☉
DEFAULT_SPIN = 0.5         # a*
DEFAULT_DIST = 30.0        # Rs
DEFAULT_LENSING_STR = 0.7  # Lensing strength
DEFAULT_TEMP = 9500.0      # Disk temperature (Kelvin)
DEFAULT_DENSITY = 4.0      # Disk optical density scale
DEFAULT_DISK_R = 50.0      # Accretion disk outer radius (Rs)
DEFAULT_THICKNESS = 0.20   # Disk thickness (H/R)
DEFAULT_PAN_SPEED = 0.005  # Camera auto-pan speed (rad/s)
DEFAULT_JET_POWER = 0.8    # Relativistic jet power

# Initial Module Toggles
DEFAULT_LENSING_ON = True
DEFAULT_JETS_ON = True
DEFAULT_DOPPLER_ON = True
DEFAULT_REDSHIFT_ON = True

# Bloom / Post-Processing
ENABLE_BLOOM = True
BLOOM_INTENSITY = 0.6
BLOOM_SIZE = "medium"

# Quality settings: low (100 steps), med (200 steps), high (350 steps)
DEFAULT_QUALITY = "med"

# Star Field / Galaxy
STAR_COUNT = 8000              # Total number of stars
STAR_RADIUS = 800.0            # Max star distribution radius
GALAXY_THICKNESS = 12.0        # Vertical spread (Gaussian σ)
MILKY_WAY_RATIO = 0.85         # Fraction of stars in spiral arms vs halo
STAR_MIN_BRIGHTNESS = 0.3      # Minimum star brightness
STAR_MAX_BRIGHTNESS = 1.0      # Maximum star brightness
STAR_ROTATION_SPEED = 0.002    # Galaxy rotation speed (degrees/frame)

# Black Hole Geometry
BLACK_HOLE_RADIUS = 1.5        # Event horizon radius (Schwarzschild units)

# Accretion Disk Geometry
DISK_INNER_RADIUS = 2.3        # Inner edge of accretion disk
DISK_OUTER_RADIUS = 7.0        # Outer edge of accretion disk

# Plasma Particles
PLASMA_PARTICLES = 2000        # Number of plasma particles in the disk
