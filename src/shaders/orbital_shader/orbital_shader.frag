struct Light
{
    vec3 ambient;
    vec3 color;
    vec3 direction;
    vec3 position;
};

vec3 calculateLight(Light light, vec3 view_position, vec3 point_position, vec3 point_normal)
{
    vec3 color = light.color;
    vec3 L = normalize(light.direction);
    vec3 N = normalize(point_normal);
    vec3 V = normalize(view_position - point_position);
    vec3 R = reflect(L, N);

    // ambient
    vec3 ambient = light.ambient;
    
    // diffuse
    float diffuse = max( dot(N, -L), 0.0 );

    // specular (TODO)

    return color * (ambient + diffuse);
}

float softShadow(vec3 light_pos, float light_radius, vec3 occluder_pos, float occluder_radius, vec3 fragment)
{
    vec3 v0 = light_pos - fragment;
    vec3 v1 = occluder_pos - fragment;

    float r0 = length(v0);
    float r1 = length(v1);

    float a0 = light_radius/r0;
    float a1 = occluder_radius/r1;

    float a = length( cross(v0, v1)/(r0*r1) );
    a = smoothstep(a0 - a1, a0 + a1, a);
    return 1 - (1-a) * pow(a1/a0, 2);
}

uniform vec3 u_color;
uniform bool u_useTexture;
uniform sampler2D u_texture;
uniform bool u_useBumpTexture;
uniform sampler2D u_bumpTexture;
uniform float u_bumpStrength;
uniform Light u_light;
uniform vec3 u_viewPosition;

in vec3 v_position;
in vec2 v_texCoords;
in vec3 v_normal;

out vec4 fragColor;

void main()
{
    vec4 color = vec4(u_color, 1.0);
    if (u_useTexture) 
    {
        color *= texture2D( u_texture, v_texCoords );
    }
    vec3 bump_normal = v_normal;
    if (u_useBumpTexture) 
    {
        bump_normal += u_bumpStrength * vec3(texture2D(u_bumpTexture, v_texCoords));
    }
    // Calculate total effect of lights on color
    vec3 light = calculateLight(
        u_light,
        u_viewPosition,
        v_position,
        bump_normal
    );

    color *= vec4(light, 1); 
    
    fragColor = color;
}