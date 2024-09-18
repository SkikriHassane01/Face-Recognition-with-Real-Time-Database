import cv2
import face_recognition
import pickle 
import os

# Importing the students images
StudentFolderPath = './images'
PathList = os.listdir(StudentFolderPath)
StudentImagesList = []
StudentIds = []
for i,path in enumerate(PathList, start=0):
    StudentImagesList.append(cv2.imread(os.path.join(StudentFolderPath,path)))
    # StudentImagesList[i] = cv2.resize(StudentImagesList[i], (488, 544 ))
    StudentIds.append(os.path.splitext(path)[0])


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print("=========Start Encoding===============")
EncodeListKnown = findEncodings(StudentImagesList)
encodeListKnownWithIds = [EncodeListKnown, StudentIds]
print("=========Encoding Complete===============")

file = open('EncodeFile.p','wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("=========file saved===============")