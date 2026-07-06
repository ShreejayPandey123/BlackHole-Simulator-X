#version 330

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform float time;

in vec4 p3d_Vertex;
in vec4 p3d_Color;

out vec4 vertexColor;

void main()
{
    vertexColor = p3d_Color;
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}