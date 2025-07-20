# --- api2/app.py ---
# นี่คือโค้ดสำหรับ API ตัวที่สอง (Analysis Engine)
# ทำหน้าที่จำลองการวิเคราะห์ภาพที่ได้รับจาก API1

from flask import Flask, request, jsonify
import logging
import random
import time

# สร้าง Instance ของ Flask app
app = Flask(__name__)

# ตั้งค่าการแสดง log ให้เห็นภาพชัดเจน
logging.basicConfig(level=logging.INFO, format='%(asctime)s - API2 - %(message)s')

@app.route('/analyze', methods=['POST'])
def analyze_image_engine():
    """
    Endpoint หลักสำหรับรับข้อมูลจาก API1 และจำลองการวิเคราะห์
    """
    # ตรวจสอบว่า API1 ส่งข้อมูลมาในรูปแบบ JSON หรือไม่
    if not request.is_json:
        # โดยปกติ User จะไม่เห็น error นี้ เพราะ API1 จะส่ง JSON มาเสมอ
        return jsonify({"error": "ข้อมูลต้องเป็น JSON เท่านั้น"}), 400

    # ดึงข้อมูลจาก JSON ที่ API1 ส่งมา
    data_from_api1 = request.get_json()
    image_name = data_from_api1.get('image_name', 'unknown_image')
    request_id = data_from_api1.get('request_id', 'N/A')

    logging.info(f"Request [{request_id}]: ได้รับคำสั่งให้วิเคราะห์ภาพ '{image_name}'")

    # จำลองการทำงานที่ต้องใช้เวลาคิด, เช่น การประมวลผลของโมเดล AI
    processing_time = random.uniform(0.5, 1.5)
    time.sleep(processing_time)

    # จำลองผลลัพธ์การวิเคราะห์แบบสุ่ม
    possible_results = ["Normal", "Potential Drowning Detected"]
    result = random.choice(possible_results)
    confidence = random.uniform(0.85, 0.99)

    # เตรียมผลลัพธ์เพื่อส่งกลับไปให้ API1
    response_data = {
        "imageProcessed": image_name,
        "prediction": result,
        "confidence": round(confidence, 4),
        "processingTime": f"{round(processing_time, 2)}s"
    }
    logging.info(f"Request [{request_id}]: วิเคราะห์เสร็จสิ้น, ส่งผลลัพธ์กลับไปให้ API1")
    return jsonify(response_data)

if __name__ == '__main__':
    # กำหนดให้ API2 ทำงานที่ port 5002 ภายใน Docker
    app.run(host='0.0.0.0', port=5002)
