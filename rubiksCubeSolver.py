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

# DETECTING COLOURS ON CUBE USING HUE, SATURATION & VALUE
"""
By default this function will return white if the saturation and value does not meet the condition.
Defined colour ranges based on its typical values for those standard rubik"s cube colours.
It loops through colourRanges checking whether the input parameters fits into the condition or not and return a colour.
"""
def colourDetect(h, s, v):
    if s < 50 and v > 50:
        return "white"

    colourRanges = [
        (0, 10, "red"),
        (11, 25, "orange"),
        (26, 40, "yellow"),
        (41, 80, "green"),
        (81, 130, "blue"),
    ]

    for low, high, colour in colourRanges:
        if low <= h <= high and s > 50 and v > 50:
            return colour

    return "white"


# DRAW SQUARES AS REFERENCES ON RUBIK'S CUBE SCANNER SCREEN
'''
Goes through each name in "stickers" and draws a square for
each position in stickers dictionary declared at the start.
'''
def drawStickers(frame,stickers,name):
        for x, y in stickers[name]:
            cv2.rectangle(frame, (x,y), (x+30, y+30), (0,0,0), 2)


# DRAW SQUARES AS REFERENCES ON CURRENT CUBE SCREEN
'''
Goes through each name in "stick" and draws a square for
each position in stickers dictionary declared at the start.
'''
def drawCurrentCubeStickers(frame,stickers):
        stick=["front","back","left","right","up","down"]
        for name in stick:
            for x,y in stickers[name]:
                cv2.rectangle(frame, (x,y), (x+40, y+40), (255,255,255), 2)


# ADD TEXT LABELS TO CURRENT CUBE SCREEN STICKERS
'''
Goes through each name in "faceNames" and takes the text symbol "sym", text colour "col" and coordinates
from each position in stickers and shows the text on current cube screen using "cv2.putText"
'''
def textOnCurrentCubeStickers(frame, stickers):
    faceNames = ["front", "back", "left", "right", "up", "down"]
    for name in faceNames:
        sym, x1, y1 = textPoints[name][0][0], textPoints[name][0][1], textPoints[name][0][2]
        cv2.putText(currentCube, sym, (x1, y1), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
                
        sym, col, x1, y1 = textPoints[name][1][0], textPoints[name][1][1], textPoints[name][1][2], textPoints[name][1][3]             
        cv2.putText(currentCube, sym, (x1, y1), font, 0.5, col, 1, cv2.LINE_AA)


# COLOUR STICKERS WITH RESPECTIVE COLOURS FROM INPUT
'''
Iterates through the "sides" dictionary with "side" and "colour".
Passes through position x, y in "stickers" dictionary for its current side.
Then it essentially re-draws the square with its respective colour.
'''
def fillStickers(frame,stickers,sides):    
    for side,colors in sides.items():
        num=0
        for x,y in stickers[side]:
            cv2.rectangle(frame,(x,y),(x+40,y+40),colour[colors[num]],-1)
            num+=1


# SHOW SOLUTION STEP BY STEP ON SOLUTION SCREEN
'''
This takes a list moves as input and visually applies these to the cube's current state.
It updates the currentCube image by rotating the specified sides according to the moves in the input list.
After each operation, the function adds the move's text to the image and appends the updated cube state to the solution list.
It then displays the updated cube state and waits for a keypress before continuing to next step.
Finally, the function removes the text of the applied operation from the image before processing the next move.
'''
def process(operation, state):
    replace = {
                "F":[rotate,"front"],
                "F2":[rotate,"front","front"],
                "F'":[revrotate,"front"],
                "U":[rotate,"up"],
                "U2":[rotate,"up","up"],
                "U'":[revrotate,"up"],
                "L":[rotate,"left"],
                "L2":[rotate,"left","left"],
                "L'":[revrotate,"left"],
                "R":[rotate,"right"],
                "R2":[rotate,"right","right"],
                "R'":[revrotate,"right"],
                "D":[rotate,"down"],
                "D2":[rotate,"down","down"],
                "D'":[revrotate,"down"],
                "B":[rotate,"back"],
                "B2":[rotate,"back","back"],
                "B'":[revrotate,"back"]           
    }    
    a=0
    
    for i in operation:
        for j in range(len(replace[i])-1):
            replace[i][0](state, replace[i][j+1])
            
        cv2.putText(currentCube, i, (700,a+50), font,1,(0,255,0), 1, cv2.LINE_AA)
        
        fillStickers(currentCube,stickers,state)
        solution.append(currentCube)
        
        cv2.imshow("solution",currentCube)
        cv2.waitKey()
        cv2.putText(currentCube, i, (700,50), font,1,(0,0,0), 1, cv2.LINE_AA)  


# MAIN EXECUTION BLOCK
'''
Initialize an empty "currentCube" image with dimensions of 700x800
with a black background.

The while loop will capture frames from the camera and processes them until
the program is ended. Stickers will be filled in "currentCube" depending on
the state.

The program will listen for key presses saves the current state
depending on the key pressed to the state dictionary and adds
the face name to checkState list.

Two frames will be displayed on different windows.
'''
if __name__== "__main__":

    currentCube = np.zeros((700,800,3), np.uint8)

    while True:
        hsv=[]
        currentState=[]
        ret, img = cap.read()
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = np.zeros(frame.shape, dtype=np.uint8)   

        drawStickers(img,stickers,"main")
        drawStickers(img,stickers,"current")
        drawCurrentCubeStickers(currentCube,stickers)
        fillStickers(currentCube,stickers,state)
        textOnCurrentCubeStickers(currentCube,stickers)

        for i in range(9):
            hsv.append(frame[stickers["main"][i][1]+10][stickers["main"][i][0]+10])
        
        a=0
        for x, y in stickers["current"]:
            colourName=colourDetect(hsv[a][0],hsv[a][1],hsv[a][2])
            cv2.rectangle(img,(x,y),(x+30,y+30),colour[colourName],-1)
            a+=1
            currentState.append(colourName)
        
        keyFaceMapping = {
            ord("u"): "up",
            ord("r"): "right",
            ord("l"): "left",
            ord("d"): "down",
            ord("f"): "front",
            ord("b"): "back",
        }

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        elif k in keyFaceMapping:
            face = keyFaceMapping[k]
            state[face] = currentState
            checkState.append(face)
        elif k == ord("\r"):
            if len(set(checkState)) == 6:
                try:
                    solved = solve(state)
                    if solved:
                        operation = solved.split(" ")
                        process(operation, state)
                except:
                    print("Error: There may be issues with lighting or orientation of the cube. Please try again and ensure that each face are scanned correctly.")
            else:
                print("You must scan all faces. Check the currentCube window for more information on the unscanned faces.")
                print("left to scan:", 6 - len(set(checkState)))

        cv2.imshow("currentCube",currentCube)
        cv2.imshow("Rubik's Cube Scanner",img[0:5000,0:500])

    cv2.destroyAllWindows()
