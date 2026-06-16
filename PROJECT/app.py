from flask import Flask, render_template

app = Flask(__name__)

# Định nghĩa trang chủ web xem phim
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    print("Rạp phim đang chạy! Bấm vào liên kết ở góc phải màn hình để xem.")
    # Chạy ở chế độ debug=True để tự làm mới khi sửa giao diện
    app.run(debug=True)