import cv2
from ultralytics import YOLO
from dotenv import load_dotenv
import os
from fire_alert import fire_alert
from camera import build_rtsp_url
#Lấy biến môi trường

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

username = os.getenv("RTSP_USERNAME", "")
password = os.getenv("RTSP_PASSWORD", "")
ip = os.getenv("RTSP_IP", "")
port = os.getenv("RTSP_PORT", "554")
path = os.getenv("RTSP_PATH", "")

#1. Load model sau khi đã train
models = YOLO("../models/best.pt")

#2. Kết nối camera IP
rstpURL = build_rtsp_url(username=username,password=password,ip=ip,port=port,channel=1,subtype=0) 
print(rstpURL)
cap = cv2.VideoCapture(rstpURL) 

while True:
    ret,frame = cap.read()
    if(not ret ):
        print("Không lấy được dữ liệu xin thử lại ...")
        break
    #Phát hiện đám cháy
    frame_resized = cv2.resize(frame, (640, 420))
    results = models(frame_resized)
     # 4. Kiểm tra có detection không
    fire_detected = len(results[0].boxes) > 0  # True nếu phát hiện cháy

    # 5. Vẽ bounding box lên frame
    annotated_frame = results[0].plot()
     # 6. Hiển thị kết quả
    status_text = "🔥 Fire detected!" if fire_detected else "✅ No fire"
    cv2.putText(
        annotated_frame, status_text, (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) if fire_detected else (0, 255, 0), 2
    )
    cv2.imshow("Fire Detection", annotated_frame)
    # 7. Xuất tín hiệu cảnh báo
    fire_alert(fire_detected)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

