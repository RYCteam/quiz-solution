# --- api1/app.py ---
# นี่คือโค้ดสำหรับ API ตัวแรก (Gateway)
# ทำหน้าที่เป็นประตูรับคำสั่งจาก User

from flask import Flask, request, jsonify
import requests
import logging
import os
import uuid

# สร้าง Instance ของ Flask app
app = Flask(__name__)

# ตั้งค่าการแสดง log ให้เห็นภาพชัดเจน
logging.basicConfig(level=logging.INFO, format='%(asctime)s - API1 - %(message)s')

# ดึง URL ของ API2 จาก Environment Variable ที่ตั้งค่าใน docker-compose.yml
# ถ้าหาไม่เจอ จะใช้ค่า default 'http://api2:5002/analyze'
API2_URL = os.environ.get('API2_URL', 'http://api2:5002/analyze')

@app.route('/analyze-image', methods=['POST'])
def analyze_image_gateway():
    """
    Endpoint หลักสำหรับรับ request จาก User
    แล้วส่งต่อไปยัง API2 เพื่อทำการวิเคราะห์
    """
    # สร้าง ID สำหรับติดตาม request นี้โดยเฉพาะ
    request_id = str(uuid.uuid4()).split('-')[0]
    logging.info(f"Request [{request_id}]: ได้รับคำสั่งใหม่จาก User")

    # ตรวจสอบว่า User ส่งข้อมูลมาในรูปแบบ JSON หรือไม่
    if not request.is_json:
        logging.error(f"Request [{request_id}]: ข้อมูลที่ส่งมาไม่ใช่ JSON")
        return jsonify({"error": "ข้อมูลต้องเป็น JSON เท่านั้น"}), 400

    # ดึงข้อมูลจาก JSON ที่ User ส่งมา
    user_data = request.get_json()
    image_to_analyze = user_data.get('image')

    # ตรวจสอบว่ามี key ชื่อ 'image' อยู่ใน JSON หรือไม่
    if not image_to_analyze:
        logging.error(f"Request [{request_id}]: ข้อมูลใน JSON ไม่ถูกต้อง (ไม่พบ key 'image')")
        return jsonify({"error": "กรุณาส่ง 'image' ใน JSON body"}), 400

    logging.info(f"Request [{request_id}]: กำลังส่งภาพ '{image_to_analyze}' ไปให้ API2 วิเคราะห์...")

    try:
        # เตรียมข้อมูลที่จะส่งไปให้ API2
        payload = {"image_name": image_to_analyze, "request_id": request_id}
        
        # ส่ง POST request ไปยัง API2
        response_from_api2 = requests.post(API2_URL, json=payload)
        response_from_api2.raise_for_status()  # หาก API2 ตอบกลับมาว่า error, จะโยน exception ทันที

        # รับผลลัพธ์จาก API2 กลับมา
        analysis_data = response_from_api2.json()
        logging.info(f"Request [{request_id}]: ได้รับผลวิเคราะห์จาก API2 เรียบร้อย")

        # เตรียมคำตอบสุดท้ายเพื่อส่งกลับไปให้ User
        final_response = {
            "requestId": request_id,
            "result": analysis_data
        }
        logging.info(f"Request [{request_id}]: ส่งคำตอบกลับให้ User สำเร็จ")
        return jsonify(final_response)

    except requests.exceptions.RequestException as e:
        # กรณีที่ไม่สามารถเชื่อมต่อกับ API2 ได้
        error_message = f"Request [{request_id}]: เกิดข้อผิดพลาดในการเชื่อมต่อกับ API2 - {e}"
        logging.error(error_message)
        return jsonify({"error": "ไม่สามารถติดต่อ Service ปลายทางได้"}), 500

if __name__ == '__main__':
    # กำหนดให้ API1 ทำงานที่ port 5001 ภายใน Docker
    # (ซึ่งเราได้ map port 8080 จากข้างนอกเข้ามาหา port นี้ใน docker-compose.yml)
    app.run(host='0.0.0.0', port=5001)
