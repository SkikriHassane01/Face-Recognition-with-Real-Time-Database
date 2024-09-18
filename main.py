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

cap = cv2.VideoCapture(0)
cap.set(3, 531)
cap.set(4, 491)

imgBackground = cv2.imread('./Resources/Background.png')

while True:
    success, img = cap.read()

    if not success:
        print('Failed to read frame from the camera')
        break

    img = cv2.resize(img, (531 - 16, 491 - 16)) # the border size is 8px
    
    img = add_border_radius(img, 50)
    imgBackground[156+8:156+8 + 491 - 16, 52+8:52+8 + 531 - 16] = img
    
    cv2.imshow("Face Attendance", imgBackground)

    cv2.flip(img,1) # horizontally
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()