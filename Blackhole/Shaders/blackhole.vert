#version 330

in vec4 p3d_Vertex;
out vec2 texcoord;

void main()
{
    // render2d card: vertex.x = [-1,1] left-right, vertex.z = [-1,1] bottom-top
    // Map directly to clip space (bypass MVP – we want a true fullscreen quad)
    texcoord    = vec2(p3d_Vertex.x * 0.5 + 0.5,
                       p3d_Vertex.z * 0.5 + 0.5);
    gl_Position = vec4(p3d_Vertex.x, p3d_Vertex.z, 0.0, 1.0);
}