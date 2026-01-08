import os
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS 


from routes.logistica_routes import logistica_bp
from routes.produccion_routes import produccion_bp 
from routes.catalogos_routes import catalogos_bp

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
CORS(app) 

app.register_blueprint(logistica_bp)
app.register_blueprint(produccion_bp)
app.register_blueprint(catalogos_bp)

@app.route('/')
def index():
    return "¡Saturno v2.0 está en línea!"

if __name__ == '__main__':
    app.run(debug=True)