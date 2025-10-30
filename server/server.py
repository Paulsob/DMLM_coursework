from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import os
import json





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

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


# Initialize real music model if configured
CONFIG = load_config()
MUSIC_MODEL = None
try:
    music_cfg = CONFIG.get('models', {}).get('music', {})
    if music_cfg.get('model_path') and music_cfg.get('index_path'):
        print('произошла загрузка модели музки')
        # MUSIC_MODEL = Music(
        #     model_path=music_cfg['model_path'],
        #     index_path=music_cfg['index_path'],
        #     sample_rate=music_cfg.get('sample_rate', 22050),
        #     n_mels=music_cfg.get('n_mels', 128),
        #     hop_length=music_cfg.get('hop_length', 512),
        #     duration_sec=music_cfg.get('duration_sec', 30),
        #     top_k=music_cfg.get('top_k', 5),
        # )
except Exception as e:
    # If loading fails, keep MUSIC_MODEL as None
    print(f"[WARN] Music model initialization failed: {e}")


def music_predict_from_file_storage(file_storage):
    if MUSIC_MODEL is None:
        return {"model2_result": random.randint(1, 10), "note": "music model not loaded"}
    wav_bytes = file_storage.read()
    return MUSIC_MODEL.infer_from_wav_bytes(wav_bytes)

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
        if request.content_type and 'multipart/form-data' in request.content_type and file_type == 'music' and file is not None:
            res_music = music_predict_from_file_storage(file)
            return jsonify(res_music)
        else:
            res1 = images_predict(data)
            res2 = {"model2_result": random.randint(1, 10)}
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