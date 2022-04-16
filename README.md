# 3d-graphics-project-2022

This project has for objective to create a Heroic Fantastic Land with OpenGL.

Members: Alexandre Berard, Thibault Groot and Margot Duran.

# How to use

We assume you have installed the OpenGL python suite (PyOpenGL package for python3). No more packages are required.

The only thing you have to do is to launch the following command on project's root:

```
./viewer.py
```

You can only move around with mouse control.

To exit the scene, press ESCAPE.

# Features:

 - Desert with some dunes created by value noise and shading
 - Randomly generated cactuses over the desert
 - Moving dragon. He planes around the castle in the sky and flaps its wings. You can control dragon's rotation circle by pressing the LEFT and RIGHT arrows on the keyboard
 - Light with some warm color
 - Skybox with a sun and gradient from blue to white, the white being at the level of the horizon

![scene image](https://github.com/kepler69c/3d-graphics-project-2022/blob/main/README_splash.png?raw=true "You can hear *grrr* noises from the distance")

# Difficulties, possible extensions:

 - Create sphere to represent some tumble weed with a texture. We failed to create a sphere. But with a working program, it would have been interesting to roll it along the dunes
 - Add some more lights
 - Add a class Skinned to have a skeleton of the dragon. With this addition, we could make the dragon do more different movements (for example: opening and closing its mouth) these could be more fluid and realistic

# Sources:

Castle 3D Model: https://open3dmodel.com/3d-models/medieval-castle-2_7077.html

Dragon 3D Model: https://www.turbosquid.com/3d-models/acnologia-3d-1442853

Cactus 3D Model 1: https://free3d.com/fr/3d-model/-cactus-v1--424886.html

Cactus 3D Model 2: https://www.cgtrader.com/free-3d-models/plant/other/century-cactus
