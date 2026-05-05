import os
import cv2
import sys
import keyboard
import numpy as np
import subprocess
import time

feature_params = dict(maxCorners=500, qualityLevel=0.2, minDistance=15, blockSize=9)

#Sets up camera
s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]

source = cv2.VideoCapture(s)

#Sets up window for camera to display to
win_name = 'Camera Preview'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
mode = 0

#Until esc is pressed, displays camera. Switches between normal, canny, and showing key points with 1, 2, 3
while cv2.waitKey(1) != 32: # Space
    has_frame, frame = source.read()
    frame = cv2.flip(frame, 1)
    if not has_frame:
        break
    if mode == 0:
        result = frame
    elif mode == 1:
        result = cv2.Canny(frame, 120, 150)
    elif mode == 2:
        result = frame
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(frame_gray, **feature_params)
        if corners is not None:
            for x, y in np.float32(corners).reshape(-1, 2):
                cv2.circle(result, (int(x), int(y)), 10, (0, 255, 0), 1)
    if keyboard.is_pressed('1'):
        mode = 0
    if keyboard.is_pressed('2'):
        mode = 1
    if keyboard.is_pressed('3'):
        mode = 2
    cv2.imshow(win_name, result)
    
#When esc is pressed, close window and save final frame
source.release()
cv2.destroyWindow(win_name)
#frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

cv2.imwrite("testcpy.png", frame)

#Comparing final frame to template
template = cv2.imread("6rdTry.png", cv2.IMREAD_GRAYSCALE)
pic = cv2.imread("testcpy.png", cv2.IMREAD_GRAYSCALE)

