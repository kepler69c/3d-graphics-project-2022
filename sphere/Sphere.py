import OpenGL.GL as GL             # standard Python OpenGL wrapper
import glfw                        # lean window system wrapper for OpenGL
import numpy as np                 # all matrix manipulations & OpenGL args
from transform import Trackball, identity
from core import Shader, Mesh, load

class Sphere(Mesh):
    """ Class for drawing a cylinder object """
    
    def __init__(self, shader, radius=2, subdivision=3):
        H_ANGLE = np.pi / 180 * 72    # 72 degree = 360 / 5
        V_ANGLE = np.atanf([1/2])  # elevation = 26.565 degree

        hAngle1 = (-np.pi - H_ANGLE) / 2
        hAngle2 = -np.pi / 2

        vertices =  np.zeros(12*3)

        vertices[0] = 0
        vertices[1] = 0
        vertices[2] = radius

        for i in range(1, 6):
            i1 = i * 3         # index for 1st row
            i2 = (i + 5) * 3   # index for 2nd row
            z  = radius * np.sin(V_ANGLE)            # elevaton
            xy = radius * np.cos(V_ANGLE)            # length on XY plane

            vertices[i1] = xy * np.cos(hAngle1)      # x
            vertices[i2] = xy * np.cos(hAngle2)
            vertices[i1 + 1] = xy * np.sin(hAngle1)  # y
            vertices[i2 + 1] = xy * np.sin(hAngle2)
            vertices[i1 + 2] = z                     # z
            vertices[i2 + 2] = -z

            # next horizontal angles
            hAngle1 += H_ANGLE
            hAngle2 += H_ANGLE


        # subdividing
        self.shader = shader
        tmpVertices = np.array([])
        tmpIndices = np.array([])

        for i in range(subdivision):
            pass

        tmpVertices = vertices
        tmpIndices = indices
        vertices.delete()
        indices.delete()
        index = 0
        
        for j in range(0, tmpIndices.size(), 3):
            # get 3 vertices of a triangle
            v1 = tmpVertices[tmpIndices[j] * 3]
            v2 = tmpVertices[tmpIndices[j + 1] * 3]
            v3 = tmpVertices[tmpIndices[j + 2] * 3]

            # compute 3 new vertices by spliting half on each edge
            #         v1       
            #        / \       
            # newV1 *---* newV3
            #      / \ / \     
            #    v2---*---v3   
            #       newV2      
            newV1 = computeHalfVertex(v1, v2, radius)
            newV2 = computeHalfVertex(v2, v3, radius)
            newV3 = computeHalfVertex(v1, v3, radius)

            # add 4 new triangles to vertex array
            vertices = numpy.append(vertices, [ [v1,    newV1, newV3], 
                                                [newV1, v2,    newV2], 
                                                [newV1, newV2, newV3],
                                                [newV3, newV2, v3]])

            # addVertices(v1,    newV1, newV3)
            # addVertices(newV1, v2,    newV2)
            # addVertices(newV1, newV2, newV3)
            # addVertices(newV3, newV2, v3)

            # add indices of 4 new triangles
            numpy.append(indices, [  index,   index+1, index+2, 
                            index+3, index+4, index+5, 
                            index+6, index+7, index+8, 
                            index+9, index+10, index+11]

            # addIndices(index,   index+1, index+2)
            # addIndices(index+3, index+4, index+5)
            # addIndices(index+6, index+7, index+8)
            # addIndices(index+9, index+10,index+11)
            index += 12    # next index


        # colors
        color = np.array([[1, 0, 1], [0, 1, 1]])
        color = np.vstack((color, (np.tile(np.arange(0, nb_circle_points * 2), (3, 1)) % 2).T))
        color = np.array(color, 'f')
        
        attributes = dict(position=vertices, color=color)
        
        super().__init__(shader, attributes=attributes, index=index)


    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        super().draw(primitives=primitives, global_color=(0, 0, 0), **uniforms)


def computeHalfVertex(v1, v2, radius)
    newV = np.array([v1[0] + v1[0], v1[1] + v2[1], v1[2] + v2[2]])
    return newV * (radius / sqrt(np.sum(np.square(newV))))
