struct Light
{
    vec3 ambient;
    vec3 color;
    vec3 position;
    float radius;
};

struct Occluder
{
    vec3 position;
    float radius;
};

uniform Occluder u_occluder0;
uniform Occluder u_occluder1;

float softShadow(vec3 light_pos, float light_radius, vec3 occluder_pos, float occluder_radius)
{
    vec3 v0 = light_pos - gl_FragCoord.xyz;
    vec3 v1 = occluder_pos - gl_FragCoord.xyz;

    float r0 = length(v0);
    float r1 = length(v1);

    float a0 = light_radius/r0;
    float a1 = occluder_radius/r1;

    float a = length(cross(v0, v1)) / (r0*r1);
    a = smoothstep(a0 - a1, a0 + a1, a);
    return 1 - (1-a) * pow(a1/a0, 2);
}

uniform vec3 u_color;
uniform bool u_useTexture;
uniform sampler2D u_texture;

uniform bool u_useBumpTexture;
uniform sampler2D u_bumpTexture;
uniform float u_bumpStrength;

uniform bool u_useAtmosphere;
uniform sampler2D u_atmosphereTexture;
uniform float u_time;

uniform Light u_light;
uniform vec3 u_viewPosition;
uniform vec3 u_objectPosition;

in vec3 v_position;
in vec2 v_texCoords;
in vec3 v_normal;
in float v_radius;

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
    // calculate total effect of lights on color
    vec3 L = normalize(u_light.position - u_objectPosition);
    vec3 N = normalize(bump_normal);
    vec3 V = normalize(u_viewPosition - v_position);
    vec3 R = reflect(L, N);

    // ambient
    vec3 ambient = u_light.ambient;
    
    // diffuse
    float diffuse = max( dot(N, L), 0.0 );

    // specular (TODO)

    vec3 light = u_light.color * (ambient + diffuse);

    if (u_useAtmosphere)
    {
        // todo: Add cloud movements
        color += vec4(texture2D(u_atmosphereTexture, v_texCoords).rgb, 0.4);
    }

    // shadows
    light *= softShadow(u_light.position, u_light.radius, u_occluder0.position, u_occluder0.radius);
    light *= softShadow(u_light.position, u_light.radius, u_occluder1.position, u_occluder1.radius);

    color *= vec4(light, 1); 
    
    fragColor = color;
}