import cv2

def capturar_frame():
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()
    cap.release()

    if ret:
        return frame
    return None