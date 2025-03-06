FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# Xóa database cũ nếu có, sau đó tạo mới
RUN rm -f blog.db && python scripts/init_db.py && python scripts/simulate_data.py

CMD ["python", "manage.py"]
