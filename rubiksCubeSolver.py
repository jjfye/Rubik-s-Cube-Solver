import cv2
import numpy as np
import kociemba as Cube
import colorama
from rotations import rotate, revrotate

GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
RED = colorama.Fore.RED
MAGENTA=colorama.Fore.MAGENTA
colorama.init()

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


font = cv2.FONT_HERSHEY_SIMPLEX


# DEFINING EACH FACE WITH LABELS
"""
label each cube face with letters for each corresponding faces - up down, left, right, front, back.
"""
textPoints=  {
            "up":[["U",242, 202],["W",(0,0,0),260,208]],
            "right":[["R",380, 354],["R",(0,0,255),398,360]],
            "front":[["F",242, 354],["G",(0,255,0),260,360]],
            "down":[["D",242, 508],["Y",(0,255,255),260,514]],
            "left":[["L",104,354],["O",(0,165,255),122,360]],
            "back":[["B",518, 354],["B",(255,0,0),536,360]],
        }

checkState=[]
solution=[]
solved=False

cap=cv2.VideoCapture(0)
cv2.namedWindow("Rubik's Cube Scanner")

# SOLVE FUNCTION
"""
takes in state dictionary as input (current state of the cube - colours as strings).
converts the representation into string "raw" using the previously defined dictionary "signConv"
to map colours to single character symbols.

Once "raw" finishes its loop and is created, "Cube.solve(raw)" will perform a calculation
using the Kociemba imported libary and will print and return the solution as a string.
"""
def solve(state):
    raw = "".join(signConv[j] for face in state.values() for j in face)
    solution = Cube.solve(raw)
    print("answer:", solution)
    return solution


