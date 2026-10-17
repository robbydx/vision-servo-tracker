import cv2
import serial
import time

# Initialize serial communication with Arduino
ser = serial.Serial('COM8', 9600, timeout=1)
time.sleep(2)  # Wait for connection

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# Initialize webcam
cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

SERVO_MIN = 0
SERVO_MAX = 180
FRAME_CENTER_X = 320


def map_value(x, in_min, in_max, out_min, out_max):
    return int(
        (x - in_min) * (out_max - out_min)
        / (in_max - in_min) + out_min
    )


try:
    while True:
        ret, frame = cap.read()

        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray, 1.1, 5
        )

        if len(faces) > 0:
            x, y, w, h = faces[0]

            center_x = x + w // 2
            error_x = center_x - FRAME_CENTER_X

            servo_angle = map_value(
                center_x, 0, 640, SERVO_MAX, SERVO_MIN
            )

            servo_angle = max(
                SERVO_MIN,
                min(SERVO_MAX, servo_angle)
            )

            ser.write(f"{servo_angle}\n".encode())

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.circle(
                frame,
                (center_x, y + h // 2),
                5,
                (0, 0, 255),
                -1
            )

            cv2.putText(
                frame,
                f"Servo: {servo_angle}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

        cv2.imshow("Face Tracker", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    ser.close()
    cv2.destroyAllWindows()