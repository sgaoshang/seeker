from flask import Blueprint

bp = Blueprint('case_new', __name__)

from app.case_new import routes
