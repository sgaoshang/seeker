from flask import render_template, flash, redirect, url_for, request, current_app, jsonify, session
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.models import Component
from app.component.forms import NewComponentForm

from app.component import bp


@bp.route('/new_component', methods=['GET', 'POST'])
@login_required
def new_component():
    form = NewComponentForm()
    if form.validate_on_submit():
        component = Component(component=form.component.data, search_date=form.search_date.data)
        db.session.add(component)
        db.session.commit()
        session['components'].append(form.component.data)
        flash(_('Congratulations, new component has been added!'))
        return redirect(url_for('index'))
    return render_template('component/new_component.html', title=_('New Component'),
                           form=form)
