from app.camera import VideoCamera

def main():
    try:
        # Khởi tạo và chạy camera
        cam = VideoCamera(source=0)
        cam.start_preview()
        
    except ValueError as e:
        print(f"Cảnh báo: {e}")
    except Exception as e:
        print(f"Đã xảy ra lỗi hệ thống: {e}")

if __name__ == "__main__":
    main()