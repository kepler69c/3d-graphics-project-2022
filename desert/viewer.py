#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL  # standard Python OpenGL wrapper
import glfw  # lean window system wrapper for OpenGL
import numpy as np  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load, Node
from texture import Texture, Textured
import random as rng
from animation import KeyFrameLoopControlNode, TransformKeyFrames
from transform import scale, rotate, translate, quaternion, quaternion_from_euler


class Desert(Textured):
    """Class for drawing a desert object"""

    def __init__(self, shader, light, N=750, size=1800):
        # prepare texture modes and light
        self.wrap = GL.GL_REPEAT
        self.filter = (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)
        self.file = "../Models/Texture/sable.jpg"
        self.light_dir = light[0]
        self.light_ambiant = light[1]
        self.light_diffuse = light[2]
        self.light_specular = light[3]

        # setup plane mesh to be textured
        mesh = Grid(shader, N, size)

        texture = Texture(self.file, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        super().draw(
            primitives=primitives,
            light_dir=self.light_dir,
            light_ambiant=self.light_ambiant,
            light_diffuse=self.light_diffuse,
            light_specular=self.light_specular,
            **uniforms
        )


class Grid(Mesh):
    """Class for desert mesh construction"""

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


class Castle(Node):
    def __init__(self, shader, light):
        super().__init__()

        self.transform = translate(y=+10) @ scale(x=0.01, y=0.01, z=0.01)
        self.add(
            *load(
                "../Models/Castle/castle_no_floor.obj",
                shader,
                light_dir=light[0],
                light_ambiant=light[1],
                light_diffuse=light[2],
                light_specular=light[3],
            )
        )


class Cactus(Node):
    def __init__(self, shader, light, position=(0.0, 0.0, 0.0)):
        super().__init__()

        tex_list = [
            "../Models/Cactus1/10436_Cactus_v1_max2010_it2.obj",
            "../Models/Cactus1/10436_Cactus_v1_max2010_it2.obj",
            "../Models/Cactus1/10436_Cactus_v1_max2010_it2.obj",
            "../Models/Cactus1/10436_Cactus_v1_max2010_it2.obj",
            "../Models/Cactus1/10436_Cactus_v1_max2010_it2.obj",
            "../Models/Cactus1/10436_Cactus_v1_max2010_it2.obj",
            "../Models/Cactus1/10436_Cactus_v1_max2010_it2.obj",
            "../Models/Cactus2/Models/SW01_1.obj",
            "../Models/Cactus2/Models/SW01_2.obj",
            "../Models/Cactus2/Models/SW01_3.obj",
            "../Models/Cactus2/Models/SW01_4.obj",
            "../Models/Cactus2/Models/SW01_5.obj",
            "../Models/Cactus2/Models/SW01_6.obj",
        ]

        self.transform = (
            translate(position) @ rotate((1, 0, 0), -90.0) @ scale(0.7, 0.7, 0.7)
        )

        self.add(
            *load(
                rng.choice(tex_list),
                shader,
                light_dir=light[0],
                light_ambiant=light[1],
                light_diffuse=light[2],
                light_specular=light[3],
            )
        )


class Dragon(Node):
    def __init__(self, shader, light):
        super().__init__()

        self.radius = 100
        self.time = 10

        self.interval = np.linspace(0, 2 * np.pi, 101)[:-1]
        pos_x = np.cos(self.interval) * self.radius
        pos_z = np.sin(self.interval) * self.radius

        keys = np.linspace(0, self.time, 101)[:-1]
        translate_keys = {
            keys[i]: np.array((pos_x[i], 0, pos_z[i])) for i in range(100)
        }
        rotate_keys = {
            keys[i]: quaternion_from_euler(0, -(i / 100) * 360.0, 0) for i in range(100)
        }
        scale_keys = {0: 1}

        self.body = KeyFrameLoopControlNode(translate_keys, rotate_keys, scale_keys)
        self.body.add(
            *load(
                "../Models/Dragon/dargeon.obj",
                shader,
                light_dir=light[0],
                light_ambiant=light[1],
                light_diffuse=light[2],
                light_specular=light[3],
            )
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
            *load(
                "../Models/Dragon/left-wing.obj",
                shader,
                light_dir=light[0],
                light_ambiant=light[1],
                light_diffuse=light[2],
                light_specular=light[3],
            )
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
            *load(
                "../Models/Dragon/right-wing.obj",
                shader,
                light_dir=light[0],
                light_ambiant=light[1],
                light_diffuse=light[2],
                light_specular=light[3],
            )
        )

        self.body.add(self.left_wing)
        self.body.add(self.right_wing)

        self.transform = translate(0, 130, 0) @ scale(.5, .5, .5)

        self.add(self.body)

    def key_handler(self, key):
        # cycle through texture modes on keypress of F6 (wrap) or F7 (filtering)
        if key in (glfw.KEY_RIGHT, glfw.KEY_LEFT):
            if key == glfw.KEY_LEFT:
                if self.radius + 10 <= 400:
                    self.radius += 10
            if key == glfw.KEY_RIGHT:
                if self.radius - 10 >= 0:
                    self.radius -= 10

            pos_x = np.cos(self.interval) * self.radius
            pos_z = np.sin(self.interval) * self.radius

            keys = np.linspace(0, self.time, 101)[:-1]
            translate_keys = {
                keys[i]: np.array((pos_x[i], 0, pos_z[i])) for i in range(100)
            }
            rotate_keys = {
                keys[i]: quaternion_from_euler(0, -(i / 100) * 360.0, 0)
                for i in range(100)
            }
            scale_keys = {0: 1}
            self.body.keyframes = TransformKeyFrames(
                translate_keys, rotate_keys, scale_keys
            )


# -------------- main program and scene setup --------------------------------
def main():
    """create a window, add scene objects, then run rendering loop"""
    viewer = Viewer()
    shader_desert = Shader("vertex_shader_desert.vs", "fragment_shader.fs")
    shader_obj = Shader("vertex_shader_objects.vs", "fragment_shader.fs")

    light_dir = (0.0, 1.0, 0.0)
    light_ambiant = (1.0, 0.94, 0.84)
    light_diffuse = (1.0, 0.72, 0.56)
    light_specular = (0.5, 0.5, 0.5)

    light = (light_dir, light_ambiant, light_diffuse, light_specular)

    viewer.add(Desert(shader_desert, light))
    viewer.add(Castle(shader_obj, light))
    viewer.add(Cactus(shader_obj, light, (150, 15, 400)))
    viewer.add(Cactus(shader_obj, light, (-640, 15, 100)))
    viewer.add(Cactus(shader_obj, light, (337, 15, -334)))
    viewer.add(Cactus(shader_obj, light, (-64, 15, -184)))
    viewer.add(Cactus(shader_obj, light, (-699, 15, 605)))
    viewer.add(Cactus(shader_obj, light, (326, 15, -639)))
    viewer.add(Cactus(shader_obj, light, (326, 15, -639)))
    viewer.add(Cactus(shader_obj, light, (-115, 15, 522)))
    viewer.add(Cactus(shader_obj, light, (327, 15, -257)))
    viewer.add(Cactus(shader_obj, light, (-226, 15, 347)))
    viewer.add(Cactus(shader_obj, light, (-321, 15, -144)))
    viewer.add(Cactus(shader_obj, light, (-144, 15, 654)))
    viewer.add(Cactus(shader_obj, light, (715, 15, 175)))
    viewer.add(Cactus(shader_obj, light, (-352, 15, 542)))
    viewer.add(Cactus(shader_obj, light, (-51, 15, -711)))
    viewer.add(Cactus(shader_obj, light, (-399, 15, -293)))
    viewer.add(Cactus(shader_obj, light, (258, 15, -221)))
    viewer.add(Cactus(shader_obj, light, (211, 15, 126)))
    viewer.add(Cactus(shader_obj, light, (348, 15, 614)))

    viewer.add(Dragon(shader_obj, light))

    viewer.run()


if __name__ == "__main__":
    main()  # main function keeps variables locally scoped
