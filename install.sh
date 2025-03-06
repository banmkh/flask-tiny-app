#!/bin/bash

echo "Setting up the project..."

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

# Xóa database cũ nếu tồn tại
if [ -f "blog.db" ]; then
    echo "Deleting old database..."
    rm blog.db
fi

# Tạo môi trường ảo
echo "Creating virtual environment..."
python3 -m venv venv

# Kích hoạt môi trường ảo
source venv/bin/activate

# Cài đặt dependencies từ requirements.txt
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Khởi tạo database mới
echo "Initializing new database..."
python scripts/init_db.py

# Tạo dữ liệu mô phỏng
echo "Simulating data..."
python scripts/simulate_data.py

# Chạy hệ thống
echo "Starting the system..."
python manage.py
