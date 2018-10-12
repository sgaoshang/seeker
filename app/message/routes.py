from flask import render_template, flash, redirect, url_for, request, current_app, jsonify, g
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.message.forms import PostForm, SearchForm
from app.models import Post
from app.message.translate import translate

from app.message import bp


@bp.before_app_request
def before_app_request():
    if current_user.is_authenticated:
        if current_app.elasticsearch != None: 
        # do not show search form when elasticsearch did not configured
            g.search_form = SearchForm()


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('message.new'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('message.new', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('message.new', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('message/message.html', title=_('New Message'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('message.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('message.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('message/message.html', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    result = {'text': translate(request.form['text'],
                      request.form['source_language'],
                      request.form['dest_language'])}
    return jsonify(result)


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('message.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('message.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('message.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('message/search.html', title=_('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)
