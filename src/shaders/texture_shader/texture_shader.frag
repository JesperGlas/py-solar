uniform vec3 u_color;
uniform sampler2D u_texture;
in vec2 v_texCoords;
out vec4 fragColor;

void main()
{
    vec4 color = vec4(u_color, 1.0) * texture2D(u_texture, v_texCoords);
    if (color.a < 0.1)
        discard;

    fragColor = color;
}