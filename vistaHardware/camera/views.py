from django.shortcuts import render
import cv2
from django.http import StreamingHttpResponse

camera = cv2.VideoCapture(1)

def create_frames():
    while True:
        success, frame = camera.read() #success is a boolean that gives you info on if the camera successfully captured a frame
        if not success:                #image captured from the camera
            break
        _, buffer = cv2.imencode('.jpg', frame) #JPEG encoded image stored in memeory (will be sent to the React UI)
        frame = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        #yield is preferred over return because it keeps the function alive while return data, unlike basic return

def vid_feed(request):
    return StreamingHttpResponse(create_frames(), content_type = 'multipart/x-mixed-replace; boundary=frame')
        #content_type tells the browser that the feed is a live video stream