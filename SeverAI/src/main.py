from fastapi import FastAPI, Request
import uvicorn
import numpy as np
import cv2
from ai import detect_fire
app = FastAPI()
fire_alert = False

@app.post("/upload")
async def upload(request: Request):
    global fire_alert
    contents = await request.body()
    if not contents:
        return {"status": "failed", "msg": "No data received"}

    # Decode ảnh
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return {"status": "failed", "msg": "Cannot decode image"}
    fire_detected = detect_fire(img)
    fire_alert = fire_detected
    return {"status": "ok"}

@app.get("/check_alert")
async def check_alert():
    global fire_alert
    if fire_alert:
        return {"alert": "fire"}
    return {"alert": "none"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
