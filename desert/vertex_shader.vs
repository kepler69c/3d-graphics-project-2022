#version 330 core

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
in vec3 position;

out vec2 frag_tex_coords;

float hash31(in vec3 p){
  return fract(sin(dot(p,vec3(12.9898,78.233,45.5432)))*43758.5453123);
}

float vNoise(in vec3 p){
  vec3 c = floor(p);
  vec3 f = fract(p);
  f = f * f * (3-2*f);
  float v1 = hash31(c);
  float v2 = hash31(c + vec3(1,0,0));
  float v3 = hash31(c + vec3(0,1,0));
  float v4 = hash31(c + vec3(1,1,0));
  float v5 = hash31(c + vec3(0,0,1));
  float v6 = hash31(c + vec3(1,0,1));
  float v7 = hash31(c + vec3(0,1,1));
  float v8 = hash31(c + vec3(1,1,1));
  float m1x = mix(v1, v2, f.x);
  float m2x = mix(v3, v4, f.x);
  float m3x = mix(v5, v6, f.x);
  float m4x = mix(v7, v8, f.x);
  float m5y = mix(m1x, m2x, f.y);
  float m6y = mix(m3x, m4x, f.y);
  float m7z = mix(m5y, m6y, f.z);
  return m7z;
}

float fNoise(in vec3 p, in float amp, in float freq, in float pers, in int nbOct) {
  float f = freq;
  float a = amp;
  float n = 0;
  for (int i = 0; i < nbOct; i++){
    n += vNoise(p * f) * a;
    f = f * 2;
    a = a * pers;
  }
  return n;
}

void main() {
    vec3 pos = position;
    pos.y = fNoise(pos, 20, 0.02, 0.1, 15);
    gl_Position = projection * view * model * vec4(pos, 1);
    frag_tex_coords = pos.xz;
}

