import asyncio
from camera import show_rtsp_stream

RTSP_URL = "rtsp://admin:Vanvu2003@192.168.1.15:554/cam/realmonitor?channel=1&subtype=0"

async def main():
    await show_rtsp_stream(RTSP_URL)

if __name__ == "__main__":
    asyncio.run(main())
