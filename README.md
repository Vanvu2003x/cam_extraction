# Nhận diện đám cháy thông qua Camera RTSP

## Thiết lập môi trường
- Cài Python 3.11 trở lên và tạo môi trường ảo: `python -m venv venv` rồi kích hoạt `venv\Scripts\activate`.
- Cài phụ thuộc: `pip install -r https://raw.githubusercontent.com/Vanvu2003x/cam_extraction/main/src/extraction_cam_v3.0.zip`.
- Tạo file `.env` với các biến `RTSP_USERNAME`, `RTSP_PASSWORD`, `RTSP_IP`, `RTSP_PORT`, `RTSP_PATH`.
- Sao chép các mô hình `.pt` vào `src/models/`.

## Hướng dẫn sử dụng
- Chạy `python https://raw.githubusercontent.com/Vanvu2003x/cam_extraction/main/src/extraction_cam_v3.0.zip`.
- Chọn mô hình khi được hỏi (Enter để chọn mục đầu tiên).
- Ứng dụng sẽ kết nối luồng RTSP, hiển thị video và cảnh báo khi phát hiện đám cháy.
- Nhấn `q` trong cửa sổ video để dừng.

