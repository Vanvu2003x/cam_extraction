import serial
import time

# Kết nối tới ESP32
ser = serial.Serial('COM12', 9600, timeout=1)
time.sleep(2)

def fire_alert(fire_detected):
    print(f"Fire status: {fire_detected}")
    if fire_detected:
        ser.write(b'1')
    else:
        ser.write(b'0')
