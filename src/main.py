import asyncio
import os
from dotenv import load_dotenv
from camera import show_rtsp_stream

# Load biến môi trường từ file .env
load_dotenv()

def build_rtsp_url() -> str:
    """Tạo RTSP URL từ các biến môi trường."""
    username = os.getenv("RTSP_USERNAME", "")
    password = os.getenv("RTSP_PASSWORD", "")
    ip = os.getenv("RTSP_IP", "")
    port = os.getenv("RTSP_PORT", "554")
    path = os.getenv("RTSP_PATH", "")
    
    # Tạo URL theo format: rtsp://username:password@IP:port/path
    rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}{path}"
    return rtsp_url

async def main():
    rtsp_url = build_rtsp_url()
    model_path = os.path.join("src", "best.pt")
    await show_rtsp_stream(rtsp_url, model_path=model_path)

if __name__ == "__main__":
    asyncio.run(main())
