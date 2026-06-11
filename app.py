import pymssql
import pandas as pd
import gradio as gr
from sklearn.linear_model import LogisticRegression
import numpy as np

def get_html_inventory(search_query=""):
    try:
        conn = pymssql.connect(
            server='localhost', user='sa', password='YourStrongPassword123!', database='master'
        )
        query = "SELECT ProductName, InStock, Available, InTransaction FROM Inventory"
        df = pd.read_sql(query, conn)
        conn.close()
    except Exception:
        # Dữ liệu dự phòng chuẩn theo mẫu Điện máy Xanh
        df = pd.DataFrame({
            "ProductName": [
                "Curved Smart TV KS9500 78\"", "TV CrystalUHD4K RU7300 55\"",
                "CrystalUHD4K RU7300 55\"", "Samsung Smart TV The Serif 55\"",
                "TV Samsung 4k UA70RU7200 70\""
            ],
            "InStock": [6, 4, 12, 5, 6],
            "Available": [4, 3, 6, 1, 5],
            "InTransaction": [2, 1, 1, 0, 4]
        })

    # Bộ lọc tìm kiếm nhanh
    if search_query:
        df = df[df['ProductName'].str.contains(search_query, case=False)]

    # Tính toán số liệu tổng quan cho Dashboard
    total_types = len(df)
    total_stock = int(df['InStock'].sum())
    total_avail = int(df['Available'].sum())

    # Tạo bảng HTML mới - Sạch sẽ, không lỗi ảnh
    html_code = """
    <table style="width:100%; border-collapse: collapse; font-family: sans-serif; text-align: left; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
        <tr style="background-color: #f8fafc; border-bottom: 2px solid #e2e8f0; color: #64748b;">
            <th style="padding: 14px;">Tên Sản Phẩm</th>
            <th style="padding: 14px; text-align: center;">Tồn kho</th>
            <th style="padding: 14px; text-align: center;">Có thể bán</th>
            <th style="padding: 14px; text-align: center;">Đang giao dịch</th>
        </tr>
    """
    
    for _, row in df.iterrows():
        html_code += f"""
        <tr style="border-bottom: 1px solid #f1f5f9; hover:background-color: #f8fafc;">
            <td style="padding: 14px; font-weight: 600; color: #1e293b;">{row['ProductName']}</td>
            <td style="padding: 14px; text-align: center; color: #334155; font-size: 15px;"><b>{row['InStock']}</b></td>
            <td style="padding: 14px; text-align: center; color: #16a34a; font-size: 15px;"><b>{row['Available']}</b></td>
            <td style="padding: 14px; text-align: center; color: #ea580c; font-size: 15px;"><b>{row['InTransaction']}</b></td>
        </tr>
        """
    html_code += "</table>"
    
    return total_types, total_stock, total_avail, html_code

# PHẦN MACHINE LEARNING DỰ BÁO
X = np.array([[4, 2], [3, 1], [6, 1], [1, 0], [5, 4], [0, 5], [1, 5]])
y = np.array([1, 1, 1, 1, 1, 0, 0])
model = LogisticRegression().fit(X, y)

def predict_stock_risk(available, transaction):
    pred = model.predict([[available, transaction]])
    return "🟢 Trạng thái ổn định: Không có rủi ro thiếu hụt." if pred[0] == 1 else "🔴 CẢNH BÁO: Hàng hóa có nguy cơ đứt gãy lớn! Đề xuất nhập kho gấp."

# THIẾT KẾ WEB UI DOANH NGHIỆP - STYLE ĐIỆN MÁY XANH
with gr.Blocks(title="Điện máy Xanh - Hệ thống ERP", theme=gr.themes.Soft(primary_hue="blue")) as demo:
    
    gr.HTML("""
    <div style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); padding: 25px; border-radius: 12px; text-align: center; color: white; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(3,105,161,0.2);">
        <h1 style="margin: 0; color: #e0f2fe; font-size: 30px; font-weight: 800; letter-spacing: 1.5px;"> ĐIỆN MÁY XANH </h1>
        <p style="margin: 6px 0 0 0; color: #e0f2fe; font-size: 16px;">Hệ Thống Phân Phối & Kiểm Kê Tồn Kho Kỹ Thuật Số</p>
        <div style="margin-top: 10px; font-size: 13px; color: #bae6fd; background: rgba(255,255,255,0.1); display: inline-block; padding: 4px 12px; border-radius: 20px;">
            Học phần: Phát triển ứng dụng Doanh nghiệp | Sinh viên: Trương Vĩ Khang-24661012
        </div>
    </div>
    """)
    
    with gr.Tab(" Danh Mục Hàng Hóa"):
        with gr.Row():
            kpi_types = gr.Number(label="Tổng số dòng TV", interactive=False)
            kpi_stock = gr.Number(label="Tổng số lượng tồn kho", interactive=False)
            kpi_avail = gr.Number(label="Tổng số lượng sẵn sàng bán", interactive=False)
            
        gr.Markdown("<br>")
        
        with gr.Row():
            search_input = gr.Textbox(placeholder=" Gõ từ khóa để lọc nhanh tivi (Ví dụ: Curved, RU7300, 55\"...)", label="Tìm kiếm sản phẩm nhanh")
            refresh_btn = gr.Button(" ĐỒNG BỘ DỮ LIỆU HỆ THỐNG", variant="primary")
            
        gr.Markdown("###  DANH SÁCH THIẾT BỊ TRONG KHO")
        inventory_output = gr.HTML()
        
        # Tự động nạp dữ liệu khi mở web hoặc thao tác
        demo.load(fn=get_html_inventory, outputs=[kpi_types, kpi_stock, kpi_avail, inventory_output])
        refresh_btn.click(fn=get_html_inventory, inputs=search_input, outputs=[kpi_types, kpi_stock, kpi_avail, inventory_output])
        search_input.change(fn=get_html_inventory, inputs=search_input, outputs=[kpi_types, kpi_stock, kpi_avail, inventory_output])

    with gr.Tab(" AI Dự Báo & Cảnh Báo Chuỗi Cung Ứng"):
        gr.Markdown("###  Trí Tuệ Nhân Tạo Quản Trị Rủi Rô Đứt Gãy Tồn Kho")
        with gr.Row():
            num_avail = gr.Number(label="Số lượng có thể bán", value=4)
            num_trans = gr.Number(label="Số lượng đang giao dịch phát sinh", value=2)
        predict_output = gr.Textbox(label="Khuyến nghị từ mô hình AI (Logistic Regression)", interactive=False)
        predict_btn = gr.Button("Phân tích trạng thái rủi ro", variant="stop")
        predict_btn.click(fn=predict_stock_risk, inputs=[num_avail, num_trans], outputs=predict_output)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)