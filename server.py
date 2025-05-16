from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import base64
import io
from datetime import datetime
from PIL import Image

app = Flask(__name__)
CORS(app)  # 解决跨域问题
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

from flask import send_file

@app.route("/defect_log.txt")
def serve_txt():
    return send_file("defect_log.txt", mimetype="text/plain")

@app.route('/')
def index():
    """展示实时监控页面"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_data():
    """接收检测结果数据"""
    try:
        # 解析JSON数据

        data = request.form  # 获取表单字段
        id=data.get('id')
        defect_type = data.get('type')
        confidence = data.get('confidence')

        # 获取上传的图像文件
        image_file = request.files.get('image')
        if not image_file:
            return jsonify({"status": "error", "message": "缺少图像文件"}), 400

        img_bytes = image_file.read()  # 读取图像二进制数据

        # 解码并保存图片
        img = Image.open(io.BytesIO(img_bytes))
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{defect_type}.jpg"
        if id==0:
            img.save(os.path.join(UPLOAD_FOLDER+"/car0", filename))
        if id==1:
            img.save(os.path.join(UPLOAD_FOLDER+"/car1", filename))
        if id==2:
            img.save(os.path.join(UPLOAD_FOLDER+"/car2", filename))
        if id==3:
            img.save(os.path.join(UPLOAD_FOLDER+"/car3", filename))

        # 记录日志
        log_entry = f"{datetime.now()} {defect_type} {confidence}\n"
        with open('defect_log.txt', 'a') as f:
            f.write(log_entry)

        return jsonify({"status": "success", "message": "数据接收成功"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
# 坑洼缺陷

@app.route('/api/image0', methods=['GET'])
def get_image0():
    """返回 uploads 文件夹中所有图片的路径"""
    image_files = [f for f in os.listdir('static/uploads/car0') if f.endswith(('.jpg', '.jpeg', '.png'))]
    image_file=image_files[-1]
    #image_urls = [f"/static/uploads/{f}" for f in image_files]  # 构造图片的URL

    image_urls = [f"/static/uploads/car0/{image_file}"]
    return jsonify({"images": image_urls})
@app.route('/api/image1', methods=['GET'])
def get_image1():
    """返回 uploads 文件夹中所有图片的路径"""
    image_files = [f for f in os.listdir('static/uploads/car1') if f.endswith(('.jpg', '.jpeg', '.png'))]
    image_file=image_files[-1]
    #image_urls = [f"/static/uploads/{f}" for f in image_files]  # 构造图片的URL

    image_urls = [f"/static/uploads/car1/{image_file}"]
    return jsonify({"images": image_urls})
@app.route('/api/image2', methods=['GET'])
def get_image2():
    """返回 uploads 文件夹中所有图片的路径"""
    image_files = [f for f in os.listdir('static/uploads/car2') if f.endswith(('.jpg', '.jpeg', '.png'))]
    image_file=image_files[-1]
    #image_urls = [f"/static/uploads/{f}" for f in image_files]  # 构造图片的URL

    image_urls = [f"/static/uploads/car2/{image_file}"]
    return jsonify({"images": image_urls})
@app.route('/api/image3', methods=['GET'])
def get_image3():
    """返回 uploads 文件夹中所有图片的路径"""
    image_files = [f for f in os.listdir('static/uploads/car3') if f.endswith(('.jpg', '.jpeg', '.png'))]
    image_file=image_files[-1]
    #image_urls = [f"/static/uploads/{f}" for f in image_files]  # 构造图片的URL

    image_urls = [f"/static/uploads/car3/{image_file}"]
    return jsonify({"images": image_urls})

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """统计各类缺陷数量"""
    from collections import Counter
    try:
        counter = Counter()
        if os.path.exists('defect_log.txt'):
            with open('defect_log.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split()  # 使用空格分割
                    if len(parts) >= 2:
                        defect_type = parts[1]
                        counter[defect_type] += 1
        return jsonify(counter)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
