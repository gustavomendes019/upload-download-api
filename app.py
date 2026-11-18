from flask import Flask, jsonify
from database.db import init_db
from routes.upload_route import upload_bp
from routes.download_route import download_bp
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

init_db()

app.register_blueprint(upload_bp, url_prefix='/uploads')
app.register_blueprint(download_bp, url_prefix='/downloads')


# Rota inicial: confirma que a API está no ar e lista as rotas disponíveis
@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "mensagem": "API de Upload e Download de arquivos",
        "rotas": {
            "upload": "POST /uploads/upload (form-data, campo 'file')",
            "download": "GET /downloads/download/<nome_do_arquivo>"
        }
    })


if __name__ == '__main__':
    # Em produção (Render) a API roda com o Gunicorn; este bloco é só para rodar localmente.
    # O Render informa a porta pela variável de ambiente PORT.
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)
