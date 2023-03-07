from flask import Blueprint

dboard = Blueprint('Dashboard', __name__,
                   template_folder='templates', static_folder='static')

from Dashboard import routes
