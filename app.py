import cv2
import numpy as np
import os
import face_recognition
from tkinter import *
from tkinter import messageBox
from res import *
import threading

# consts
trainingDir = 'known_file'
testingDir = 'imgs'
tolerance = 0.6
frameThickness = 3
model = 'cnn'

#lists
knownNames = []
knownFaces = []

# global booleans
run = True

def updateResources():
    print('[RELOAD] Loading or Reloading Known Faces...')
    # reset the names
    knownNames = []
    knownFaces = []

    # iterate through all the names
    for name in os.listdir(trainingDir):
        # iterate throught the images in the directory with the name before
        for image in os.listdir(f'{trainingDir}/{name}'):
            image = face_recognition.load_image_file(f'{trainingDir}/{name}/{image}')
            encoding = face_recognition.face_encodings(image)[0]
            knownFaces.append(encoding)
            knownNames.append(image)

def faceRecognise(img):
    # load the image
    image = face_recognition.load_image(f'{testingDir}/{img}')
    # find the locations of the faces
    locations = face_recognition.face_locations(image, model = model)
    # encode the image to compare it later
    encodings = face_recognition.face_encodings(image, locations)
    
    # loop to find similar encodings
    for faceEncoding, faceLocation in zip(encodings, locations):
        # compare the faces
        results = face_recognition.compare_faces(knownFaces, faceEncoding, tolerance)
        if True in results:
            match = knownNames[results.index(True)]
            return match
    
    return None

def userAlert(msg, action):
    userAlertWin = Tk()

    userAlertWin.mainloop()

def faceCheckLoop():
    cam = cv2.videoCapture()

    while True:
        ret, frame = cam.read()

        if not ret:
            raise IOError("Error getting camera frame...")
            raise IOError('"Mission failed... well get them next time..."')
            break
        
        # to exit the program
        key = cv2.waitKey(1)
        # press f to exit application
        if key == ord('f'):
            print('[EXIT] Exiting Application...')
            break
        
        cv2.imwrite(os.path.join('img.jpg'), frame)
        face = faceRecognise('img.jpg')
        if not face == None:
            userAlert(f'{face} is trying to enter your home')
        if os.path.exist('img.png'):
            os.remove('img.png')
        else:
            raise IOError('The file was not saved properly...')
            break

    cam.release()

def tkWindow():
    #make the window
    root = Tk()

    #make the tkinter objects
    #make the gradient frame while pulling from res.py
    mainframe = gradientFrame(
        root
    )
    #make a label cause I probably don't have time to make 

    #commit the tkinter objects
    mainframe.pack(fill = 'both', expand = True)
    root.protocol('WM_DELETE_WINDOW', onWindowClose)
    root.mainloop()

def onWindowClose():
    root.destroy()
    run = False

def loop():
    faceRecogniseThread = threading.Thread(target = faceCheckLoop)
    tkWindowThread = threading.Thread(target = tkWindow)

    faceRecogniseThread.start()
    tkWindowThread.start()

updateResources()
loop()