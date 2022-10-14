uniform vec3 u_color;
uniform sampler2D u_texture;

in vec3 v_position;
in vec2 v_texCoords;
in vec3 v_normal;
out vec4 fragColor;

void main()
{
    vec4 color = vec4(u_color, 1.0);
    color *= texture2D( u_texture, v_texCoords );
    
    fragColor = color;
}