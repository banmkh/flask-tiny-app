# FLASK TINY APP

## 1. Thông tin nhóm
- **Sinh viên 1:**
  - Họ và tên: Đoàn Vũ Thiên Ban
  - Mã sinh viên: 22710261
- **Sinh viên 2:**
  - Họ và tên: Phan Tấn Tài
  - Mã sinh viên: 22686181

## 2. Mô tả Project
Flask Tiny App là một blog app nhỏ gọn, sử dụng **Flask** để xây dựng hệ thống quản lý bài viết với các chức năng chính:
- **Quản lý bài viết:** Thêm, xóa, chỉnh sửa bài viết.
- **Chức năng đăng nhập/đăng ký:** Hỗ trợ user authentication.
- **Phân quyền admin:** Admin quản lý user, khóa user, đặt lại mật khẩu.
- **Hỗ trợ phân trang:** Chia danh sách bài viết theo trang.
- **Xóa nhiều bài viết cùng lúc:** Giúp người dùng quản lý nội dung dễ dàng hơn.
- **Triển khai Docker:** Dễ dàng deploy bằng Docker.

## 3. Hướng dẫn cài đặt và chạy

### **Cài đặt trên Windows**
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python scripts\init_db.py
python scripts\simulate_data.py
python manage.py
```
hoặc chạy lệnh:
```cmd
install.bat
```

### **Cài đặt trên Linux/macOS**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/init_db.py
python scripts/simulate_data.py
python manage.py
```
hoặc chạy lệnh:
```bash
chmod +x install.sh
./install.sh
```
---

## 5. Ghi chú
- Nếu số lượng bài viết ít hơn số giới hạn trên mỗi trang, thanh phân trang sẽ không hiển thị.
- Chỉ chủ sở hữu bài viết mới có thể thực hiện thao tác xóa bài viết.
- Tính năng phân trang giúp load dữ liệu nhanh hơn và dễ dàng quản lý bài viết.

