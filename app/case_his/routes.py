from flask import render_template, flash, redirect, url_for, request, current_app, jsonify
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.models import Cases
from app.case_new.scraper.cp_case_scraper import CPCaseScraper

from app.case_his import bp


@bp.route('/case', methods=['GET', 'POST'])
@login_required
def case():
    page = request.args.get('page', 1, type=int)
    cases = Cases.query.filter_by(component=current_user.last_component).order_by(Cases.case_date.desc()).paginate(
        page, current_app.config['CASES_PER_PAGE'], False)
    next_url = url_for('case_his.case', page=cases.next_num) \
        if cases.has_next else None
    prev_url = url_for('case_his.case', page=cases.prev_num) \
        if cases.has_prev else None
    return render_template('case_his/case.html', title=_('His Case'),
                           cases=cases.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route("/show_case_details", methods=('GET', 'POST'))
def show_case_details():
    if request.method == 'POST':
        data = request.get_json()
        case_id = data.get('case_id')
        case_details = get_case_details(case_id)
    return jsonify({"case_details":case_details})


def get_case_details(case_id):
    scraper = CPCaseScraper()
    return scraper.scrape_case_messages(case_id)


@bp.route("/update_case", methods=('GET', 'POST'))
def update_case():
#     form = UpdateCaseForm()
#     if form.validate_on_submit():
    case_id = request.form['case-id']
    validate = request.form['validate']
    case_cover = request.form['case-cover']
    bug_cover = request.form['bug-cover']
    error = None
    if not case_id:
        error = 'case-id is required.'
    if error is None:
        Cases.query.filter_by(case_id=case_id).update({'validate':validate, 'case_cover':case_cover, 'bug_cover':bug_cover})
        db.session.commit()
        return ('', 204)
    flash(error)
#     flash(_("Failed to update case, please check..."))
    return redirect(url_for('index'))
