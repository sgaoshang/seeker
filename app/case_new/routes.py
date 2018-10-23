from flask import render_template, flash, redirect, url_for, request, current_app, session, jsonify
from flask_babel import _, get_locale
from flask_login import current_user, login_required
from app import db
from app.models import Cases
from app.models import Component
from app.case_new.scraper.cp_case_scraper import CPCaseScraper
from math import ceil
from datetime import datetime

from app import celery

from app.case_new import bp


@bp.before_request
def before_request():
    current_app.logger.info("run: bp.before_request")
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
    scraper = CPCaseScraper()
    search_date = get_search_date(component)
    case_id_list, update_date = scraper.scrape_cases_id_via_date(component, search_date)
    if update_date != "" and datetime.strptime(update_date, '%Y-%m-%d') > datetime.strptime(search_date, '%Y-%m-%d'):
        update_search_date(component, datetime.strptime(update_date, '%Y-%m-%d'))
    return case_id_list


@bp.route('/case', methods=['GET', 'POST'])
@login_required
def case():
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
        # scraper = CPCaseScraper()
        # for case_id in new_case_id_list[start:start + per_page]:
        #    cases.append(scraper.scrape_case_dict(component, case_id))
    # for key in session:
    #    print key
    if 'new_case_content_list' in session:
        next_url = url_for('case_new.case', page=page + 1) \
            if page < pages else None
        prev_url = url_for('case_new.case', page=page - 1) \
            if page > 1 else None
        cases = session['new_case_content_list']
        session.pop('new_case_content_list')
    else:
        task = task_get_case_content.delay(component, new_case_id_list[start:start + per_page])  # .apply_async()
        return jsonify({}), 202, {'Location': url_for('case_new.status', task_id=task.id)}
    return render_template('case_new/case.html', title=_('New Case'), cases=cases, next_url=next_url, prev_url=prev_url)


@celery.task(bind=True)
def task_get_case_content(self, component, case_id_list):
    scraper = CPCaseScraper()
    total = len(case_id_list)
    cases_content_list = []
    for index, case_id in enumerate(case_id_list):
        self.update_state(state='PROGRESS', meta={'current': index, 'total': total, 'status': "Loading Case %s ..." % case_id})
        cases_content_list.append(scraper.scrape_case_dict(component, case_id))
    return {'current': 100, 'total': 100, 'status': 'Completed', 'result': cases_content_list}


@bp.route('/status/<task_id>')
def status(task_id):
    task = task_get_case_content.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current'),
            'total': task.info.get('total'),
            'status': task.info.get('status')
        }
        if 'result' in task.info:
            cases_content_list = task.info['result']
            if 'new_case_content_list' in session:
                session.pop('new_case_content_list')
            session['new_case_content_list'] = cases_content_list
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


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
        db.session.add(Cases(case_id=case_id, predict=predict, validate=validate, case_date=datetime.strptime(case_date, '%Y-%m-%d'), status=status, case_cover=case_cover, bug_cover=bug_cover, user_id=1, component=current_user.last_component))
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
