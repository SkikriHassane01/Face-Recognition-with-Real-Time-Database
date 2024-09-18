# Outline
# =================================>
# =================================>
"""
1. Run our webcam 
2. add Graphics interface to the app
3. Encoding Generator
4. Face Recognition
5. Database Setup
6. Add data to db
7. Add images to db
8. Real-time db update
9. limit number of attendance per day
"""
# =================================>
# =================================>


import cv2
import os
import pickle
import face_recognition
from logger import logger
import numpy as np
import cvzone

cap = cv2.VideoCapture(0)
cap.set(3, 531)
cap.set(4, 491)

imgBackground = cv2.imread("./Resources/Background.png")

# add the different mode to the ModeImagesList
ModeFolderPath = "./Resources/Modes"
modePathList = os.listdir(ModeFolderPath)
ModeImagesList = []
for i, path in enumerate(modePathList, start=0):
    ModeImagesList.append(cv2.imread(os.path.join(ModeFolderPath, path)))
    ModeImagesList[i] = cv2.resize(ModeImagesList[i], (488, 544))


# Load the encoding file
logger.info("=========Loading Encode File=============")
file = open("EncodeFile.p", "rb")
encodeListKnownWithIds = pickle.load(file)
file.close()

EncodeListKnown, StudentIds = encodeListKnownWithIds
logger.info(f"Student Ids:{StudentIds}")
logger.info("=========Encode File Loaded=============")

while True:
    success, img = cap.read()

    if not success:
        print("Failed to read frame from the camera")
        break

    img = cv2.resize(
        img, (531, 491), None, fx=0.25, fy=0.25
    )  # Reduce the image size to save computational power
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.flip(img, 1)  # horizontally

    logger.info("==find a list of 128-dimensional face encodings==")
    LocationCurrentFrame = face_recognition.face_locations(img)
    EncodeCurrentFrame = face_recognition.face_encodings(img, LocationCurrentFrame)

    imgBackground[156 : 156 + 491, 52 : 52 + 531] = img
    imgBackground[103 : 103 + 544, 742 : 742 + 488] = ModeImagesList[0]

    for faceEncoded, faceLocation in zip(EncodeCurrentFrame, LocationCurrentFrame):
        Matches = face_recognition.compare_faces(EncodeListKnown, faceEncoded)
        faceDistance = face_recognition.face_distance(EncodeListKnown, faceEncoded)
        # print("matches",Matches)
        # print("Face Distance",faceDistance)

        matchIndex = np.argmin(faceDistance)

        if Matches[matchIndex]:
            logger.info(f"Known Face Detected with id {StudentIds[matchIndex]}")
            y1, x2, y2, x1 = faceLocation  # (top, right, bottom, left)
            bbox = (52 + x1, 156 + y1, x2 - x1, y2 - y1) # bbox: Bounding box [x, y, w, h]
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
            # print(x1,y1,x2,y2)

    cv2.imshow("Face Attendance", imgBackground)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
