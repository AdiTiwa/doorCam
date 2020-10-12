import cv2
import face_recognition
import os

# consts
knownFacesDir = 'known_file'
unknownFacesDir = 'imgs'
tolerance = 0.6
model = 'cnn'


def updateResources():
    # lists
    known_faces = []
    known_names = []

    # update resources
    for name in os.listdir(knownFacesDir):
        for filename in os.listdir(f'{knownFacesDir}/{name}'):
            image = face_recognition.load_image_file(f'{knownFacesDir}/{name}/{filename}')
            encoding = face_recognition.face_encodings(image)
            known_faces.append(encoding)
            known_names.append(name)


def loop():
    # set up cv2
    cam = cv2.VideoCapture()

    while True:
        ret, frame = cam.read()

        if not ret:
            print('Failed to get frame...')
            break

    cam.release()


updateResources()
loop()
