import cv2
import asyncio
import os
from ultralytics import YOLO


async def show_rtsp_stream(rtsp_url: str, model_path: str | None = None):
    """
    Hiển thị video từ RTSP URL với nhận diện đám cháy bằng YOLO.
    - Bấm phím 'q' để thoát.
    """
    print(f"🎥 Kết nối tới RTSP: {rtsp_url}")
    
    # Tải mô hình nhận diện đám cháy
    if model_path is None:
        model_path = os.path.join("src", "best.pt")

    if not os.path.exists(model_path):
        print(f"❌ Không tìm thấy file mô hình: {model_path}")
        return

    print(f"🔥 Đang tải mô hình nhận diện đám cháy: {model_path}")
    model = YOLO(model_path)
    print("✅ Mô hình đã được tải thành công!")
    
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("❌ Không mở được luồng RTSP.")
        return

    print("✅ Bắt đầu phát video với nhận diện đám cháy (nhấn 'q' để thoát).")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Mất kết nối hoặc không nhận được frame.")
            await asyncio.sleep(1)
            continue

        # Chạy inference với mô hình YOLO
        results = model(frame, conf=0.25, verbose=False)
        
        # Vẽ kết quả lên frame
        annotated_frame = results[0].plot()
        
        # Hiển thị số lượng đám cháy phát hiện được
        detections = results[0].boxes
        if len(detections) > 0:
            fire_count = len(detections)
            cv2.putText(annotated_frame, f"Detected {fire_count} fire!", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            print(f"WARNING: Detected {fire_count} fire!")
        
        # Resize frame để hiển thị
        annotated_frame = cv2.resize(annotated_frame, (1280, 720))
        cv2.imshow("RTSP Camera - Fire Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🛑 Stopping video.")
            break

    cap.release()
    cv2.destroyAllWindows()
