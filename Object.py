import struct
import numpy
class Object(object):
    def __init__(self, filename):
        self.vertices = []
        self.faces = []
        self.vtvertex = []
        self.normals = []

        self.pol_count = 0
        self.retorno = []

        with open(filename) as f:
            self.lines = f.read().splitlines()


        for line in self.lines:
            #por cada linea del archivo obj
            try:
                prefix, value = line.split(' ', 1) #split para obtener el tipo de dato que es cara o vertice
            except:
                continue

            match prefix:
                case 'v':
                    #vertice
                    self.vertices.append( list(map(float,value.split(' '))))

                case'f' :
                    #cara
                    self.faces.append([  list(map(int, vert.split('/'))) for vert in value.split(' ')] )

                case'vt' :
                    #vt
                    self.vtvertex.append( list(map(float, value.split(' '))))

                case'vn' :
                    #vn
                    self.normals.append( list(map(float, value.split(' '))))
        #print(self.vtvertex)

    def load_model(self):
        for face in self.faces:
            temp_faces = []
            temp_texture = []
            temp_normal = []

            for actual_v in face:
                temp_faces.append(self.vertices[actual_v[0] - 1])

                temp_textures = self.vtvertex[actual_v[1] - 1]
                temp_texture.append(temp_textures)

                temp_normals = self.normals[actual_v[2] - 1] if len(self.normals) - 1 >= actual_v[2] - 1 else (0, 0, 0)
                temp_normal.append(temp_normals)
            
            

            for index in range(len(temp_faces) - 2):
                self.pol_count += 3
                vertex = (temp_faces[0], temp_faces[index+1], temp_faces[index+2])
                t_normals = (temp_normal[0], temp_normal[index+1], temp_normal[index+2])
                textures = (temp_texture[0], temp_texture[index+1], temp_texture[index+2])

                for i in range(3):
                    # Vertex
                    self.retorno.append(vertex[i][0])
                    self.retorno.append(vertex[i][1])
                    self.retorno.append(vertex[i][2])

                    # Normals        
                    self.retorno.append(t_normals[i][0])
                    self.retorno.append(t_normals[i][1])
                    self.retorno.append(t_normals[i][2])
                    
                    # Textures        
                    self.retorno.append(textures[i][0])
                    self.retorno.append(1 - textures[i][1])

        
        
    def object_data(self):
        self.load_model()
        vertex_data = numpy.array(self.retorno, dtype=numpy.float32)
        return self.pol_count, vertex_data
