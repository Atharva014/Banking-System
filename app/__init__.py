from flask import Flask
from app.config import Config
from app.models import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
with app.app_context():
    db.create_all()

app.secret_key = "Atharva"

from app import routes
from Dashboard import dboard
from TransactionAndInformation import tranAndInfo
from MoneyTransaction import moneyTran

app.register_blueprint(dboard, url_prefix='/Dashboard')
app.register_blueprint(tranAndInfo, url_prefix='/TranInfo')
app.register_blueprint(moneyTran, url_prefix='/MoneyTran')
