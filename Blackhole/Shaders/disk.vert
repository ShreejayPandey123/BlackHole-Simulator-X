#version 330

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;

in vec4 p3d_Vertex;
in vec4 p3d_Color;

out vec3 worldPos;
out vec2 diskUV;
out vec4 vertexColor;
out float radius;

void main()
{
    vec4 world = p3d_ModelMatrix * p3d_Vertex;

    worldPos = world.xyz;

    diskUV = p3d_Vertex.xz;

    radius = length(diskUV);

    vertexColor = p3d_Color;

    gl_Position =
        p3d_ModelViewProjectionMatrix *
        p3d_Vertex;
}