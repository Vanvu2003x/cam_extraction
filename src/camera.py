def build_rtsp_url(username: str, password: str, ip: str, port: int = 554, channel: int = 1, subtype: int = 0) -> str:
    #Tạo Doctring mô tả hàm
    """
    Tạo URL RTSP cho camera.
    Args:
        username (str): Tên đăng nhập camera
        password (str): Mật khẩu camera
        ip (str): IP của camera
        port (int, optional): Port RTSP. Mặc định 554
        channel (int, optional): Channel camera. Mặc định 1
        subtype (int, optional): 0 = chính, 1 = phụ. Mặc định 0

    Returns:
        str: URL RTSP đầy đủ
    """
    return f"rtsp://{username}:{password}@{ip}:{port}/cam/realmonitor?channel={channel}&subtype={subtype}"
