#version 330

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;

in vec4 p3d_Vertex;
in vec4 p3d_Color;

out vec4 vColor;
out float vDistFromCenter;

// Gravitational well parameters
const float WELL_DEPTH    = 6.0;   // how deep the funnel goes
const float WELL_RADIUS   = 12.0;  // radius at which bending starts to flatten out
const float EVENT_HORIZON = 1.8;   // inner cutoff (clamp to prevent inversion)

void main()
{
    vec3 pos = p3d_Vertex.xyz;

    // Horizontal distance from the black hole centre
    float r = length(pos.xz);
    float rSafe = max(r, EVENT_HORIZON);

    // Schwarzschild-inspired funnel:  dip = -depth / (r + softening)
    float dip = -WELL_DEPTH / (rSafe / WELL_RADIUS + 1.0);

    // Smooth transition: no bending beyond a large radius
    float blend = smoothstep(40.0, 4.0, r);   // 1 near BH, 0 far away
    pos.y += dip * blend;

    vColor = p3d_Color;
    vDistFromCenter = r;

    gl_Position = p3d_ModelViewProjectionMatrix * vec4(pos, 1.0);
}
