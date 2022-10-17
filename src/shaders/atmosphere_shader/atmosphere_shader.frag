struct Light
{
    vec3 ambient;
    vec3 color;
    vec3 position;
    float radius;
};

// light uniforms
uniform Light u_light;
uniform vec3 u_viewPosition;
uniform vec3 u_objectPosition;

// color uniforms
uniform vec4 u_color;

// atmosphere uniforms
uniform bool u_useAtmosphere;
uniform sampler2D u_atmosphereTexture;

// vertex shader data
in vec3 v_position;
in vec2 v_texCoords;
in vec3 v_normal;
in float v_radius;

// out data
out vec4 fragColor;

void main()
{
    // calculate total effect of lights on color
    vec3 L = normalize(u_light.position - u_objectPosition);
    vec3 N = normalize(v_normal);
    vec3 V = normalize(u_viewPosition - v_position);
    vec3 R = reflect(-L, N);

    // ambient
    vec3 ambient = u_light.ambient;
    
    // diffuse
    float diffuse = max( dot(N, L), 0.0 );

    // specular (TODO)
    float specular = 0.0;

    float specular_strength = 0.5;
    specular = pow( max( dot(V, R), 0.0 ), 32 ) * specular_strength;

    vec3 light = u_light.color * (ambient + diffuse + specular);

    // calculate color
    fragColor = u_color;
}