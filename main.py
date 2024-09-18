import cv2


cap = cv2.VideoCapture(0)
cap.set(3, 450)
cap.set(4, 415)

while True:
    success, img = cap.read()
    if not success:
        print('Failed to read frame from the camera')
        break
    
    cv2.imshow("Webcame", img)
    cv2.flip(img,1) # horizontally
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()