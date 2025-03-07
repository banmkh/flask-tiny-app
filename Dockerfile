FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -r requirements.txt

# Xóa database cũ nếu có, sau đó tạo mới
RUN rm -f blog.db && python scripts/init_db.py && python scripts/simulate_data.py

RUN chmod +x manage.py

EXPOSE 5000

CMD ["python", "manage.py"]