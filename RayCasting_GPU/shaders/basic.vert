#version 330

//inputs desde el VAO
in vec3 in_pos;
in vec3 in_color;

//output --> lo recibe el fragment shader
out vec3 v_color;

//variable global que recibimos para aplicar transformaciones al objeto
uniform mat4 Mvp;

void main(){
    gl_Position = Mvp * vec4(in_pos, 1.0);
    v_color = in_color;
}