"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Title: modelviewer

    Description: simple 3d model viewer with textures and shaders on
    opengl.

    @author Marco Antonio Jurado 20308
    last update: 22/11/2022
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import pygame
import numpy
import random
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import glm

pygame.init()
w,h = (600,600)
pantalla = pygame.display.set_mode((w,h), pygame.OPENGL | pygame.DOUBLEBUF)

vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 vertexColor;

uniform mat4 amatrix;

out vec3 ourColor;


void main()
{
    gl_Position = amatrix * vec4(position, 1.0f);
    ourColor = vertexColor;

}
"""

fragment_shader = """
#version 460

layout (location = 0) out vec4 fragColor;

uniform vec3 color;


in vec3 ourColor;

void main()
{
    // fragColor = vec4(ourColor, 1.0f);
    fragColor = vec4(color, 1.0f);
}
"""

sizes_shader = """
#version 460

layout (location = 0) out vec4 position;
layout (location = 1) out vec4 texturecords;
layout (location = 2) out vec4 normal;

uniform float time; // para que cambie con el tiempo

uniform mat4 ModelMatrix;
uniform mat4 ViewMatrix;
uniform mat4 ProjectionMatrix;

//retornos
out vec2 cord;
out vec3 norms;
out vec3 pos;

in vec3 ourColor;

void main()
{
    pos = (ModelMatrix * vec4(position + normal + cos(time)/10, 1.0)).xyz;
    cord = texturecords;
    norms = normal;
    gl_Position = ModelMatrix * ViewMatrix * ProjectionMatrix * vec4(position + normal * cos(time)/10, 1.0)
}
"""

golden_shader = """
#version 460

out vec4 fragColor;

uniform sampler2D textura;
uniform vec3 light;

in vec3 normales;
in vec3 position;
in vec2 texturecords;

void main()
{
    fragColor = texture(texture, texturecords) * vec4(1,1,0,1.0)
}
"""
# shaders
compiled_vertex_shader = compileShader(vertex_shader, GL_VERTEX_SHADER)
compiled_fragment_shader = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
shader = compileProgram(compiled_vertex_shader, compiled_fragment_shader)
glUseProgram(shader)

# data
vertex_data = numpy.array([
    -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
     0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
     0.0,  0.5, 0.0, 0.0, 0.0, 1.0
], dtype=numpy.float32)

# object en vertex usando data
vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(
    GL_ARRAY_BUFFER,  # tipo de datos
    vertex_data.nbytes,  # tamaño de da data en bytes    
    vertex_data, # puntero a la data
    GL_STATIC_DRAW
)
vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)

glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)
glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
glEnableVertexAttribArray(1)

def calculateMatrix(angle):
    i = glm.mat4(1)
    translate = glm.translate(i, glm.vec3(0, 0, 0))
    rotate = glm.rotate(i, glm.radians(angle), glm.vec3(0, 1, 0))
    scale = glm.scale(i, glm.vec3(1, 1, 1))
    model = translate * rotate * scale
    view = glm.lookAt( glm.vec3(0, 0, 5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    projection = glm.perspective(glm.radians(45), 600/600, 0.1, 1000.0) #using w,h
    amatrix = projection * view * model
    glUniformMatrix4fv( glGetUniformLocation(shader, 'amatrix'), 1, GL_FALSE, glm.value_ptr(amatrix))

# Viewport
glViewport(0, 0, w, h)
glClearColor(0.1, 0.2, 0.3, 1)

running = True
r = 0

while running:
    r += 1
    glClear(GL_COLOR_BUFFER_BIT)

    color1 = random.random()
    color2 = random.random()
    color3 = random.random()

    color = glm.vec3(color1, color2, color3)

    glUniform3fv( glGetUniformLocation(shader,'color'), 1, glm.value_ptr(color))
    calculateMatrix(r)

    pygame.time.wait(50)

    glDrawArrays(GL_TRIANGLES, 0, 3)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False