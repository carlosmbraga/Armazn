from flask import render_template
from app import app, db
from flask import Flask, request, redirect, url_for, session, g, flash, \
     render_template
from app.models import forms
from app.models import tables

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=('GET', 'POST'))
def registro():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Registro realizado com sucesso!", "success")
        forms.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('login'))
    return render_template('registro.html', form=form)
	
@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = tables.User.get(tables.User.email == form.email.data)
        except:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('error.html'), 404	



	
