from flask import Blueprint

bp = Blueprint('case', __name__)

from app.case import routes
