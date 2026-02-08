import sqlite3
from flask import Flask, request, jsonify
#Run
app = Flask(__name__)
# Push code
# LỖI 1: Hardcoded Secret
# Giả vờ đây là key để mã hóa dữ liệu
SECRET_KEY = "AKIAIOSFODNN7EXAMPLE"

# Hàm tạo database giả (Chạy mỗi khi khởi động app)
def init_db():
    conn = sqlite3.connect(':memory:') # Tạo DB trong RAM
    c = conn.cursor()
    c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, salary INTEGER)''')
    # Thêm dữ liệu mẫu
    c.execute("INSERT INTO users (username, email, salary) VALUES ('admin', 'admin@company.com', 5000)")
    c.execute("INSERT INTO users (username, email, salary) VALUES ('nhanvien', 'user@company.com', 1000)")
    conn.commit()
    return conn

# Khởi tạo DB
db_connection = init_db()

@app.route('/')
def home():
    return "<h1>Hệ thống Quản lý Nhân sự (Vulnerable)</h1><p>Dùng /api/user?username=admin để test</p>"

@app.route('/api/user', methods=['GET'])
def get_user():
    username = request.args.get('username')
    
    if not username:
        return jsonify({"error": "Vui long nhap username"}), 400

    cursor = db_connection.cursor()
    
    # LỖI 2 (SAST & DAST): SQL Injection
    # Cộng chuỗi trực tiếp! Hacker có thể nhập: admin' OR '1'='1
    query = f"SELECT * FROM users WHERE username = '{username}'"
    
    try:
        print(f"Executing query: {query}") # In log để thấy lệnh SQL
        cursor.execute(query)
        data = cursor.fetchall()
        
        if data:
            return jsonify({"results": data})
        else:
            return jsonify({"message": "Khong tim thay user"}), 404
            
    except Exception as e:
        # LỖI 3: In lỗi SQL ra màn hình -> Hacker biết cấu trúc DB
        return jsonify({"database_error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
