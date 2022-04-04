#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL  # standard Python OpenGL wrapper
import glfw  # lean window system wrapper for OpenGL
import numpy as np  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load, Node
from texture import Texture, Textured
from animation import KeyFrameLoopControlNode
from transform import quaternion, quaternion_from_euler

# -------------- Example textured plane class ---------------------------------
class TexturedPlane(Textured):
    """Simple first textured object"""

    def __init__(self, shader, tex_file):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle(
            [
                GL.GL_REPEAT,
                GL.GL_MIRRORED_REPEAT,
                GL.GL_CLAMP_TO_BORDER,
                GL.GL_CLAMP_TO_EDGE,
            ]
        )
        self.filters = cycle(
            [
                (GL.GL_NEAREST, GL.GL_NEAREST),
                (GL.GL_LINEAR, GL.GL_LINEAR),
                (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR),
            ]
        )
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file = tex_file

        # setup plane mesh to be textured
        base_coords = ((-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0))
        scaled = 100 * np.array(base_coords, np.float32)
        indices = np.array((0, 1, 2, 0, 2, 3), np.uint32)
        mesh = Mesh(shader, attributes=dict(position=scaled), index=indices)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(tex_file, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture)

    def key_handler(self, key):
        # cycle through texture modes on keypress of F6 (wrap) or F7 (filtering)
        self.wrap = next(self.wraps) if key == glfw.KEY_F6 else self.wrap
        self.filter = next(self.filters) if key == glfw.KEY_F7 else self.filter
        if key in (glfw.KEY_F6, glfw.KEY_F7):
            texture = Texture(self.file, self.wrap, *self.filter)
            self.textures.update(diffuse_map=texture)


class Dragon(Node):
    def __init__(self, shader, light_dir):
        super().__init__()

        self.body = Node()
        self.body.add(
            *load("../Models/Dragon/dargeon.obj", shader, light_dir=light_dir)
        )

        translate_keys = {0: (5, 51, -7)}
        rotate_keys = {
            0: quaternion(),
            1: quaternion_from_euler(10, 0, 0),
            3: quaternion_from_euler(-45, 0, 0),
            4: quaternion(),
        }
        scale_keys = {0: 1}
        self.left_wing = KeyFrameLoopControlNode(
            translate_keys, rotate_keys, scale_keys
        )
        self.left_wing.add(
            *load("../Models/Dragon/left-wing.obj", shader, light_dir=light_dir)
        )

        translate_keys = {0: (-5, 51, -7)}
        rotate_keys = {
            0: quaternion(),
            1: quaternion_from_euler(-10, 0, 0),
            3: quaternion_from_euler(45, 0, 0),
            4: quaternion(),
        }
        scale_keys = {0: 1}
        self.right_wing = KeyFrameLoopControlNode(
            translate_keys, rotate_keys, scale_keys
        )
        self.right_wing.add(
            *load("../Models/Dragon/right-wing.obj", shader, light_dir=light_dir)
        )

        self.body.add(self.left_wing)
        self.body.add(self.right_wing)

        self.add(self.body)


# -------------- main program and scene setup --------------------------------
def main():
    """create a window, add scene objects, then run rendering loop"""
    viewer = Viewer()
    shader = Shader("texture.vert", "texture.frag")

    light_dir = (0, 1, 0)
    viewer.add(Dragon(shader, light_dir))

    # start rendering loop
    viewer.run()


if __name__ == "__main__":
    main()  # main function keeps variables locally scoped
