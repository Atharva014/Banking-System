from flask import Blueprint

moneyTran = Blueprint('MoneyTransaction', __name__, template_folder='templates')

from MoneyTransaction import routes
