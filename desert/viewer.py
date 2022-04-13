#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load
from texture import Texture, Textured
from transform import identity

class Node:
    """ Scene graph transform and parameter broadcast node """
    def __init__(self, children=(), transform=identity()):
        self.transform = transform
        self.world_transform = identity()
        self.children = list(iter(children))

    def add(self, *drawables):
        """ Add drawables to this node, simply updating children list """
        self.children.extend(drawables)

    def draw(self, model=identity(), **other_uniforms):
        """ Recursive draw, passing down updated model matrix. """
        self.world_transform = model @ self.transform
        for child in self.children:
            child.draw(model=self.world_transform, **other_uniforms)

    def key_handler(self, key):
        """ Dispatch keyboard events to children with key handler """
        for child in (c for c in self.children if hasattr(c, 'key_handler')):
            child.key_handler(key)

class Grid(Node):
    """ Class for drawing a desert object """
    
    def __init__(self, shader, nb_circle_points=50):
        self.shader = shader

        N = 100

        # positions
        x_position = np.zeros((N, N))
        y_position = np.zeros((N, N))
        #init x_position and y_position
        for j in range(N):
            for i in range(N):
                x_position[j][i] = -250 + i*500/(N-1)
                y_position[j][i] = -250 + j*500/(N-1)

        z_position = np.zeros((N, N)).flatten()
        x_position = x_position.flatten()
        y_position = y_position.flatten()

        position = np.vstack((x_position, y_position, z_position)).T

        # indexes
        mat = np.reshape(np.arange(N*N), (N,N))

        top = np.vstack([
            mat[:-1][:-1].flatten(),
            mat[1:][:-1].flatten(),
            mat[:-1][1:].flatten(),
        ]).T.flatten()

        bottom = np.vstack([
            mat[:-1][1:].flatten(),
            mat[1:][:-1].flatten(),
            mat[1:][1:].flatten(),
        ]).T.flatten()

        index = np.hstack([top, bottom])
        
        attributes = dict(position=position)
        
        super().__init__()


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

    grid = Grid(shader)

    terrain = Node()
    terrain.add(grid)

    viewer.add(terrain)

    light_dir = (0, 1, 0)
    viewer.add(*[mesh for file in sys.argv[1:]
        for mesh in load(file, shader, light_dir=light_dir)])

    if len(sys.argv) != 2:
        print('Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in'
              ' format supported by assimp.' % (sys.argv[0],))
        #viewer.add(TexturedPlane(shader, "sable.jpg"))

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
