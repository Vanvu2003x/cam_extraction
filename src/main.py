import asyncio
import os
from dotenv import load_dotenv
from camera import show_rtsp_stream

# Load biến môi trường từ file .env
load_dotenv()

MODELS_DIR = os.path.join("src", "models")
DEFAULT_MODEL = os.path.join("src", "best.pt")


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


def find_available_models(models_dir: str = MODELS_DIR) -> list[str]:
    """Tìm tất cả file .pt trong thư mục models."""
    if not os.path.isdir(models_dir):
        return []

    model_files = []
    for file_name in os.listdir(models_dir):
        file_path = os.path.join(models_dir, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith(".pt"):
            model_files.append(file_path)
    return sorted(model_files)


def choose_model() -> str:
    """Cho người dùng chọn mô hình khi chạy main.py."""
    models = find_available_models()

    if not models:
        print("⚠️ Không tìm thấy mô hình nào trong thư mục src/models.")
        if os.path.exists(DEFAULT_MODEL):
            print(f"➡️ Sử dụng mặc định: {DEFAULT_MODEL}")
            return DEFAULT_MODEL
        raise FileNotFoundError(
            "Không có mô hình nào để sử dụng. Vui lòng thêm file .pt vào src/models."
        )

    print("🧠 Các mô hình hiện có:")
    for idx, model_path in enumerate(models, start=1):
        print(f"{idx}. {os.path.basename(model_path)}")

    while True:
        choice = input(
            f"👉 Chọn mô hình (1-{len(models)}) hoặc nhấn Enter để dùng mô hình 1: "
        ).strip()
        if choice == "":
            return models[0]

        if choice.isdigit():
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(models):
                return models[choice_idx]

        print("❌ Lựa chọn không hợp lệ. Vui lòng thử lại.")


async def main():
    rtsp_url = build_rtsp_url()
    model_path = choose_model()
    await show_rtsp_stream(rtsp_url, model_path=model_path)


if __name__ == "__main__":
    asyncio.run(main())
