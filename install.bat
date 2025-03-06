@echo off
echo Setting up the project...

:: Kiểm tra Python
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b
)

:: Xóa database cũ nếu tồn tại
if exist blog.db (
    echo Deleting old database...
    del blog.db
)

:: Tạo môi trường ảo
echo Creating virtual environment...
python -m venv venv

:: Kích hoạt môi trường ảo
call venv\Scripts\activate

:: Cài đặt dependencies từ requirements.txt
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

:: Khởi tạo database mới
echo Initializing new database...
python scripts\init_db.py

:: Tạo dữ liệu mô phỏng
echo Simulating data...
python scripts\simulate_data.py

:: Chạy hệ thống
echo Starting the system...
python manage.py
