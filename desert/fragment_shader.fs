#version 330 core

uniform sampler2D diffuse_map;
uniform vec3 light_dir;
uniform vec3 k_a, k_s;
uniform vec3 w_camera_position;

float s = 5;

in vec2 frag_tex_coords;
in vec3 w_position, w_normal;

out vec4 out_color;

void main() {
    // vec3 n = normalize(w_normal);
    // vec3 v = normalize(w_camera_position - w_position);

    // vec3 diffuse = texture(diffuse_map, frag_tex_coords).xyz * max(0, dot(n, light_dir));
    // vec3 specular = k_s * max(0, pow(dot(reflect(-light_dir, n), v), s));

    out_color = texture(diffuse_map, frag_tex_coords);
}