#Creates orbs on the keypoints of both images
orb = cv2.ORB_create(500)
maskT = np.ones(template.shape, dtype=np.uint8)*255
maskT[374:830, 217:668] = 0
#maskP = np.ones(pic.shape, dtype=np.uint8)*255
#picY, picX = pic.shape
#maskP[int(2*picY/5):int(3*picY/5), int(2*picX/5):int(3*picX/5)]
keypointsT, descriptorsT = orb.detectAndCompute(template, maskT)
keypointsP, descriptorsP = orb.detectAndCompute(pic, None)
t_display = cv2.drawKeypoints(template, keypointsT, outImage=np.array([]), color=(255, 0, 0), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
p_display = cv2.drawKeypoints(pic, keypointsP, outImage=np.array([]), color=(255, 0, 0), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

#Uses matcher to match up orbs and remove poor matches
matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
matches = list(matcher.match(descriptorsT, descriptorsP, None))
matches.sort(key=lambda x: x.distance, reverse=False)
numGoodMatches = int(len(matches) * .1)
matches = matches[:numGoodMatches]

im_matches = cv2.drawMatches(template, keypointsT, pic, keypointsP, matches, None)

#Computing homography(How to change picture image)
pointsT = np.zeros((len(matches), 2), dtype=np.float32)
pointsP = np.zeros((len(matches), 2), dtype=np.float32)
for i, match in enumerate(matches):
    pointsT[i, :] = keypointsT[match.queryIdx].pt
    pointsP[i, :] = keypointsP[match.trainIdx].pt
h, mask = cv2.findHomography(pointsP, pointsT, cv2.RANSAC)

#Manipulating image
height, width = template.shape
template_reg = cv2.warpPerspective(pic, h, (width, height))
cv2.imwrite("CorrectedImage.png", template_reg)
guh = cv2.imread("CorrectedImage.png")

#Detect X's and O's
xSpot = cv2.imread('X.png', cv2.IMREAD_GRAYSCALE)
oSpot = cv2.imread('O.png', cv2.IMREAD_GRAYSCALE)
w2, h2 = xSpot.shape[:2]
w3, h3 = oSpot.shape[:2]
resX = cv2.matchTemplate(template_reg, xSpot, cv2.TM_CCOEFF_NORMED)
resO = cv2.matchTemplate(template_reg, oSpot, cv2.TM_CCOEFF_NORMED)
threshold = .6
locX = np.where(resX >= threshold)
locO = np.where(resO >= threshold)
#Set up arrays for getting X's and O's
pVs = 9
coords = 2
locX2 = [[-1*w2 for x in range(coords)] for y in range(pVs)]
locO2 = [[-1*w2 for x in range(coords)] for y in range(pVs)]
numX = 0
numO = 0
matchCoord = True

for pt in zip(*locX[::-1]):
    matchCoord = True
    cv2.rectangle(template_reg, pt, (pt[0] + w2, pt[1] + h2), (0, 0, 255), 2)
    for e in range(9):
        if(pt[0] > locX2[e][0]-.5*w2 and pt[0] < locX2[e][0]+.5*w2 and pt[1] > locX2[e][1]-.5*w2 and pt[1] < locX2[e][1]+.5*w2):
            matchCoord = False
            #print("Too close to {0}, {1}".format(locX2[e][0], locX2[e][1]))
    if matchCoord == True:
        #print("Case found")
        #print(pt[0])
        #print(pt[1])
        locX2[numX][0] = pt[0]
        locX2[numX][1] = pt[1]
        numX = numX + 1
#print("X's done, starting O's")
for pt in zip(*locO[::-1]):
    matchCoord = True
    cv2.rectangle(template_reg, pt, (pt[0] + w3, pt[1] + h3), (0, 0, 255), 2)
    for e in range(9):
        if(pt[0] > locO2[e][0]-.5*w3 and pt[0] < locO2[e][0]+.5*w3 and pt[1] > locO2[e][1]-.5*w3 and pt[1] < locO2[e][1]+.5*w3):
            matchCoord = False
    if matchCoord == True:
        #print("Case found")
        #print(pt[0])
        #print(pt[1])
        locO2[numO][0] = pt[0]
        locO2[numO][1] = pt[1]
        numO = numO + 1
    
#print("X's found: {0} and O's found: {1}".format(numX, numO))

board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
column = 0
row = 0
for t in range(numX):
    if(locX2[t][0] > 200 and locX2[t][0] < 300):
        #In 1st column
        column = 1
    if(locX2[t][0] > 350 and locX2[t][0] < 450):
        #In 2nd column
        column = 2
    if(locX2[t][0] > 500 and locX2[t][0] < 600):
        #In 3rd column
        column = 3
    if(locX2[t][1] > 350 and locX2[t][1] < 450):
        row = 1
    if(locX2[t][1] > 500 and locX2[t][1] < 600):
        row = 2
    if(locX2[t][1] > 650 and locX2[t][1] < 750):
        row = 3
    board[column-1 + 3*(row-1)] = 1
for t in range(numO):
    if(locO2[t][0] > 200 and locO2[t][0] < 300):
        #In 1st column
        column = 1
    if(locO2[t][0] > 350 and locO2[t][0] < 450):
        #In 2nd column
        column = 2
    if(locO2[t][0] > 500 and locO2[t][0] < 600):
        #In 3rd column
        column = 3
    if(locO2[t][1] > 350 and locO2[t][1] < 450):
        row = 1
    if(locO2[t][1] > 500 and locO2[t][1] < 600):
        row = 2
    if(locO2[t][1] > 650 and locO2[t][1] < 750):
        row = 3
    board[column-1 + 3*(row-1)] = 2


#Shows template and comparison image
cv2.namedWindow("Comparison", cv2.WINDOW_NORMAL)
mode = 1
while cv2.waitKey(1) != 32:
    if mode == 1:
        result = template
    elif mode == 2:
        result = pic
    elif mode == 3:
        result = t_display
    elif mode == 4:
        result = p_display
    elif mode == 5:
        result = guh
    elif mode == 6:
        result = im_matches
    elif mode == 7:
        result = template_reg
    if keyboard.is_pressed('1'):
        mode = 1
    if keyboard.is_pressed('2'):
        mode = 2
    if keyboard.is_pressed('3'):
        mode = 3
    if keyboard.is_pressed('4'):
        mode = 4
    if keyboard.is_pressed('5'):
        mode = 5
    if keyboard.is_pressed('6'):
        mode = 6
    if keyboard.is_pressed('7'):
        mode = 7
    cv2.imshow("Comparison", result)
cv2.destroyWindow("Comparison")

for i in range(3):
    print(board[i], end=" ")
print()
for i in range(3, 6):
    print(board[i], end=" ")
print()
for i in range(6, 9):
    print(board[i], end=" ")
print()

f = open("hi2.txt", "w")
for i in range(9):
    f.write(str(board[i])+' ')
f.close()

send = input("Confirm board is accurate and start game with z or end program with c\n")
if(send == "c"):
    sys.exit()


subprocess.run(["python", "TicTacToe.py", "hi2.txt"])
