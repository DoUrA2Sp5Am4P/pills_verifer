from qreader import QReader
import cv2
import time
start = time.time()
# Create a QReader instance
qreader = QReader()
# Open the default camera
cam = cv2.VideoCapture(0)
while True:
    ret, frame = cam.read()
    cv2.imwrite('./temp_python_files/captured_frame.png', frame)
    # Write the frame to the output file
    # Get the image that contains the QR code
    image = cv2.cvtColor(cv2.imread("./temp_python_files/captured_frame.png"), cv2.COLOR_BGR2RGB)
    # Use the detect_and_decode function to get the decoded QR data
    decoded_text = qreader.detect_and_decode(image=image)
    if decoded_text[0]!="":
        break

