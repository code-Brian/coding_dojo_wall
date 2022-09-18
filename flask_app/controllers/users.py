from flask_app import app
from flask_app.models import user, post
from flask import Flask, request, redirect, session, render_template,flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# login/register home page
@app.route('/')
def r_login():
    print('rendering the login page...')

    return render_template('login.html')

# create user form route
@app.route('/user/create', methods=['POST'])
def f_user_create():
    parse = user.User.parse_user_registration(request.form)

    if not user.User.validate_registration(request.form):
        session['first_name'] = request.form.get('first_name')
        session['last_name'] = request.form.get('last_name')
        session['email'] = request.form.get('email')

        print(parse)

        print('invalid form data')
        return redirect('/')

    session.clear()

    user_id = user.User.create(parse)

    session['user_id'] = user_id
    session['user_first_name'] = request.form.get('first_name').capitalize()
    session['user_last_name'] = request.form.get('last_name').capitalize()

    print('redirecting to the wall...')
    return redirect('/wall')

# login user form route
@app.route('/user/login', methods=['POST'])
def f_user_login():
    print('Attempting to login...')

    data = {
        'email' : request.form.get('email')
    }

    user_match = user.User.get_user_by_email(data)

    if not user_match:
        flash(u'Invalid Email/Password', 'login')
        return redirect('/')
    
    if not bcrypt.check_password_hash(user_match.password, request.form.get('password')):
        flash(u'Invalid Email/Password', 'login')
        return redirect('/')

    session['user_id'] = user_match.id
    session['user_first_name'] = user_match.first_name.capitalize()
    session['user_last_name'] = user_match.last_name.capitalize()

    return redirect('/wall')

@app.route('/logout')
def d_logout():
    print('logging out and redirect to login page...')
    session.clear()
    return redirect('/')