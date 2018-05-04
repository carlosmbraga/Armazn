from flask import render_template
from app import app, db, lm
from flask import Flask, request, redirect, url_for, session, g, flash, \
     render_template
from flask_login import login_user, logout_user	 
from app.models import forms
from app.models import tables
from app.models.tables import User


@lm.user_loader
def load_user(id):
	return User.query.filter_by(id=id).first()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=('GET', 'POST'))
def registro():
    form = forms.RegisterForm()
    if request.method == "POST":
        username=form.username.data,
        email=form.email.data,
        password=form.password.data
        if username and email and password:
            u = User(username, password, email)
            db.session.add(u)
            db.session.commit()
            flash("Usuario registrado com sucesso", "success")
            return redirect(url_for('login'))
        else:
            flash("Falha no registro", "error")
    else:
        return render_template('registro.html', form=form)
	
@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if  user and user.password == form.password.data:
                login_user(user)
                flash("Olá " + user.username, "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    else:
        return render_template('login.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))
	
	
@app.errorhandler(404)
def page_not_found(e):
  return render_template('error.html'), 404	



	
