from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired
from flask_babel import _, lazy_gettext as _l


class NewComponentForm(FlaskForm):
    component = StringField(_l('Component'), validators=[DataRequired()])
    search_date = DateField(_l('Search Date'), validators=[DataRequired()])
    submit = SubmitField(_l('ADD'))
