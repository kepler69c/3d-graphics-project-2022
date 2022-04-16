#version 330 core

uniform vec3 w_camera_position;
uniform sampler2D diffuse_map;
in vec3 w_position, w_normal;
in vec2 frag_tex_coords;
out vec4 out_color;

void main() {
    out_color = texture(diffuse_map, frag_tex_coords);
}
