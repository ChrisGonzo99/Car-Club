from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user

@app.route('/')
def register_login():
    return render_template("reg_login.html")

@app.route('/user/register', methods = ['POST'])
def register_user():
    if user.User.register_user(request.form):
        return redirect('/home')
    return redirect('/')

@app.route('/login', methods = ['POST'])
def login():
    if user.User.login_user(request.form):
        return redirect('/home')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
