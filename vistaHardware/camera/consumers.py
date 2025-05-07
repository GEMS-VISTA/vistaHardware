"""
Consumers.py sets up the WebSocket consumer which will serve as the main camera streamer
"""

import cv2
import asyncio
import base64
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoFeedConsumer(AsyncWebsocketConsumer):
#"async" allows the program to run a long task while being responsive to other events instead of waiting for task to finish (multithreading)
#await is used with async functions to pause execution until awaited task is completed
    async def connect(self):
        print("WebSocket connect() called") #Debugging
        await self.accept()
        self.camera = cv2.VideoCapture(0)
        self.running = True
        asyncio.create_task(self.send_frames())

    async def disconnect(self, close_code):
        self.running = False
        self.camera.release()

    async def send_frames(self):
        while self.running:
            success, frame = self.camera.read() #success is a boolean that gives you info on if the camera successfully captured a frame
            if not success: #frame image captured from the camera
                continue  

            _, buffer = cv2.imencode('.jpg', frame) #JPEG encoded image stored in memeory (will be sent to the React UI)
            frame_data = base64.b64encode(buffer).decode('utf-8')

            await self.send(text_data=frame_data)
            await asyncio.sleep(0.05) #Send about 20 FPS (FPS = 1/ sleep time; 1/0.05 = 20 frames per second)