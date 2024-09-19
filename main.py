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
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://faceattendancewithrealtimedb-default-rtdb.firebaseio.com/",
        "storageBucket": "faceattendancewithrealtimedb.appspot.com",
    },
)
bucket = storage.bucket()
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


modeType = 0
counter = 0 # to download the data one time 
id = -1
imgStudent = []
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

    LocationCurrentFrame = face_recognition.face_locations(img)
    EncodeCurrentFrame = face_recognition.face_encodings(img, LocationCurrentFrame)

    imgBackground[156 : 156 + 491, 52 : 52 + 531] = img
    # print(len(ModeImagesList))
    imgBackground[103 : 103 + 544, 742 : 742 + 488] = ModeImagesList[modeType]

    if LocationCurrentFrame:
        for faceEncoded, faceLocation in zip(EncodeCurrentFrame, LocationCurrentFrame):
            Matches = face_recognition.compare_faces(EncodeListKnown, faceEncoded)
            faceDistance = face_recognition.face_distance(EncodeListKnown, faceEncoded)
            # print("matches",Matches)
            # print("Face Distance",faceDistance)

            matchIndex = np.argmin(faceDistance)

            if Matches[matchIndex]:
                y1, x2, y2, x1 = faceLocation  # (top, right, bottom, left)
                bbox = (52 + x1, 156 + y1, x2 - x1, y2 - y1) # bbox: Bounding box [x, y, w, h]
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = StudentIds[matchIndex]
                
                if counter == 0:
                    cvzone.putTextRect(imgBackground,"Loading",(250,400))
                    cv2.imshow("Face Attendance",imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1
        
        if counter != 0:
            if counter == 1:
                # get the data from our database
                studentInfo = db.reference(f'Students/{id}').get()
                # if studentInfo is None:
                #     print(f"No data found for Student ID: {id}")
                # else:
                #     print(f"Student Info: {studentInfo}")
                
                # get the image from the storage 
                blob = bucket.get_blob(f'images/{id}.png')
                array = np.frombuffer(blob.download_as_string(),np.uint8)
                imgStudent = cv2.imdecode(array,cv2.COLOR_BGR2RGB)
                
                # update the data of attendance 
                
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                if secondsElapsed > 30:
                    
                    ref = db.reference(f'Students/{id}')
                    total_attendance = studentInfo.get('total_attendance',0)
                    last_attendance_time = studentInfo.get('last_attendance_time')
                    total_attendance +=1
                    ref.child('total_attendance').set(total_attendance)
                    ref.child('last_attendance_time').set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    modeType=3
                    counter = 0
                    imgBackground[103 : 103 + 544, 742 : 742 + 488] = ModeImagesList[modeType]
            if modeType !=3:
                if  10<counter<20:
                    modeType = 2
                
                imgBackground[103 : 103 + 544, 742 : 742 + 488] = ModeImagesList[modeType]
                        
                if counter <= 10:
                    name = studentInfo.get('name','None')
                    major = studentInfo.get('major','None')
                    starting_year = studentInfo.get('starting_year',0)
                    year = studentInfo.get('year',0)
                    standing = studentInfo.get('standing','None')
                    
                    cv2.putText(imgBackground,str(total_attendance),(742 + 62,103 + 67),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
                    cv2.putText(imgBackground,str(id),(742 + 250 + 10,103 + 387),cv2.FONT_HERSHEY_SIMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgBackground,str(major),(742 + 250 + 25 ,103 + 395 + 48),cv2.FONT_HERSHEY_SIMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgBackground,str(starting_year),(1084 + 55,103 + 395 + 48 + 20 + 40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(100,100,100),1)
                    cv2.putText(imgBackground,str(year),(948 + 60,103 + 395 + 48 + 20 + 40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(100,100,100),1)
                    cv2.putText(imgBackground,str(standing),(811 + 60 ,103 + 395 + 48 + 20 + 40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(100,100,100),1)
                    
                    (w,h),_ = cv2.getTextSize(name,cv2.FONT_HERSHEY_COMPLEX,1,2)
                    offset = (487 - w) // 2
                    cv2.putText(imgBackground,str(name),(742 + offset,103 + 340),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,50),2)
                    
                    imgStudent = cv2.resize(imgStudent, (249, 230))
                    imgBackground[174:174 + 230, 861:861 + 249] = imgStudent
                    
                counter +=1
                    
                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[103 : 103 + 544, 742 : 742 + 488] = ModeImagesList[modeType]
                    
    else:
        modeType = 0
        counter = 0
    cv2.imshow("Face Attendance", imgBackground)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
# cap.release()
# cv2.destroyAllWindows()
