import cv2
import asyncio

async def show_rtsp_stream(rtsp_url: str):
    """
    Hiển thị video từ RTSP URL bằng OpenCV.
    - Bấm phím 'q' để thoát.
    """
    print(f"🎥 Kết nối tới RTSP: {rtsp_url}")
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("❌ Không mở được luồng RTSP.")
        return

    print("✅ Bắt đầu phát video (nhấn 'q' để thoát).")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Mất kết nối hoặc không nhận được frame.")
            await asyncio.sleep(1)
            continue

        frame = cv2.resize(frame, (640, 480))
        cv2.imshow("RTSP Camera Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🛑 Dừng phát video.")
            break

    cap.release()
    cv2.destroyAllWindows()
