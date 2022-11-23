import numpy
class Object(object):
    def __init__(self, filename):
        self.vertices = []
        self.faces = []
        self.vtvertex = []
        self.normals = []
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