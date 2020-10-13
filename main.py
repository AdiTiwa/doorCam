import cv2
import face_recognition
import os
from tkinter import *
from res import *

# consts
knownFacesDir = 'known_file'
unknownFacesDir = 'imgs'
tolerance = 0.6
frame_thickness = 3
model = 'cnn'


# lists
known_faces = []
known_names = []

# update resources
for name in os.listdir(knownFacesDir):
    for filename in os.listdir(f'{knownFacesDir}/{name}'):
        image = face_recognition.load_image_file(f'{knownFacesDir}/{name}/{filename}')
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(name)

print("processing unknown faces")
for filename in os.listdir(unknownFacesDir):
    print(filename)
    image = face_recognition.load_image(f"{unknownFaceDir}/{filename}")
    locations = face_recognition.face_locations(image, model = model)
    encodings = face_recognition.face_encodings(image, locations)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    for face_encoding, face_location in zip(encodings, locations):
        results = face_recognition.compare_faces(known_faces, face_encoding, tolerance)
        match = None
        if True in results:
            match = known_names[results.index(True)]
            print("Match found: {match}")
            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])
            color = [0,255,0]
            cv2.rectangle(image, top_left, bottom_right, color, frame_thickness)
            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2]+22)
            cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
            cv2.putText(image, match, (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), FONT_THICKNESS)
    cv2.imshow(filename, image)
    cv2.waitKey(10000)
    #cv2.destroyWindow(filename)


            
def faceRecognize(img):
    return known_faces[0]

def notify(msg, isInvite = False):
    win = Tk()

    # instantiate the tkinter objects
    tkinterObjects = []
    messageLabel = Label(
        master = win,
        text = msg
    )
    messageLabelObject = [
        messageLabel,
        True,
        0,
        0,
        2
    ]
    tkinterObjects.append(messageLabelObject)
    closeButton = Button(
        master = win
    )

    # commit the tkinter objects
    for tkinterObject in tkinterObjects:
        if tkinterObject[1]:
            tkinterObject[0].grid(row = tkinterObject[2], column = tkinterObject[3], columnspan = tkinterObject[4])
        else:
            tkinterObject[0].pack()

    win.mainloop()

def loop():
    # set up cv2
    cam = cv2.VideoCapture()

    while True:
        ret, frame = cam.read()

        if not ret:
            raise IOError("The camera couldn't get the frame from the camera...")
            break
        
        key = cv2.waitKey(1)
        if key == ord('e'):
            print('[CLOSING] Closing Application...')
            break
        
        cv2.imwrite('img.png', frame)
        faceRecognized = faceRecognize('img.png')
        
        if os.path.exist('img.png'):
            os.remove('img.png')
        else:
            raise IOError('The file was not saved properly...')
            break
    
    cam.release()


