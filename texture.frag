#version 330 core

uniform vec3 light_dir;
uniform vec3 w_camera_position;
uniform sampler2D diffuse_map;
in vec3 w_position, w_normal;
in vec2 frag_tex_coords;
out vec4 out_color;

vec3 k_a = vec3(0);
vec3 k_s = vec3(0);

void main() {
    vec3 k_d = texture(diffuse_map, frag_tex_coords).xyz;
    vec3 n = normalize(w_normal);
    vec3 l = normalize(light_dir);
    float d = max(0, dot(n, l));
    vec3 ref = reflect(-l, n);
    vec3 r = normalize(ref);
    vec3 vec = w_camera_position - w_position;
    vec3 v = normalize(vec);
    float sp = pow(max(0, dot(r, v)), 50);
    vec3 I = k_a + k_d * d + k_s * sp;
    out_color = vec4(I, 1);
}
