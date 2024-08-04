from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

from flask_bcrypt import Bcrypt

from flask_jwt_extended import JWTManager

from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
bcrypt=Bcrypt()
jwt=JWTManager()

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    CORS(app)
    
    from .auth_route import auth_blueprint
    from .game_route import game_blueprint

  

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(game_blueprint)
   
    return app