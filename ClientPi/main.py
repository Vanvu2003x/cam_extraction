# ---------------- ESP32 Fire Camera Client Optimized ----------------
import network
import time
import urequests as requests
from machine import Pin
import hashlib
import os
import uasyncio as asyncio

# ---------------- Cấu hình Wi-Fi ----------------
SSID = "Anh Duc"
PASSWORD = "12345678"

# ---------------- Cấu hình Camera ----------------
CAM_IP = "192.168.1.108"
USER = "admin"
PASS = "Vanvu2003"
SNAPSHOT_URL = f"http://{CAM_IP}/onvifsnapshot/media_service/snapshot?channel=1&subtype=0"

# ---------------- Cấu hình Server ----------------
SERVER_UPLOAD = "http://192.168.1.13:8000/upload"
CHECK_ALERT = "http://192.168.1.13:8000/check_alert"

# ---------------- LED Báo động ----------------
led26 = Pin(26, Pin.OUT)
led26.off()

# ---------------- Hàm hỗ trợ MD5 ----------------
def md5_hex(s):
    m = hashlib.md5()
    m.update(s)
    return m.digest().hex()

# ---------------- Tạo header Digest Auth ----------------
def digest_header(url, method="GET", username="", password="", www_authenticate=""):
    auth_dict = {}
    for item in www_authenticate.replace("Digest ", "").split(","):
        k, v = item.strip().split("=", 1)
        auth_dict[k] = v.replace('"', "")
    realm = auth_dict.get("realm")
    nonce = auth_dict.get("nonce")
    qop = auth_dict.get("qop", "auth")
    uri = url.split(f"http://{CAM_IP}")[1]
    nc = "00000001"
    cnonce = "%08x" % int.from_bytes(os.urandom(4), "big")
    ha1 = md5_hex(f"{username}:{realm}:{password}".encode())
    ha2 = md5_hex(f"{method}:{uri}".encode())
    response = md5_hex(f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}".encode())
    header_value = (
        f'Digest username="{username}", realm="{realm}", nonce="{nonce}", uri="{uri}", '
        f'algorithm=MD5, response="{response}", qop={qop}, nc={nc}, cnonce="{cnonce}"'
    )
    return {"Authorization": header_value}

# ---------------- Kết nối Wi-Fi ----------------
def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        print("Đang kết nối Wi-Fi...")
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            time.sleep(0.5)
    print("Wi-Fi đã kết nối:", sta_if.ifconfig())
    time.sleep(1)

# ---------------- Lấy snapshot từ camera (tối ưu) ----------------
last_nonce = None

def get_snapshot():
    global last_nonce
    try:
        if last_nonce:
            headers = digest_header(SNAPSHOT_URL, "GET", USER, PASS, f'nonce="{last_nonce}"')
            r = requests.get(SNAPSHOT_URL, headers=headers, timeout=5)
        else:
            r = requests.get(SNAPSHOT_URL, timeout=5)
            if r.status_code == 401:
                www_auth = r.headers.get("WWW-Authenticate")
                headers = digest_header(SNAPSHOT_URL, "GET", USER, PASS, www_auth)
                last_nonce = headers["Authorization"].split('nonce="')[1].split('"')[0]
                r.close()
                r = requests.get(SNAPSHOT_URL, headers=headers, timeout=5)
        if r.status_code == 200:
            img = r.content
            r.close()
            return img
        r.close()
        return None
    except Exception as e:
        print("Lỗi get_snapshot:", e)
        return None

# ---------------- Gửi ảnh lên server ----------------
async def upload_snapshot(img_data):
    headers_upload = {"Content-Type": "image/jpeg"}
    try:
        for retry in range(3):
            try:
                requests.post(SERVER_UPLOAD, data=img_data, headers=headers_upload, timeout=10)
                print("Ảnh gửi server thành công")
                return True
            except Exception as e:
                print(f"Retry gửi ảnh {retry+1}/3:", e)
                await asyncio.sleep(1)
        return False
    except Exception as e:
        print("Lỗi upload_snapshot:", e)
        return False

# ---------------- Kiểm tra cảnh báo ----------------
async def check_alert():
    try:
        resp = requests.get(CHECK_ALERT, timeout=5)
        if resp.status_code == 200 and "fire" in resp.text.lower():
            led26.on()
            print("Báo cháy! LED 26 ON")
        else:
            led26.off()
        resp.close()
    except Exception as e:
        print("Lỗi check_alert:", e)
        led26.off()

# ---------------- Task chính loop ----------------
async def main_loop():
    INTERVAL = 1  # 1 giây
    while True:
        img = get_snapshot()
        if img:
            asyncio.create_task(upload_snapshot(img))  # gửi async, không block loop
        await check_alert()
        await asyncio.sleep(INTERVAL)

# ---------------- Main ----------------
def main():
    connect_wifi()
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("Đã dừng chương trình bởi người dùng")
        led26.off()
    except Exception as e:
        print("Lỗi tổng:", e)
        led26.off()

if __name__ == "__main__":
    main()
