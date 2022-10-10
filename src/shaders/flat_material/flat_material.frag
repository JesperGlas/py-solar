uniform vec3 u_color;
uniform bool u_useTexture;
uniform sampler2D u_texture;
in vec2 v_texCoords;
in vec3 v_light;
out vec4 fragColor;

void main()
{
    vec4 color = vec4(u_color, 1.0);
    if (u_useTexture)
        color *= texture2D(u_texture, v_texCoords);
    color *= vec4(v_light, 1);
    fragColor = color;
}