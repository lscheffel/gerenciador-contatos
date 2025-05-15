from flask import Flask
from flask_cors import CORS
from app.routes import api_bp
from app.models import init_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4321"}})  # Permite apenas o frontend Astro
app.register_blueprint(api_bp, url_prefix="/api")

@app.route("/")
def health_check():
    logger.info("Health check acessado")
    return {"status": "API is running"}

if __name__ == "__main__":
    init_db()
    logger.info("Iniciando aplicação Flask")
    app.run(debug=True, host="0.0.0.0", port=5000)