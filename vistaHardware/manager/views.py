from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
import serial

#Arduino specifications
SERIAL_PORT = 'COM3' #Change to the serial port of Arduino
BAUD_RATE = 9600 #Speed of data transmission (9600 is standard)

#Establish serial connection

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout = 1)
except serial.SerialException as e:
    arduino = None
    print(f"Arduino connection failed with: {e}")

@api_view(['POST'])
def led_on(request):
    print("LED ON request received")
    if arduino:
        try:
            arduino.write(b'ON\n')
            return JsonResponse({'status': 'LED ON'})
        except Exception as e:
            print(f"Write failed: {e}")
            return JsonResponse({'error': f'Failed to write to Arduino: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Arduino not connected'}, status=500)
        
@api_view(['POST'])
def led_off(request):
    if(arduino):
        arduino.write(b'OFF\n')
        return JsonResponse({'status': 'LED OFF'})
    return JsonResponse({'error': 'Arduino not connected'}, status = 500)
