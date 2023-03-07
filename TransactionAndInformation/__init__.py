from flask import Blueprint

tranAndInfo = Blueprint('TransactionAndInformation', __name__, template_folder='templates')

from TransactionAndInformation import routes
