from flask import Flask
from app.routes import api_bp
from app.models import init_db
import logging

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix="/api")

@app.route("/")
def health_check():
    logger.info("Health check acessado")
    return {"status": "API is running"}

if __name__ == "__main__":
    init_db()  # Cria tabelas
    logger.info("Iniciando aplicação Flask")
    app.run(debug=True, host="0.0.0.0", port=5000)