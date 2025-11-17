# 📘 ESP32 Fire Camera Client – Hướng Dẫn Chạy & Cấu Hình

Dự án này dùng ESP32 kết hợp Camera IP để gửi ảnh lên server AI và nhận cảnh báo cháy. Tài liệu này giúp bạn chạy dự án và **đổi IP Laptop / Camera / Server** dễ dàng.

---

## 🚀 1. Yêu cầu phần cứng

* ESP32 (DevKit V1 hoặc tương đương)
* Camera IP hỗ trợ snapshot
* Laptop chạy FastAPI Server
* LED điều khiển bằng GPIO 26
* Wi-Fi chung mạng

---

## 📡 2. Cấu hình mạng (IP Laptop để ESP32 gửi ảnh)

### 🔍 Xem IP của Laptop (Windows)

Mở CMD:

```
ipconfig
```

Tìm dòng:

```
IPv4 Address : 192.168.1.xx
```

IP này dùng để ESP32 gửi ảnh về.

### 📌 Đặt IP tĩnh cho laptop (khuyến nghị)

Giúp ESP32 không bị sai IP mỗi lần bật máy.

Vào:

```
Control Panel → Network and Internet → Network and Sharing Center
→ Change adapter settings → Wi-Fi → Properties
→ Internet Protocol Version 4 (TCP/IPv4)
```

Chọn:

```
Use the following IP address
```

Ví dụ:

```
IP address: 192.168.1.13
Subnet mask: 255.255.255.0
Default gateway: 192.168.1.1
DNS: 8.8.8.8
```

---

## 🎥 3. Cấu hình Camera IP

Trong file code ESP32, thay:

```
CAM_IP = "192.168.1.108"
```

Nếu camera đổi IP → chỉ sửa tại đây.

Camera snapshot URL tự tạo từ CAM_IP.

---

## 💻 4. Cấu hình Server AI

Thay IP laptop tương ứng:

```
SERVER_UPLOAD = "http://192.168.1.13:8000/upload"
CHECK_ALERT   = "http://192.168.1.13:8000/check_alert"
```

Chỉ đổi phần IP nếu laptop bạn đổi IP.

---

## ⚙️ 5. Chạy server FastAPI

Trên laptop, chạy env sau đó lệnh:

```
py .\SeverAI\src\main.py
```

API cần có:

* `/upload` – nhận ảnh từ ESP32
* `/check_alert` – trả kết quả fire/no-fire

---

## 🔌 6. Nạp code vào ESP32

Dùng Thonny:

1. Mở file `main.py`
2. Save → "MicroPython Device"
3. ESP32 sẽ tự chạy

---

## 🚨 7. LED cảnh báo

* **LED sáng** → Phát hiện cháy
* **LED tắt** → Bình thường

Mặc định dùng GPIO 26:

```
led26 = Pin(26, Pin.OUT)
```

---

## 🛠 8. Chỉnh sửa IP mà không sửa code (tùy chọn)

Bạn có thể tách IP ra file `config.py` để đổi IP mà không sửa file chính.

---

## ✔ 9. Kết luận

File này giúp bạn:

* Đổi IP laptop làm server
* Đổi IP camera
* Chạy server AI
* Flash code ESP32
* Sử dụng LED cảnh báo

Hệ thống sẽ chạy mượt khi laptop, ESP32, và Camera nằm chung mạng LAN.
