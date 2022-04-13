#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL  # standard Python OpenGL wrapper
import glfw  # lean window system wrapper for OpenGL
import numpy as np  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load, Node
from texture import Texture, Textured

class Desert(Textured):
    def __init__(self, shader, N, size):
        # prepare texture modes cycling variables for interactive toggling
        self.wrap = GL.GL_REPEAT
        self.filter = (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)
        self.file = "../Models/Texture/sable.jpg"

        # setup plane mesh to be textured
        mesh = Grid(shader, N, size)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(self.file, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture)


class Grid(Mesh):
    """Class for drawing a desert object"""

    def __init__(self, shader, N, size):
        self.shader = shader

        # positions
        x_position = np.zeros((N, N))
        z_position = np.zeros((N, N))
        # init x_position and y_position
        for j in range(N):
            for i in range(N):
                x_position[j][i] = -size / 2 + i * size / (N - 1)
                z_position[j][i] = -size / 2 + j * size / (N - 1)

        x_position = x_position.flatten()
        z_position = z_position.flatten()
        y_position = np.zeros((N, N)).flatten()

        position = np.vstack((x_position, y_position, z_position)).T

        # indexes
        mat = np.reshape(np.arange(N * N), (N, N))

        top = np.vstack(
            (
                mat[:-1, :-1].flatten(),
                mat[1:, :-1].flatten(),
                mat[:-1, 1:].flatten(),
            )
        ).T.flatten()

        bottom = np.vstack(
            (
                mat[1:, :-1].flatten(),
                mat[1:, 1:].flatten(),
                mat[:-1, 1:].flatten(),
            )
        ).T.flatten()

        index = np.hstack((top, bottom))

        attributes = dict(position=position)

        super().__init__(shader, attributes=attributes, index=index)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        super().draw(primitives=primitives, global_color=(0, 0, 0), **uniforms)


# -------------- main program and scene setup --------------------------------
def main():
    """create a window, add scene objects, then run rendering loop"""
    viewer = Viewer()
    shader = Shader("vertex_shader.vs", "fragment_shader.fs")

    light_dir = (0, 1, 0)

    viewer.add(Desert(shader, 750, 200))

    viewer.run()


if __name__ == "__main__":
    main()  # main function keeps variables locally scoped
