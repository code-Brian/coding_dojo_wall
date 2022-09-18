from flask_app import app
from flask_app.models import user, post, comment
from flask import Flask, request, redirect, session, render_template

@app.route('/comment/create/<int:id>', methods=['POST'])
def f_comment_create(id):
    if not comment.Comment.validate_comment(request.form):
        return redirect('/wall')

    data = {
        'user_id' : request.form.get('user_id'),
        'post_id' : id,
        'content' : request.form.get('content')
    }

    comment.Comment.create(data)

    return redirect('/wall')