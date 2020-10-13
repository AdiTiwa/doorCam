import cv2
import numpy as np
import os
import face_recognition

# consts
trainingDir = 'known_file'
testingDir = 'imgs'
tolerance = 0.6
frameThickness = 3
model = 'cnn'

#lists
knownNames = []
knownFaces = []

def updateResources():
    print('[RELOAD] Loading or Reloading Known Faces...')
    knownNames = []
    knownFaces = []
    for name in os.listdir(trainingDir):
        for image in os.listdir(f'{trainingDir}/{name}'):
            image = face_recognition.load_image_file(f'{trainingDir}/{name}/{image}')
            encoding = face_recognition.face_ecodings(image)[0]
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

def notify(msg):
    pass

def loop():
    # set up openCV
    # make camera object
    cam = cv2.VideoCapture()

    while True:
        ret, frame = cam.read()

        if not ret:
            raise IOError("Error getting camera frame...")
            raise IOError('"Mission failed... well get them"')
            