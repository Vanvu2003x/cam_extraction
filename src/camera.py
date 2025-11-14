import cv2
from ultralytics import YOLO
from dotenv import load_dotenv
import os
import threading
import queue
from fire_alert import fire_alert
from connect_camera import build_rtsp_url

# 1️⃣ ĐỌC CẤU HÌNH TỪ FILE .env
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

username = os.getenv("RTSP_USERNAME", "")
password = os.getenv("RTSP_PASSWORD", "")
ip = os.getenv("RTSP_IP", "")
port = os.getenv("RTSP_PORT", "554")
path = os.getenv("RTSP_PATH", "")

# 2️⃣ TẢI MÔ HÌNH YOLO
model = YOLO("../models/best.pt")  

# 3️⃣ KẾT NỐI CAMERA
rtsp_url = build_rtsp_url(
    username=username,
    password=password,
    ip=ip,
    port=port,
    channel=1,
    subtype=0
)
print("🔗 Kết nối tới camera:", rtsp_url)

# Mở camera RTSP
cap = cv2.VideoCapture(rtsp_url)

# 4️⃣ TẠO HÀNG ĐỢI
# frame_queue: Lưu frame từ camera 
# result_queue: Lưu kết quả inference (frame + results)
frame_queue = queue.Queue(maxsize=5)
result_queue = queue.Queue(maxsize=5)

def capture_frames():
    """
    Luồng này chỉ đọc frame từ camera và đẩy vào frame_queue.
    Nếu queue đầy, bỏ frame cũ nhất để tránh delay.
    """
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Không lấy được frame từ camera")
            break

        if frame_queue.full():
            try:
                frame_queue.get_nowait()
            except queue.Empty:
                pass

        frame_queue.put(frame)

def ai_inference():
    """
    Luồng này lấy frame từ frame_queue, chạy YOLO, đưa kết quả vào result_queue.
    """
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            frame_resized = cv2.resize(frame, (640, 420))

            results = model(frame_resized) 

            if result_queue.full():
                try:
                    result_queue.get_nowait()
                except queue.Empty:
                    pass

            result_queue.put((frame, results))

# 7️⃣ TẠO VÀ CHẠY THREADS
capture_thread = threading.Thread(target=capture_frames, daemon=True)
capture_thread.start()

ai_thread = threading.Thread(target=ai_inference, daemon=True)
ai_thread.start()

# 8️⃣ LUỒNG CHÍNH: HIỂN THỊ + CẢNH BÁO (CPU)
print("🚀 Bắt đầu phát hiện đám cháy... (nhấn 'q' để thoát)")

while True:
    if not result_queue.empty():
        frame, results = result_queue.get()

        # Vẽ khung bounding box
        annotated_frame = results[0].plot()

        # Ghi chữ trạng thái
        fire_detected = len(results[0].boxes) > 0
        status_text = "🔥 Fire detected!" if fire_detected else "✅ No fire"
        color = (0, 0, 255) if fire_detected else (0, 255, 0)
        cv2.putText(annotated_frame, status_text, (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # Hiển thị
        cv2.imshow("Fire Detection", annotated_frame)

        # Gửi tín hiệu cảnh báo
        fire_alert(fire_detected)

    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 9️⃣ DỌN DẸP
cap.release()
cv2.destroyAllWindows()
print("🛑 Đã dừng chương trình.")
