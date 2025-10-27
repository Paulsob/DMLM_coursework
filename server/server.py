from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import os

app = Flask(__name__, static_folder='../client')
CORS(app)  # позволяет фронтенду (HTML/JS) обращаться к серверу с другого порта

@app.route("/")
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/favicon.ico')
def favicon():
    return '', 204

def images_predict(data):
    return {"model1_result": random.randint(1, 10)}

def music_predict(data):
    return {"model2_result": random.randint(1, 10)}

def text_predict(data):
    return {"model3_result": random.randint(1, 10)}

@app.route("/predict", methods=["POST"])
def predict():
    """
    Обработка запросов от клиента
    Поддерживает как FormData (для файлов), так и JSON (для текста)
    """
    try:
        # Проверяем тип контента
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Обработка файлов (изображения, музыка)
            file = request.files.get('file')
            file_type = request.form.get('type')
            
            if not file:
                return jsonify({"error": "Файл не найден"}), 400
            
            # Симулируем обработку файла
            data = [1, 2, 3, 4, 5]  # Заглушка для данных файла
            
        else:
            # Обработка JSON (текст)
            content = request.get_json()
            if not content:
                return jsonify({"error": "JSON данные не найдены"}), 400
            
            text = content.get("text", "")
            file_type = content.get("type", "text")
            
            if not text:
                return jsonify({"error": "Текст не найден"}), 400
            
            # Симулируем обработку текста
            data = [len(text), len(text.split()), len(text.split('.'))]  # Простые метрики текста

        # Выполняем предсказания
        res1 = images_predict(data)
        res2 = music_predict(data)
        res3 = text_predict(data)

        combined_result = {
            **res1,
            **res2,
            **res3,
            "final_result": (res1["model1_result"] + res2["model2_result"] + res3["model3_result"]) // random.randint(1, 10),
            "type": file_type
        }

        return jsonify(combined_result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  