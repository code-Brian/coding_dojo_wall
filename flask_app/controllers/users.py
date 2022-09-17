from flask_app import app
from flask_app.models import user
from flask import Flask, request, redirect, session, render_template

@app.route('/')
def r_login():
    print('rendering the login page...')

    return render_template('login.html')