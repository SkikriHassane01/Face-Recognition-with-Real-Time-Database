# Outline
#=================================>
#=================================>
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
#=================================>
#=================================>


import cv2
import os 
cap = cv2.VideoCapture(0)
cap.set(3, 531)
cap.set(4, 491)

imgBackground = cv2.imread('./Resources/Background.png')

# add the different mode to the ModeImagesList
ModeFolderPath = './Resources/Modes'
modePathList = os.listdir(ModeFolderPath)
ModeImagesList = []
for i,path in enumerate(modePathList, start=0):
    ModeImagesList.append(cv2.imread(os.path.join(ModeFolderPath,path)))
    ModeImagesList[i] = cv2.resize(ModeImagesList[i], (488, 544 ))


while True:
    success, img = cap.read()

    if not success:
        print('Failed to read frame from the camera')
        break

    img = cv2.resize(img, (531, 491))
    cv2.flip(img,1) # horizontally
    imgBackground[156:156 + 491, 52:52 + 531] = img
    imgBackground[103:103 + 544, 742:742 + 488 ] = ModeImagesList[0]

    
    cv2.imshow("Face Attendance", imgBackground)


    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()