import cv2
import face_recognition
import pickle
import os
from logger import logger
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

# Importing the students images
StudentFolderPath = "./images"
PathList = os.listdir(StudentFolderPath)
StudentImagesList = []
StudentIds = []

# Loop through each image in the folder, resize it, and upload it
for path in PathList:
    # Read the image
    imagePath = os.path.join(StudentFolderPath, path)
    img = cv2.imread(imagePath)
    
    if img is not None:
        resized_img = cv2.resize(img, (216, 216))
        
        # Save the resized image back to the local folder
        cv2.imwrite(imagePath,resized_img)
        
        # Append resized image and student ID
        StudentImagesList.append(resized_img)
        StudentIds.append(os.path.splitext(path)[0])
        
        fileName = f'images/{os.path.basename(imagePath)}'
        bucket = storage.bucket()
        blob = bucket.blob(fileName)
        try:
            blob.upload_from_filename(fileName)
            print(f"Uploaded: {fileName}")
        except Exception as e:
            print(f"Failed to upload {fileName}: {e}")
    else:
        print(f"Failed to read image: {path}")


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


logger.info("=========Start Encoding===============")
EncodeListKnown = findEncodings(StudentImagesList)
encodeListKnownWithIds = [EncodeListKnown, StudentIds]
logger.info("=========Encoding Complete===============")

file = open("EncodeFile.p", "wb")
pickle.dump(encodeListKnownWithIds, file)
file.close()
logger.info("=========file saved===============")
