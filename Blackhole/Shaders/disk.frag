#version 330

in vec3 worldPos;
in vec2 diskUV;
in vec4 vertexColor;
in float radius;

uniform float time;

out vec4 fragColor;

//====================================================
// Noise
//====================================================

float hash(vec2 p)
{
    return fract(sin(dot(p, vec2(41.0,289.0))) * 43758.5453);
}

float noise(vec2 p)
{
    vec2 i=floor(p);
    vec2 f=fract(p);

    float a=hash(i);
    float b=hash(i+vec2(1,0));
    float c=hash(i+vec2(0,1));
    float d=hash(i+vec2(1,1));

    vec2 u=f*f*(3.0-2.0*f);

    return mix(a,b,u.x)
        +(c-a)*u.y*(1.0-u.x)
        +(d-b)*u.x*u.y;
}

float fbm(vec2 p)
{
    float v=0.0;
    float a=0.5;

    for(int i=0;i<6;i++)
    {
        v+=a*noise(p);
        p*=2.02;
        a*=0.5;
    }

    return v;
}

//====================================================

void main()
{
    float angle = atan(diskUV.y,diskUV.x);

    //------------------------------------------------
    // Doppler
    //------------------------------------------------

    vec2 orbitDir = normalize(vec2(-diskUV.y,diskUV.x));
    vec2 viewDir = normalize(vec2(0.0,-1.0));

    float doppler = dot(orbitDir,viewDir);
    float dopplerFactor = doppler*0.5+0.5;

    float boost = mix(
        0.80,
        1.25,
        dopplerFactor
    );

    //------------------------------------------------
    // Domain Warp
    //------------------------------------------------

    vec2 warp = diskUV*2.0;

    warp += vec2(
        fbm(warp+time*0.12),
        fbm(warp-time*0.10)
    );

    vec2 flow = warp;

    flow += vec2(
        fbm(flow*2.0+time*0.20),
        fbm(flow*2.0-time*0.15)
    )*0.45;

    //------------------------------------------------
    // Plasma
    //------------------------------------------------

    float plasma =
        fbm(flow*4.0);

    plasma +=
        fbm(flow*9.0)*0.35;

    plasma +=
        fbm(flow*18.0)*0.12;

    //------------------------------------------------
    // Spiral Arms
    //------------------------------------------------

    float spiral =
        sin(
            angle*24.0
            -radius*8.0
            -time*3.0
            +plasma*6.0
        );

    spiral =
        smoothstep(
            -0.2,
            1.0,
            spiral
        );

    //------------------------------------------------
    // Heat
    //------------------------------------------------

    float heat =
        exp(-radius*0.45);

    heat = pow(
        heat,
        0.72
    );

    //------------------------------------------------
    // Colours
    //------------------------------------------------

    vec3 cold =
        vec3(
            0.50,
            0.04,
            0.01
        );

    vec3 warm =
        vec3(
            1.00,
            0.42,
            0.02
        );

    vec3 hot =
        vec3(
            1.00,
            0.92,
            0.72
        );

    vec3 colour =
        mix(
            cold,
            warm,
            spiral
        );

    colour =
        mix(
            colour,
            hot,
            heat*plasma
        );

    //------------------------------------------------
    // Density
    //------------------------------------------------

    float density =
        smoothstep(
            0.25,
            1.0,
            plasma
        );

    colour *=
        mix(
            0.8,
            1.4,
            density
        );

    //------------------------------------------------
    // Orbiting Hotspots
    //------------------------------------------------

    float hotspot =
        fbm(
            flow*14.0+
            vec2(
                time*1.5,
                -time
            )
        );

    hotspot =
        smoothstep(
            0.83,
            0.98,
            hotspot
        );

    colour +=
        hotspot
        *heat
        *vec3(
            1.35,
            1.1,
            0.8
        );

    //------------------------------------------------
    // Vertical Thickness
    //------------------------------------------------

    float vertical =
        exp(
            -abs(worldPos.y)*6.0
        );

    colour *= vertical;

    //------------------------------------------------
    // Glow
    //------------------------------------------------

    float glow =
    0.55
    + heat * 2.0
    + plasma * 0.25;

colour *= glow;

    //------------------------------------------------
    // Doppler
    //------------------------------------------------

    colour *= boost;

    vec3 blueShift =
        vec3(
            0.92,
            0.98,
            1.16
        );

    vec3 redShift =
        vec3(
            1.15,
            0.90,
            0.72
        );

    colour =
        mix(
            colour*redShift,
            colour*blueShift,
            dopplerFactor
        );

    //------------------------------------------------
    // Rim Glow
    //------------------------------------------------

    float rim =
        pow(
            1.0-
            abs(worldPos.y),
            4.0
        );

    colour +=
        vec3(
            1.0,
            0.72,
            0.30
        )
        *rim
        *0.7;

    //------------------------------------------------
    // Alpha
    //------------------------------------------------

    float alpha =
        smoothstep(
            6.4,
            5.3,
            radius
        );
    //------------------------------------------------
// ACES Filmic Tone Mapping
//------------------------------------------------

colour =
    (colour * (2.51 * colour + 0.03))
    /
    (colour * (2.43 * colour + 0.59) + 0.14);

colour = clamp(
    colour,
    0.0,
    1.0
);

// Gamma

colour = pow(
    colour,
    vec3(1.0 / 2.2)
);

    fragColor =
        vec4(
            colour,
            alpha
        );
}