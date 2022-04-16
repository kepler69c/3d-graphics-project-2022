#version 330 core

uniform vec3 w_camera_position;
uniform sampler2D diffuse_map;
//uniform vec3 k_a, k_s;
vec3 k_a = vec3(0);
vec3 k_s = vec3(0);
in vec3 w_position, w_normal;
in vec2 frag_tex_coords;
out vec4 out_color;

// light
uniform vec3 light_dir;
uniform vec3 light_ambient;
uniform vec3 light_diffuse;
uniform vec3 light_specular;

void main() {
    vec3 k_d = texture(diffuse_map, frag_tex_coords).xyz;
    vec3 n = normalize(w_normal);
    vec3 l = normalize(light_dir);
    float d = max(0, dot(n, l));
    vec3 ref = reflect(-l, n);
    vec3 r = normalize(ref);
    vec3 vec = w_camera_position - w_position;
    vec3 v = normalize(vec);
    float sp = pow(max(0, dot(r, v)), 5);

    vec3 ambiant = light_ambient * k_a;
    vec3 diffuse = light_diffuse * d * k_d;
    vec3 specular = light_specular * sp * k_s;

    vec3 I = light_ambient + diffuse + specular;
    out_color = vec4(I, 1);
}
