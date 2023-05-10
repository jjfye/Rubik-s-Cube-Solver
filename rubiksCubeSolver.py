import cv2
import numpy as np
import kociemba as Cube
import colorama
from rotations import rotate, revrotate

print(f"Use the Rubik's Cube Scanner window to see which faces are required to scan.")

#INITIALIZES CUBE FACES WITH WHITE AS DEFAULT VALUE
faces = ["up", "right", "front", "down", "left", "back"]
state = {face: ["white"] * 9 for face in faces}


signConv={
            "green"  : "F",
            "white"  : "U",
            "blue"   : "B",
            "red"    : "R",
            "orange" : "L",
            "yellow" : "D"
          }

#Create dictionary of colours, map each colour to their RGB number
colour = {
        "red"    : (0,0,255),
        "orange" : (16,136,255),
        "blue"   : (255,0,0),
        "green"  : (0,255,0),
        "white"  : (255,255,255),
        "yellow" : (0,255,255)
        }

#Generate positions with coordinates for different sections of cube
stickers = {
    "main": [[x, y] for y in range(120, 321, 100) for x in range(200, 401, 100)],
    "current": [[x, y] for y in range(20, 89, 34) for x in range(20, 89, 34)],
    "currentCube": [[x, y] for y in range(130, 199, 34) for x in range(20, 89, 34)],
    "left": [[x, y] for y in range(280, 369, 44) for x in range(50, 139, 44)],
    "front": [[x, y] for y in range(280, 369, 44) for x in range(188, 277, 44)],
    "right": [[x, y] for y in range(280, 369, 44) for x in range(326, 415, 44)],
    "up": [[x, y] for y in range(128, 217, 44) for x in range(188, 277, 44)],
    "down": [[x, y] for y in range(434, 523, 44) for x in range(188, 277, 44)],
    "back": [[x, y] for y in range(280, 369, 44) for x in range(464, 553, 44)],
}


