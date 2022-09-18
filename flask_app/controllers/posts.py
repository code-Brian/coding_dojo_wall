from flask_app import app
from flask_app.models import user, post
from flask import Flask, request, redirect, session, render_template

@app.route('/wall')
def r_wall():
    print('rendering wall page...')

    return render_template('wall.html', posts=post.Post.get_all_with_creator_comments())

@app.route('/post/create', methods=['POST'])
def f_post_create():
    if not post.Post.validate_post(request.form):
        return redirect('/wall')

    data = post.Post.parse_data(request.form)

    post.Post.create(data)

    return redirect('/wall')