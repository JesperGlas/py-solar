uniform mat4 u_proj;
uniform mat4 u_view;
uniform mat4 u_model;
in vec3 a_position;
in vec2 a_texCoords;
uniform vec2 u_texRepeat;
uniform vec2 u_texOffset;
out vec2 v_texCoords;

void main()
{
    gl_Position = u_proj * u_view * u_model * vec4(a_position, 1.0);
    v_texCoords = a_texCoords * u_texRepeat + u_texOffset;
}