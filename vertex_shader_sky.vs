#version 330 core

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
in vec3 position;
in vec2 tex_coord;

out vec3 w_position;
out vec2 frag_tex_coords;

void main() {
    w_position = (model * vec4(position, 1)).xyz;

    gl_Position = projection * view * model * vec4(position, 1);
    frag_tex_coords = tex_coord;
}
