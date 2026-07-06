#version 330

uniform sampler2D sceneTex;

uniform vec2  blackHolePos;   // screen-space UV [0,1]
uniform float lensRadius;     // outer radius of lens effect  (in UV units)
uniform float strength;       // peak warp strength

in vec2 texcoord;
out vec4 fragColor;

void main()
{
    vec2 uv    = texcoord;
    vec2 delta = uv - blackHolePos;
    float r    = length(delta);
    vec2  dir  = normalize(delta + vec2(1e-9));

    // -------------------------------------------------------
    // Gravitational lensing — inverse-square-style deflection
    //   deflection  ∝  strength / r^2   (softened near centre)
    // -------------------------------------------------------
    float softR   = max(r, 0.005);                  // avoid singularity
    float deflect = strength / (softR * softR + 0.01);

    // Clamp so very close pixels don't go wild
    deflect = min(deflect, 0.40);

    // Only bend within the lens radius; smooth blend at the edge
    float mask = smoothstep(lensRadius, lensRadius * 0.30, r);

    vec2 warpedUV = uv - dir * deflect * mask;

    // -------------------------------------------------------
    // Chromatic aberration — RGB channels bent by slightly
    // different amounts (like real gravitational optics)
    // -------------------------------------------------------
    float chromatic = deflect * mask * 0.18;
    vec2  uvR = uv - dir * (deflect + chromatic) * mask;
    vec2  uvG = warpedUV;
    vec2  uvB = uv - dir * (deflect - chromatic) * mask;

    float colR = texture(sceneTex, uvR).r;
    float colG = texture(sceneTex, uvG).g;
    float colB = texture(sceneTex, uvB).b;

    // -------------------------------------------------------
    // Einstein ring glow — a bright rim at the photon sphere
    // -------------------------------------------------------
    float ringRadius  = lensRadius * 0.18;
    float ringWidth   = lensRadius * 0.06;
    float ringMask    = exp(-pow((r - ringRadius) / ringWidth, 2.0));
    vec3  ringGlow    = vec3(1.0, 0.92, 0.75) * ringMask * 0.55;

    vec3 col = vec3(colR, colG, colB) + ringGlow;

    fragColor = vec4(col, 1.0);
}