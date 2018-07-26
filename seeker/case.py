from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from seeker.auth import login_required
from seeker.db import get_db
from seeker.serverside_table import serverside_table
from seeker.serverside_table_scrape import serverside_table_scrape
from seeker.logger import logger
from seeker.scraper.cp_case_scraper import CPCaseScraper

bp = Blueprint('case', __name__)


@bp.route('/')
def show_case():
    return render_template('case/case_base.html')


@bp.route('/show_his')
def show_his():
    return render_template('case/case_his.html')

 
@bp.route('/show_new')
def show_new():
    return render_template('case/case_new.html')


@bp.route("/show_his_table", methods=('GET',))
def show_his_table():
    show_data = serverside_table(request).get_table()
    logger.debug("show_his_table: %s" % show_data)
    return jsonify(show_data)


@bp.route("/show_new_table", methods=('GET',))
def show_new_table():
    show_data = serverside_table_scrape(request).get_table()
    logger.debug("show_new_table: %s" % show_data)
    return jsonify(show_data)


@bp.route("/show_case_details", methods=('GET', 'POST'))
def show_case_details():
    if request.method == 'POST':
        data = request.get_json()
        case_id = data.get('case_id')
        case_details = get_case_details(case_id)
    return jsonify({"case_details":case_details})
#     return render_template('case/case_details.html')


def get_case_details(case_id):
    scraper = CPCaseScraper()
    return scraper.scrape_case_messages(case_id)


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
