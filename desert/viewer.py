#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load
from texture import Texture, Textured

class Grille:
    """ Class for drawing a desert object """
    
    def __init__(self, shader, nb_circle_points=50):
        self.shader = shader

        N = 20
        M = 50

        # positions
        x_position = np.array((N*M, N*M))
        y_position = np.array((N*M, N*M))
        #init x_position and y_position
        for j in range(N*M):
            for i in range(N*M):
                x_position[j][i] = -250 + i*500/(N*M-1)
                y_position[j][i] = -250 + i*500/(N*M-1)

        z_position = np.zeros((N*M, N*M))

        position = np.vstack((x_position, y_position, z_position)).T

        # indexes
        index = np.vstack((
            np.vstack(position[:N*M-1][0],
                [val for val in position[:N*M-1][1:N*M-1] for _ in (0, 1)],
                position[:N*M-1][N*M-1]),
            np.vstack(position[0][1:],
                [val for val in position[1:N*M-1][1:] for _ in (0, 1)],
                position[N*M-1][1:]),
            [val for val in position[1:][:N*M-1] for _ in (0, 1)]
        )).T.flatten()

        # colors
        color = np.array([[1, 0, 1], [0, 1, 1]])
        color = np.vstack((color, (np.tile(np.arange(0, nb_circle_points * 2), (3, 1)) % 2).T))
        color = np.array(color, 'f')
        
        attributes = dict(position=position, color=color)
        
        super().__init__(shader, attributes=attributes, index=index)


    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        super().draw(primitives=primitives, global_color=(0, 0, 0), **uniforms)

# -------------- Example textured plane class ---------------------------------
class TexturedPlane(Textured):
    """ Simple first textured object """
    def __init__(self, shader, tex_file):
        # prepare texture modes cycling variables for interactive toggling
        self.wrap = GL.GL_REPEAT
        '''self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])'''
        self.filter = (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)
        '''self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])'''
        #self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file = tex_file

        # setup plane mesh to be textured
        base_coords = ((-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0))
        scaled = 100 * np.array(base_coords, np.float32)
        indices = np.array((0, 1, 2, 0, 2, 3), np.uint32)
        mesh = Mesh(shader, attributes=dict(position=scaled), index=indices)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(tex_file, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture)

    '''def key_handler(self, key):
        # cycle through texture modes on keypress of F6 (wrap) or F7 (filtering)
        self.wrap = next(self.wraps) if key == glfw.KEY_F6 else self.wrap
        self.filter = next(self.filters) if key == glfw.KEY_F7 else self.filter
        if key in (glfw.KEY_F6, glfw.KEY_F7):
            texture = Texture(self.file, self.wrap, *self.filter)
            self.textures.update(diffuse_map=texture)'''

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader = Shader("vertex_shader.vs", "fragment_shader.fs")

    #grille = Grille()

    light_dir = (0, 1, 0)
    viewer.add(*[mesh for file in sys.argv[1:]
        for mesh in load(file, shader, light_dir=light_dir)])

    if len(sys.argv) != 2:
        print('Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in'
              ' format supported by assimp.' % (sys.argv[0],))
        viewer.add(TexturedPlane(shader, "sable.jpg"))

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
