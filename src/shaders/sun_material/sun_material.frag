uniform vec3 u_color;
uniform sampler2D u_texture;

in vec3 v_position;
in vec2 v_texCoords;
in vec3 v_normal;
out vec4 fragColor;

uniform float u_time;
uniform sampler2D u_noise;

void main()
{
    vec4 color = vec4(u_color, 1.0);
    
    float noise_magnitude = 0.01;
    float noise_offset = clamp(sin(u_time*noise_magnitude) * texture2D(u_noise, v_texCoords).r, -1, 1);
    
    color *= texture2D( u_texture, v_texCoords + noise_offset ) + vec4(0.1);
    
    fragColor = color;
}