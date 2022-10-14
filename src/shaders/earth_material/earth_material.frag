struct Light
{
    int lightType;  // 1 = AMBIENT, 2 = DIRECTIONAL, 3 = POINT
    vec3 color;  // used by all lights
    vec3 direction;  // used by point lights
    vec3 position;  // used by point lights
    vec3 attenuation;  // used by point lights
};

uniform Light u_light0;
uniform Light u_light1;
uniform Light u_light2;
uniform Light u_light3;
uniform vec3 u_viewPosition;
uniform float u_specularStrength;
uniform float u_shininess;

vec3 lightCalc(Light light, vec3 point_position, vec3 point_normal)
{
    float ambient = 0;
    float diffuse = 0;
    float specular = 0;
    float attenuation = 1;
    vec3 light_direction = vec3(0, 0, 0);
    
    if (light.lightType == 1)  // ambient light
    {
        ambient = 1;
    }
    else if (light.lightType == 2)  // directional light
    {
        light_direction = normalize(light.direction);
    }
    else if (light.lightType == 3)  // point light
    {
        light_direction = normalize(point_position - light.position);
        float distance = length(light.position - point_position);
        attenuation = 1.0 / (light.attenuation[0] 
                            + light.attenuation[1] * distance 
                            + light.attenuation[2] * distance * distance);
    }
    
    if (light.lightType > 1)  // directional or point light
    {
        point_normal = normalize(point_normal);
        diffuse = max(dot(point_normal, -light_direction), 0.0);
        diffuse *= attenuation;
        if (diffuse > 0)
        {
            vec3 view_direction = normalize(u_viewPosition - point_position);
            vec3 reflect_direction = reflect(light_direction, point_normal);
            specular = max(dot(view_direction, reflect_direction), 0.0);
            specular = u_specularStrength * pow(specular, u_shininess);
        }
    }
    return light.color * (ambient + diffuse + specular);
}

uniform vec3 u_color;
uniform bool u_useTexture;
uniform sampler2D u_texture;
uniform bool u_useBumpTexture;
uniform sampler2D u_bumpTexture;
uniform float u_bumpStrength;

in vec3 v_position;
in vec2 v_texCoords;
in vec3 v_normal;
out vec4 fragColor;

struct Shadow
{
    // direction of light that casts shadow
    vec3 lightDirection;
    // data from camera that produces depth texture
    mat4 projectionMatrix;
    mat4 viewMatrix;
    // texture that stores depth values from shadow camera
    sampler2D depthTexture;
    // regions in shadow multiplied by (1-strength)
    float strength;
    // reduces unwanted visual artifacts
    float bias;
};

uniform bool u_useShadow;
uniform Shadow u_shadow0;
in vec3 v_shadowPosition0;

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
    vec3 light = vec3(0, 0, 0);
    light += lightCalc( u_light0, v_position, bump_normal );
    light += lightCalc( u_light1, v_position, bump_normal );
    light += lightCalc( u_light2, v_position, bump_normal );
    light += lightCalc( u_light3, v_position, bump_normal );
    color *= vec4(light, 1);
    
    if (u_useShadow)
    {
        // determine if surface is facing towards light direction
        float cos_angle = dot(normalize(v_normal), -normalize(u_shadow0.lightDirection));
        bool facing_light = (cos_angle > 0.01);
        // convert range [-1, 1] to range [0, 1]
        // for UV coordinate and depth information
        vec3 shadow_coord = (v_shadowPosition0.xyz + 1.0) / 2.0;
        float closest_distance_to_light = texture2D(u_shadow0.depthTexture, shadow_coord.xy).r;
        float fragment_distance_to_light = clamp(shadow_coord.z, 0, 1);
        // determine if fragment lies in shadow of another object
        bool in_shadow = (fragment_distance_to_light > closest_distance_to_light + u_shadow0.bias);
        if (facing_light && in_shadow)
        {
            float s = 1.0 - u_shadow0.strength;
            color *= vec4(s, s, s, 1);
        }
    }  
    
    fragColor = color;
}