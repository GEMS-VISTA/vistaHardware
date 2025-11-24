from flask import Flask, request, jsonify
import serial

app = Flask(__name__) # Creates the web app instance

SERIAL_PORT = 'COM3'  # Update if needed
BAUD_RATE = 9600

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to Arduino on {SERIAL_PORT}")
except serial.SerialException as e:
    arduino = None
    print(f"Failed to connect to Arduino: {e}")

@app.route('/led/on', methods=['POST'])
def led_on():
    if arduino:
        try:
            arduino.write(b'ON\n')
            return jsonify({'status': 'LED ON'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Arduino not connected'}), 500

@app.route('/led/off', methods=['POST'])
def led_off():
    if arduino:
        try:
            arduino.write(b'OFF\n')
            return jsonify({'status': 'LED OFF'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Arduino not connected'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)