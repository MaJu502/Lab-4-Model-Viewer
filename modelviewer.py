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
# Viewport
glViewport(0, 0, w, h)
glClearColor(0.1, 0.2, 0.3, 1)

vertex_shader = '''
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 vertexColor;

uniform mat4 ViewMatrix;

void main()
{
    gl_Position = ViewMatrix * vec4(position, 1.0f);

}
'''

fragment_shader = '''
#version 460

out vec4 FragColor;


void main()
{
    FragColor = vec4(1,1,1, 1.0f);
}
'''

golden_vertex = '''
#version 450 core
layout (location = 0) in vec3 position;
layout (location = 2) in vec2 texturecords;
uniform mat4 ViewMatrix;

out vec2 cord;

in vec3 ourColor;

void main()
{
  cord = texturecords;
  gl_Position = ViewMatrix * vec4(position, 1.0);
}
'''

golden_shader = '''
#version 450 core
out vec4 FragColor;
in vec2 cord;

uniform sampler2D theTexture;

void main()
{
  FragColor = texture(theTexture, cord) * vec4(1.0, 1.0, 0.0, 1.0);
}
'''

color_storm_vertex = """
#version 450 core
layout (location = 0) in vec3 position;
layout (location = 2) in vec2 texturecords;
layout (location = 1) in vec2 normals;

uniform mat4 ViewMatrix;

out vec2 cord;
out vec2 norms;

void main()
{
  cord = texturecords;
  norms = normals;
  gl_Position = ViewMatrix * vec4(position, 1.0);
}
"""

color_storm_fragment = '''
#version 450 core
out vec4 FragColor;

in vec2 cord;
in vec2 norms;

uniform sampler2D theTexture;
uniform float time;

void main()
{
  if (cos(time)>=0 && cos(time)<0.5){
        FragColor = texture(theTexture, cord) * vec4(0.0,0.71,1.0,1.0);
  } else if (cos(time)>=0.5 && cos(time)<1) {
        FragColor = texture(theTexture, cord) * vec4(0.0,1.0,0.4,1.0);
  } else if (cos(time)<0 && cos(time)>=-0.5) {
        FragColor = texture(theTexture, cord) * vec4(0.6,1.0,0.0,1.0);
  } else if (cos(time)<0 && cos(time)>=-1) {
        FragColor = texture(theTexture, cord) * vec4(1.0,0.75,0.345,1.0);
  }
}
'''

explode_v ='''
#version 450 core
layout (location = 0) in vec3 position;
layout (location = 2) in vec2 texturecords;
layout (location = 1) in vec3 normals;

uniform mat4 ViewMatrix;
uniform mat4 ModelMatrix;
uniform mat4 ProjectionMatrix;
uniform float time;

out vec2 cord;
out vec3 norms;
out vec3 pos;

void main()
{
    cord = texturecords;
    norms = normals;
    pos = (ModelMatrix * vec4(position + normals * cos(time)/10, 1.5)).xyz;
    gl_Position = ProjectionMatrix * ViewMatrix * ModelMatrix * vec4(position + normals * cos(time)/10, 1.5);
}
'''
possible = '''
#version 450 core
out vec4 FragColor;

in vec2 cord;
in vec3 norms;
in vec3 pos;

uniform sampler2D theTexture;

void main()
{
  FragColor = texture(theTexture, cord) * vec4(0.0, 1.0, 0.0, 1.0);
}
'''




sh1 = compileProgram( compileShader(vertex_shader, GL_VERTEX_SHADER), compileShader(fragment_shader,GL_FRAGMENT_SHADER) )
sh2 = compileProgram( compileShader(golden_vertex, GL_VERTEX_SHADER), compileShader(golden_shader,GL_FRAGMENT_SHADER) )
sh3 = compileProgram( compileShader(color_storm_vertex, GL_VERTEX_SHADER), compileShader(color_storm_fragment,GL_FRAGMENT_SHADER) )
sh4 = compileProgram( compileShader(explode_v, GL_VERTEX_SHADER), compileShader(possible,GL_FRAGMENT_SHADER) )



# loading object
plant = Object('.\objs\plant.obj')
triangle_count,vertex_data = plant.object_data()

texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

image = pygame.image.load('.\objs\plant.bmp').convert()
image_width, image_height = image.get_rect().size
image_data = pygame.image.tostring(image, 'RGB')
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image_width, image_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
glGenerateMipmap(GL_TEXTURE_2D)



# object en vertex usando data
vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)

#vertice
glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)

#normales
glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
glEnableVertexAttribArray(1)

#textura
glVertexAttribPointer( 2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)


ProjectionMatrix = glm.perspective(glm.radians(45), 1260/900, 0.1, 1000.0)

def calculateMatrix(angle):
    if temp != None:
        i = glm.mat4(1)
        translate = glm.translate(i, glm.vec3(0, -1.5, 0))
        rotate = glm.rotate(i, glm.radians(angle), glm.vec3(0, 1, 0))
        scale = glm.scale(i, glm.vec3(0.5,0.5,0.5))
        model = translate * rotate * scale
        view = glm.lookAt( glm.vec3(0, 0, 5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))

        return ProjectionMatrix * view * model, model

time = 0.0
r = 0
temp = sh2
ViewMatrix,ModelMatrix = calculateMatrix(r)
pygame.display.flip()
running = True
calculateMatrix(r)
while running:
    glClear(GL_COLOR_BUFFER_BIT)

    mouse = pygame.mouse.get_rel()
    teclado = pygame.key.get_pressed()

    glUseProgram(temp)

    ViewMatrix,ModelMatrix  = calculateMatrix(r)
    glUniformMatrix4fv( glGetUniformLocation(temp, 'ViewMatrix'), 1, GL_FALSE, glm.value_ptr(ViewMatrix))

    glUniformMatrix4fv( glGetUniformLocation(temp, "ProjectionMatrix"), 1, GL_FALSE, glm.value_ptr(ProjectionMatrix))

    glUniformMatrix4fv( glGetUniformLocation(temp, "ModelMatrix"), 1, GL_FALSE, glm.value_ptr(ModelMatrix))

    glUniform1i( glGetUniformLocation(temp, "tex"), 0)

    glUniform1f( glGetUniformLocation(temp, "time"), time)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glDrawArrays(GL_TRIANGLES, 0, triangle_count)

    pygame.display.flip()

    r += 0.03
    time += 0.06

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                temp = sh1
            if event.key == pygame.K_2:
                temp = sh2
            if event.key == pygame.K_3:
                temp = sh3
            if event.key == pygame.K_4:
                temp = sh4
            if event.key == pygame.K_RIGHT:
                r += 10
                calculateMatrix(r)
            if event.key == pygame.K_LEFT:
                r -= 10
                calculateMatrix(r)
        r += (mouse[0] / 1)

    time += 0.06