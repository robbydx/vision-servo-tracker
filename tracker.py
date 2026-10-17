import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
print("Webcam opened successfully.")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    cv2.imshow('Tracker test', frame)

    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()