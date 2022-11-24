"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Title: modelviewer

    Description: simple 3d model viewer with textures and shaders on
    opengl.

    @author Marco Antonio Jurado 20308
    last update: 22/11/2022
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import pygame
from pygame import image
from numpy import array, float32
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import glm
from Object import *
from math import sin,cos

pygame.init()
w,h = (600,600)
pantalla = pygame.display.set_mode((w,h), pygame.OPENGL | pygame.DOUBLEBUF)
reloj = pygame.time.Clock()

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

uniform float clock; // para que cambie con el tiempo

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
    pos = (ModelMatrix * vec4(position + normal + cos(clock)/10, 1.0)).xyz;
    cord = texturecords;
    norms = normal;
    gl_Position = ModelMatrix * ViewMatrix * ProjectionMatrix * vec4(position + normal * cos(clock)/10, 1.0);
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
    fragColor = texture(texture, texturecords) * vec4(1,1,0,1.0);
}
"""


texture_surface = pygame.image.load("./objs/plant.bmp")
texture_data = pygame.image.tostring(texture_surface,"RGB",1)
width = texture_surface.get_width()
height = texture_surface.get_height()
texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
glGenerateMipmap(GL_TEXTURE_2D)

glEnable(GL_DEPTH_TEST)

# loading object
plant = Object('.\objs\plant.obj')
vertex_data = array(plant.vertices, dtype = float32) # aqui se cargaba un cubo


# object en vertex usando data
vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)
glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(12))
glEnableVertexAttribArray(0)
glVertexAttribPointer( 2, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(24))
glEnableVertexAttribArray(0)

vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)

ProjectionMatrix = glm.perspective(glm.radians(45), 1260/900, 0.1, 1000.0)

def calculateMatrix(angle):
    if temp != None:
        i = glm.mat4(1)
        translate = glm.translate(i, glm.vec3(0, 0, 0))
        rotate = glm.rotate(i, glm.radians(angle), glm.vec3(0, 1, 0))
        scale = glm.scale(i, glm.vec3(1, 1, 1))
        model = translate * rotate * scale
        view = glm.lookAt( glm.vec3(0, 0, 5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))

        return ProjectionMatrix * view * model

def currentShade(vertex, fragment):
    if vertex and fragment:
        return compileProgram(compileShader(vertex, GL_VERTEX_SHADER), compileShader(fragment, GL_FRAGMENT_SHADER))
    else:
        return None

# Viewport
glViewport(0, 0, w, h)
glClearColor(0.1, 0.2, 0.3, 1)
temp = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER), compileShader(fragment_shader, GL_FRAGMENT_SHADER))
light = glm.vec3(0,0,0)
clock = 0
r = 0


ViewMatrix = calculateMatrix(r)


running = True

calculateMatrix(r)
while running:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    mouse = pygame.mouse.get_rel()
    teclado = pygame.key.get_pressed()

    glUseProgram(temp)

    ViewMatrix = calculateMatrix(r)
    glUniformMatrix4fv( glGetUniformLocation(temp, 'ViewMatrix'), 1, GL_FALSE, glm.value_ptr(ViewMatrix))

    glUniformMatrix4fv( glGetUniformLocation(temp, "ProjectionMatrix"), 1, GL_FALSE, glm.value_ptr(ProjectionMatrix))

    glUniform1i( glGetUniformLocation(temp, "tex"), 0)

    glUniform1f( glGetUniformLocation(temp, "clock"), clock)

    glUniform3fv( glGetUniformLocation(temp, "light"), 1, glm.value_ptr(light))


    pygame.time.wait(50)

    glDrawArrays(GL_TRIANGLES, 0, len(vertex_data))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                temp = currentShade(vertex_shader, fragment_shader)
            if event.key == pygame.K_2:
                temp = currentShade(sizes_shader, fragment_shader)
            if event.key == pygame.K_3:
                temp = currentShade(golden_shader, fragment_shader)
            if event.key == pygame.K_RIGHT:
                r += 0.3
                light.x += 15 * clock
                calculateMatrix(r)
            if event.key == pygame.K_LEFT:
                r -= 0.3
                light.x -= 15 * clock
                calculateMatrix(r)
        r += (mouse[0] / 10)

    clock += 0.06