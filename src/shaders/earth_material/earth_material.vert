uniform mat4 u_proj;
uniform mat4 u_view;
uniform mat4 u_model;
in vec3 a_position;
in vec2 a_texCoords;
in vec3 a_vNormal;
out vec3 v_position;
out vec2 v_texCoords;
out vec3 v_normal;

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
out vec3 v_shadowPosition0;

void main()
{
    gl_Position = u_proj * u_view * u_model * vec4(a_position, 1);
    v_position = vec3(u_view * vec4(a_position, 1));
    v_texCoords = a_texCoords;
    v_normal = normalize(mat3(u_model) * a_vNormal);
    // Shadow
    if (u_useShadow)
    {
        vec4 temp0 = u_shadow0.projectionMatrix * u_shadow0.viewMatrix * u_model * vec4(a_position, 1);
        v_shadowPosition0 = vec3(temp0);
    } 
}