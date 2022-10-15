uniform mat4 u_proj;
uniform mat4 u_view;
uniform mat4 u_model;
uniform sampler2D u_bumpTexture;

in vec3 a_position;
in vec2 a_texCoords;
in vec3 a_vNormal;

out vec3 v_position;
out vec2 v_texCoords;
out vec3 v_normal;

void main()
{
    gl_Position = u_proj * u_view * u_model * vec4(a_position, 1);
    v_position = vec3(u_view * vec4(a_position, 1));
    v_texCoords = a_texCoords;
    v_normal = normalize(mat3(u_model) * a_vNormal);
}