import os
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv


from models.models import db, TipoMaterial, Material, Producto, ProductoReceta
load_dotenv()
app = Flask(__name__)

USER = os.getenv('DB_USER')
PASS = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
DBNAME = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER}:{PASS}@{HOST}/{DBNAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return "¡Saturno v2.0 está en línea!"

from routes.logistica_routes import logistica_bp


app.register_blueprint(logistica_bp)
# Permitir CORS para que Angular no llore
from flask_cors import CORS
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)