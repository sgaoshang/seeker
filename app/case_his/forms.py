from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_babel import _, lazy_gettext as _l


class CaseSearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(CaseSearchForm, self).__init__(*args, **kwargs)


class UpdateCaseForm(FlaskForm):
    case_id = StringField(_l('Case_ID'), validators=[DataRequired()])
    validate = StringField(_l('Validate'), validators=[DataRequired()])
    case_cover = StringField(_l('Case_Cover'), validators=[DataRequired()])
    bug_cover = StringField(_l('Bug_Cover'), validators=[DataRequired()])
