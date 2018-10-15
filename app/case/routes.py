from flask import render_template, flash, redirect, url_for, request, current_app, jsonify, session
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.models import Cases
from app.models import Component
from app.case.scraper.cp_case_scraper import CPCaseScraper
from app.case.forms import UpdateCaseForm, CaseSearchForm

from math import ceil
import datetime
from app.case import bp


@bp.before_app_request
def before_app_request():
    if current_user.is_authenticated and current_user.last_component:
        try:
            new_case_id_list = session['new_case_id_list']
        except KeyError:
            new_case_id_list = None
        if new_case_id_list is None:
            if current_user.is_authenticated:
                session['new_case_id_list'] = get_case_id_list(current_user.last_component)
                current_app.logger.info("Re-fetch session[new_case_id_list]: %s" % session['new_case_id_list'])


def get_case_id_list(component):
    # case_id_list = []
    scraper = CPCaseScraper()
    search_date = get_search_date(component)
    # while not case_id_list:
#     for i in range(5):
#         if not case_id_list:
    case_id_list, update_date = scraper.scrape_cases_id_via_date(component, search_date)
    if update_date != "" and datetime.datetime.strptime(update_date, '%Y-%m-%d') > datetime.datetime.strptime(search_date, '%Y-%m-%d'):
        update_search_date(component, datetime.datetime.strptime(update_date, '%Y-%m-%d'))
#         if case_id_list:
#             current_app.logger.info("case_id_list %s" % case_id_list)
#             return case_id_list
#         else:
#             current_app.logger.info("Failed to get case_id_list from CP, retry %s times" % i)
    return case_id_list


@bp.route('/his_case', methods=['GET', 'POST'])
@login_required
def his_case():
    page = request.args.get('page', 1, type=int)
    cases = Cases.query.filter_by(component=current_user.last_component).order_by(Cases.case_date.desc()).paginate(
        page, current_app.config['CASES_PER_PAGE'], False)
    next_url = url_for('case.his_case', page=cases.next_num) \
        if cases.has_next else None
    prev_url = url_for('case.his_case', page=cases.prev_num) \
        if cases.has_prev else None
    return render_template('case/his_case.html', title=_('His Case'),
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
#     return "fake details"


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


@bp.route('/new_case', methods=['GET', 'POST'])
@login_required
def new_case():
    page = request.args.get('page', 1, type=int)
    cases = []
    next_url = None
    prev_url = None
    component = current_user.last_component
    if component:
        new_case_id_list = session['new_case_id_list']
        total = len(new_case_id_list)
        per_page = current_app.config['CASES_PER_PAGE']
        pages = int(ceil(total / float(per_page)))
        start = (page - 1) * per_page
        if total <= per_page:
            # display only one page
            per_page = total
        else:
            end = start + per_page
            if end >= total:
                # display last page
                per_page = total - start
    
        cases = []
        scraper = CPCaseScraper()
        for case_id in new_case_id_list[start:start + per_page]:
            cases.append(scraper.scrape_case_dict(component, case_id))
        next_url = url_for('case.new_case', page=page + 1) \
            if page < pages else None
        prev_url = url_for('case.new_case', page=page - 1) \
            if page > 1 else None
    return render_template('case/new_case.html', title=_('New Case'),
                           cases=cases, next_url=next_url,
                           prev_url=prev_url)


@bp.route("/save_case", methods=('GET', 'POST'))
def save_case():
    case_id = request.form['case-id']
    predict = request.form['predict']
    validate = request.form['validate']
    case_date = request.form['case-date']
    status = request.form['status']
    case_cover = request.form['case-cover']
    bug_cover = request.form['bug-cover']
    error = None
    if not case_id:
        error = 'case-id is required.'
    if validate == "":
        error = 'validate is required.'
    if error is None:
        db.session.add(Cases(case_id=case_id, predict=predict, validate=validate, case_date=datetime.datetime.strptime(case_date, '%Y-%m-%d'), status=status, case_cover=case_cover, bug_cover=bug_cover, user_id=1, component=current_user.last_component))
        db.session.commit()
        # session.modified = True
        session['new_case_id_list'].remove(case_id)
        return ("", 204)
        # return (request.path, 204)
    flash(error)
    return redirect(url_for('index'))


def get_search_date(component):
    component = Component.query.filter_by(component=component).first()
    return str(component.search_date)


def update_search_date(component, search_date):
    Component.query.filter_by(component=component).update({'search_date':search_date})
    db.session.commit()
