#!/usr/bin/env python3
"""
Python OpenGL practical application.
"""

import OpenGL.GL as GL             # standard Python OpenGL wrapper
import glfw                        # lean window system wrapper for OpenGL
import numpy as np                 # all matrix manipulations & OpenGL args
from transform import Trackball, identity
from core import Shader, Mesh, load

class Cylinder(Mesh):
    """ Class for drawing a cylinder object """
    
    def __init__(self, shader, nb_circle_points=50):
        self.shader = shader

        # positions
        x_position = np.cos(np.linspace(0, 4*np.pi, 2*nb_circle_points + 1)[:-1])
        y_position = np.sin(np.linspace(0, 4*np.pi, 2*nb_circle_points + 1)[:-1])
        z_position = np.hstack((-np.ones(nb_circle_points), np.ones(nb_circle_points)))

        position = np.vstack((
            np.array([0, 0, -1]),
            np.array([0, 0, 1]),
            np.vstack((x_position, y_position, z_position)).T,
        ))

        # indexes
        bot_circle = np.vstack((
            np.zeros(nb_circle_points),
            np.append(np.arange(1, nb_circle_points), 0) + 2,
            np.arange(0, nb_circle_points) + 2,
        )).T.flatten()

        top_circle = np.vstack((
            np.ones(nb_circle_points),
            np.arange(0, nb_circle_points) + 2 + nb_circle_points,
            np.append(np.arange(1, nb_circle_points), 0) + 2 + nb_circle_points,
        )).T.flatten()

        bl_walls = np.vstack((
            np.arange(0, nb_circle_points) + 2,
            np.append(np.arange(1, nb_circle_points), 0) + 2,
            np.arange(0, nb_circle_points) + 2 + nb_circle_points
        )).T.flatten()

        tr_walls = np.vstack((
            np.append(np.arange(1, nb_circle_points), 0) + 2 + nb_circle_points,
            np.arange(0, nb_circle_points) + 2 + nb_circle_points,
            np.append(np.arange(1, nb_circle_points), 0) + 2,
        )).T.flatten()

        index = np.hstack((bot_circle, top_circle, bl_walls, tr_walls))
        index = np.array(index, np.uint32)

        # colors
        color = np.array([[1, 0, 1], [0, 1, 1]])
        color = np.vstack((color, (np.tile(np.arange(0, nb_circle_points * 2), (3, 1)) % 2).T))
        color = np.array(color, 'f')
        
        attributes = dict(position=position, color=color)
        
        super().__init__(shader, attributes=attributes, index=index)


    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        super().draw(primitives=primitives, global_color=(0, 0, 0), **uniforms)


# ------------  Exercise 1 and 2: Scene object classes ------------------------
class Pyramid(Mesh):
    """ Class for drawing a pyramid object """

    def __init__(self, shader):
        self.shader = shader

        position = np.array(((-0.5, 0, -0.5), (0.5, 0, -0.5), (0.5, 0, 0.5), (-0.5, 0, 0.5), (0, 1, 0)), 'f')
        color = np.array(((1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 1, 1)), 'f')
        index = np.array((0, 2, 3, 0, 1, 2, 0, 4, 1, 2, 1, 4, 3, 2, 4, 0, 3, 4), np.uint32)
        
        attributes = dict(position=position, color=color)
        
        super().__init__(shader, attributes=attributes, index=index)


    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        super().draw(primitives=primitives, global_color=(0, 0, 0), **uniforms)


class Triangle(Mesh):
    """Hello triangle object"""
    def __init__(self, shader):
        position = np.array(((0, .5, 0), (-.5, -.5, 0), (.5, -.5, 0)), 'f')
        color = np.array(((1, 0, 0), (0, 1, 0), (0, 0, 1)), 'f')
        self.color = (1, 1, 0)
        attributes = dict(position=position, color=color)
        super().__init__(shader, attributes=attributes)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        super().draw(primitives=primitives, global_color=self.color, **uniforms)

    def key_handler(self, key):
        if key == glfw.KEY_C:
            self.color = (0, 0, 0)

# ------------  Viewer class & window management ------------------------------
class Viewer:
    """ GLFW viewer window, with classic initialization & graphics loop """
    def __init__(self, width=640, height=480):

        # version hints: create GL window with >= OpenGL 3.3 and core profile
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)
        self.win = glfw.create_window(width, height, 'Viewer', None, None)

        # make win's OpenGL context current; no OpenGL calls can happen before
        glfw.make_context_current(self.win)

        # initialize trackball
        self.trackball = Trackball()
        self.mouse = (0, 0)

        # register event handlers
        glfw.set_key_callback(self.win, self.on_key)
        glfw.set_cursor_pos_callback(self.win, self.on_mouse_move)
        glfw.set_scroll_callback(self.win, self.on_scroll)

        # useful message to check OpenGL renderer characteristics
        print('OpenGL', GL.glGetString(GL.GL_VERSION).decode() + ', GLSL',
              GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode() +
              ', Renderer', GL.glGetString(GL.GL_RENDERER).decode())

        # initialize GL by setting viewport and default render characteristics
        GL.glClearColor(0.1, 0.1, 0.1, 0.1)
        GL.glEnable(GL.GL_CULL_FACE)   # enable backface culling (Exercise 1)
        GL.glEnable(GL.GL_DEPTH_TEST)  # enable depth test (Exercise 1)

        # initially empty list of object to draw
        self.drawables = []

    def run(self):
        """ Main render loop for this OpenGL window """
        while not glfw.window_should_close(self.win):
            # clear draw buffer, but also need to clear Z-buffer! (Exercise 1)
            # GL.glClear(GL.GL_COLOR_BUFFER_BIT)  # comment this, uncomment next
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            win_size = glfw.get_window_size(self.win)
            view = self.trackball.view_matrix()
            projection = self.trackball.projection_matrix(win_size)

            # draw our scene objects
            for drawable in self.drawables:
                drawable.draw(view=view, projection=projection,
                              model=identity())

            # flush render commands, and swap draw buffers
            glfw.swap_buffers(self.win)

            # Poll for and process events
            glfw.poll_events()

    def add(self, *drawables):
        """ add objects to draw in this window """
        self.drawables.extend(drawables)

    def on_key(self, _win, key, _scancode, action, _mods):
        """ 'Q' or 'Escape' quits """
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE or key == glfw.KEY_Q:
                glfw.set_window_should_close(self.win, True)

            for drawable in self.drawables:
                if hasattr(drawable, 'key_handler'):
                    drawable.key_handler(key)

    def on_mouse_move(self, win, xpos, ypos):
        """ Rotate on left-click & drag, pan on right-click & drag """
        old = self.mouse
        self.mouse = (xpos, glfw.get_window_size(win)[1] - ypos)
        if glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_LEFT):
            self.trackball.drag(old, self.mouse, glfw.get_window_size(win))
        if glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_RIGHT):
            self.trackball.pan(old, self.mouse)

    def on_scroll(self, win, _deltax, deltay):
        """ Scroll controls the camera distance to trackball center """
        self.trackball.zoom(deltay, glfw.get_window_size(win)[1])


# -------------- main program and scene setup --------------------------------
def main():
    """ create window, add shaders & scene objects, then run rendering loop """
    viewer = Viewer()
    color_shader = Shader("color.vert", "color.frag")

    # place instances of our basic objects
    #viewer.add(*load('suzanne.obj', color_shader))
    viewer.add(Cylinder(color_shader, 10))

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                  # main function keeps variables locally scoped
