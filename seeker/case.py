from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from seeker.auth import login_required
from seeker.db import get_db
from seeker.serverside_table import serverside_table
from seeker.logger import logger
from seeker.scraper.cp_case_scraper import CPCaseScraper

import datetime

bp = Blueprint('case', __name__)


@bp.route('/')
def show_case():
    return render_template('case/case_base.html')


@bp.route("/show_his_table", methods=('GET', 'POST'))
def show_his_table():
    show_data = serverside_table(request).get_table()
    logger.debug("show_his_table: %s" % show_data)
    return jsonify(show_data)


@bp.route("/show_new_table", methods=('GET', 'POST'))
def show_new_table():
    case_dict = {}
    search_date = get_search_date()
    scraper = CPCaseScraper()
    case_list = scraper.scrape_cases_via_date(search_date)

    # logger.debug("before case_list: %s" % case_list)
    db = get_db()
    min_date = ""
    for case in case_list:
        if db.execute('SELECT * FROM cases WHERE case_id=%s' % (case["case_id"])).fetchone() is not None:
            case_list.remove(case)
        else:
            if min_date == "" or datetime.datetime.strptime(min_date, '%Y-%m-%d') > datetime.datetime.strptime(case["case_date"], '%Y-%m-%d'):
                min_date = case["case_date"]
    if datetime.datetime.strptime(min_date, '%Y-%m-%d') > datetime.datetime.strptime(search_date, '%Y-%m-%d'):
        logger.debug("update search date to: %s" % min_date)
        update_search_date("2018-8-5")

    # logger.debug("after case_list: %s" % case_list)
    case_dict['data'] = case_list
    logger.debug("show_new_table: %s" % case_dict)
    return jsonify(case_dict)


def get_search_date():
    sql_search_date = 'SELECT search_date FROM cases_search_date WHERE component = "virt-who"'
    search_date = get_db().execute(sql_search_date).fetchone()[0]
    logger.debug("search_date: %s" % search_date)
    return search_date


def update_search_date(search_date):
    db = get_db()
    db.execute(
        'UPDATE cases_search_date SET search_date="%s" WHERE component = "virt-who"' % search_date
    )
    db.commit()


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


@bp.route("/save_case", methods=('GET', 'POST'))
def save_case():
    case_id = request.form['case-id']
    predict = request.form['predict']
    validate = request.form['validate']
    case_date = request.form['case-date']
    case_cover = request.form['case-cover']
    bug_cover = request.form['bug-cover']
    error = None
    if not case_id:
        error = 'case-id is required.'
    if validate == "":
        error = 'validate is required.'
    if error is None:
        db = get_db()
        db.execute(
            'INSERT INTO cases (case_id,predict,validate,case_date,case_cover,bug_cover,author_id)'
            'VALUES (?, ?, ?,?,?,?,?)',
            (case_id, predict, validate, case_date, case_cover, bug_cover, "1")
        )
        db.commit()
        logger.debug("save_case")
        return ('', 204)
    flash(error)
    return render_template('case/case_base.html')


@bp.route("/update_case", methods=('GET', 'POST'))
def update_case():
    case_id = request.form['case-id']
    validate = request.form['validate']
    case_cover = request.form['case-cover']
    bug_cover = request.form['bug-cover']
    error = None
    if not case_id:
        error = 'case-id is required.'
#     if validate:
#         error = 'validate is required.'
    if error is None:
        db = get_db()
        db.execute(
            'UPDATE cases SET validate="%s",case_cover="%s",bug_cover="%s" WHERE case_id="%s"' % (validate, case_cover, bug_cover, case_id)
        )
        db.commit()
        logger.debug("update_case")
        return ('', 204)
    flash(error)
    return render_template('case/case_base.html')
#     if request.method == 'POST':
#         data = request.get_json()
#         case_id = data.get('case_id')
#         case_details = get_case_details(case_id)
#     return jsonify({"case_details":case_details})


def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ? WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
