import pymssql

try:
    conn = pymssql.connect(
        server='localhost',
        user='sa',
        password='YourStrongPassword123!',
        database='master'
    )
    cursor = conn.cursor()
    
    # Tạo hoặc làm sạch bảng Inventory
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Inventory' AND xtype='U')
    CREATE TABLE Inventory (
        ProductID INT PRIMARY KEY,
        ProductName NVARCHAR(200),
        InStock INT,
        Available INT,
        InTransaction INT
    )
    """)
    cursor.execute("TRUNCATE TABLE Inventory")
    
    # Nạp đầy đủ 5 sản phẩm tivi theo mẫu dữ liệu
    data = [
        (1, "Curved Smart TV KS9500 78\"", 6, 4, 2),
        (2, "TV CrystalUHD4K RU7300 55\"", 4, 3, 1),
        (3, "CrystalUHD4K RU7300 55\"", 12, 6, 1),
        (4, "Samsung Smart TV The Serif 55\"", 5, 1, 0),
        (5, "TV Samsung 4k UA70RU7200 70\"", 6, 5, 4)
    ]
    
    cursor.executemany("INSERT INTO Inventory VALUES (%d, %s, %d, %d, %d)", data)
    conn.commit()
    print("🎉 Đã cập nhật đầy đủ sản phẩm của ĐIỆN MÁY XANH vào SQL Server!")
    conn.close()
except Exception as e:
    print(f"❌ Lỗi khởi tạo database: {e}")