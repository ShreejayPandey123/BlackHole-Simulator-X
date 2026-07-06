#version 330

in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;

out vec2 texcoord;

void main()
{
    texcoord    = p3d_MultiTexCoord0;
    gl_Position = p3d_Vertex;
}