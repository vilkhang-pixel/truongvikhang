import cv2

class VideoCamera:
    def __init__(self, source=0):
        # Khởi tạo camera (mặc định là 0)
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise ValueError("Không thể mở camera. Vui lòng kiểm tra lại kết nối!")

    def start_preview(self):
        print("Đang mở camera... Nhấn phím 'q' trên cửa sổ video để THOÁT.")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Lỗi: Không thể nhận luồng dữ liệu.")
                break

            # Hiển thị video
            cv2.imshow('Camera Preview', frame)

            # Bấm 'q' để thoát
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        self.stop()

    def stop(self):
        # Giải phóng camera và đóng cửa sổ
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        print("Đã tắt camera thành công.")