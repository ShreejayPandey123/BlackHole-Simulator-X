#version 330

in vec4 vColor;
in float vDistFromCenter;

out vec4 fragColor;

void main()
{
    // Fade grid lines out as they approach the centre (swallowed by BH)
    float innerFade = smoothstep(2.0, 5.0, vDistFromCenter);

    // Fade grid lines at the horizon edge (far boundary)
    float outerFade = smoothstep(42.0, 30.0, vDistFromCenter);

    float alpha = vColor.a * innerFade * outerFade;

    fragColor = vec4(vColor.rgb, alpha);
}
