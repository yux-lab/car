import cv2
import requests
import base64
import time
import json
import random
import os
import io
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件中的环境变量

SERVER_URL = os.getenv("SERVER_URL")
CAMERA_ID = int(os.getenv("CAMERA_ID", "0"))  # 默认值设为 0


def capture_image():
    """捕获摄像头图像并返回Base64编码"""
    cap = cv2.VideoCapture(CAMERA_ID)
    ret, frame = cap.read()
    cap.release()

    if ret:
        # 图像预处理
        frame = cv2.resize(frame, (224, 224))  # 调整分辨率
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])# 压缩质量
        return base64.b64encode(buffer).decode('utf-8')
    return None


def detect_defect():
    """模拟缺陷检测（需替换为实际检测模型）"""
    # 此处应接入YOLO/TensorRT等检测模型
    defect_type = random.choice(["crack", "dent"])
    confidence = round(85 + random.random() * 10, 1)
    return {"type": defect_type, "confidence": confidence}


def main_loop():
    while True:
        try:
            # 捕获并处理图像
            start_time = time.time()  # 拍摄开始前记录时间
            img_base64 = capture_image()
            if not img_base64:
                continue

            # 获取检测结果
            detection = detect_defect()

            # 构建要发送的文件和额外数据
            files = {
                'image': ('image.jpg', io.BytesIO(base64.b64decode(img_base64)), 'image/jpeg')
            }
            data = {
                "type": detection["type"],
                "confidence": detection["confidence"]
            }

            # 发送POST请求
            response = requests.post(
                SERVER_URL,
                id=0,
                data=data,  # 额外字段使用 data 参数
                files=files,  # 文件使用 files 参数
                timeout=5
            )

            print(f"上传结果: {response.status_code} - {response.json()}")
            end_time = time.time()  # 上传完成后记录时间
            print(f"总耗时: {end_time - start_time:.2f} 秒")
            #time.sleep(1)  # 采样间隔

        except Exception as e:
            print(f"发生错误: {str(e)}")
            #time.sleep(1)


if __name__ == '__main__':
    main_loop()
