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
    // calculate color
    fragColor = u_color;
}