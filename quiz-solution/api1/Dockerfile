# ใช้ Python image เป็นพื้นฐาน
FROM python:3.9-slim

# กำหนด Working Directory ภายใน Container
WORKDIR /app

# คัดลอกไฟล์ requirements.txt เข้าไปก่อน
COPY requirements.txt .

# ติดตั้ง Dependencies ที่จำเป็น
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดทั้งหมดในโฟลเดอร์ api1 เข้าไป
COPY . .

# กำหนดให้ Container นี้ทำงานที่ port 5001
EXPOSE 5001

# คำสั่งสำหรับรันแอปพลิเคชันเมื่อ Container เริ่มทำงาน
CMD ["python", "app.py"]