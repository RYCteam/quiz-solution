# # AI For Thai Hackathon 2025 - Quiz Solution

# โปรเจกต์นี้เป็นโซลูชันสำหรับควิซครับ เป็นระบบง่ายๆ ที่มี API 2 ตัวคุยกัน ทำงานบน Docker

# ## มันทำงานยังไง?
# - **API1** (`./api1`): เป็นเหมือนประตูหน้าบ้าน คอยรับคำสั่งจากเรา
# - **API2** (`./api2`): เป็นเหมือนห้องเครื่องหลังบ้าน คอยทำงานวิเคราะห์ (ในที่นี้คือจำลองการทำงานเฉยๆ)

# เมื่อเราส่งคำสั่งไปที่ API1, มันจะส่งงานต่อไปให้ API2 แล้วเอาคำตอบกลับมาให้เราครับ

# ## วิธีรัน
# 1. ต้องมี Docker กับ Docker Compose ในเครื่องก่อนนะครับ
# 2. เปิด Terminal ขึ้นมา แล้ว `cd` เข้ามาในโฟลเดอร์นี้
# 3. สั่งรันด้วยคำสั่ง:
#    ```bash
#    docker compose up --build
#    ```
#    (ถ้าไม่ได้ลอง `docker-compose up --build`)

# ## วิธีเทส
# 1. เปิด Terminal อีกหน้าต่างนึง
# 2. ใช้ `curl` ยิงคำสั่งไปเทสได้เลย:
#    - **สำหรับ Windows (Command Prompt):**
#      ```bash
#     curl -X POST -H "Content-Type: application/json" -d "{\"image\": \"test_image_01.jpg\"}" http://localhost:8080/analyze-image 
#      ```
#    - **สำหรับ Mac/Linux หรือ PowerShell บน Windows:**
#      ```bash
#      curl -X POST -H "Content-Type: application/json" -d '{"image": "test_image_01.jpg"}' http://localhost:8080/analyze-image
#      ```

# ## ผลที่ได้
# ถ้าทุกอย่างถูก, เราจะได้ JSON ตอบกลับมาหน้าตาประมาณนี้:
# ```json
# {
#   "requestId": "xxxxxx",
#   "result": {
#     "confidence": 0.9,
#     "imageProcessed": "test_image_01.jpg",
#     "prediction": "Potential Drowning Detected",
#     "processingTime": "1.23s"
#   }
# }
# ```
# แล้วใน Terminal ที่รัน docker อยู่ ก็จะเห็น log การทำงานของ API ทั้งสองตัวขึ้นมาครับ
