import sqlite3

DATABASE = "blog.db"

def add(username,email,password):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        if cursor.execute("select COUNT(*) from users where username == ?",(username,)).fetchone()[0] == 1:
            print('Trùng username !!!')
        elif cursor.execute("select COUNT(*) from users where email == ?",(email,)).fetchone()[0] == 1:
            print("Trùng tên email !!!")
        else:
            cursor.execute(
            "INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
            (username, email, password, 1))
        conn.commit()
        conn.close()
        print("Hoàn thành tạo tài khoản admin!!!")
    except sqlite3.Error as e:
        print(f"lỗi khi truy cập database :{e}")
if __name__ == "__main__":
    print('khởi chạy quá trình tạo admin')
    add(input('nhập tên username:'),input('nhập vào email:'),input('nhập vào password:'))