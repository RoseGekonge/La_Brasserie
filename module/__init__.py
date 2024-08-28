from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model.db'
app.config['SECRET_KEY'] = 'a45d138867d8dea199b3975f'
app.secret_key = "2cddd63c4c0fbfa32c9c9b41"
app.permanent_session_lifetime = timedelta(minutes=1440)
app.app_context().push()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from module import routes