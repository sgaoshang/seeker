from flask import Blueprint

bp = Blueprint('case_his', __name__)

from app.case_his import routes
