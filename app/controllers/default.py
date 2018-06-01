import os
from app import app, db, lm
from flask import Flask, request, redirect, url_for, session, render_template, send_from_directory, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from app.models import forms
from app.models import tables
from app.models.tables import User
from flask_autoindex import AutoIndex, RootDirectory

ALLOWED_EXTENSIONS = set(['txt', 'png'])
UPLOAD_FOLDER = 'app/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
files_index = AutoIndex(app, os.path.curdir +
                        '/' + app.config['UPLOAD_FOLDER'], add_url_rules=False)

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
        username = form.username.data,
        email = form.email.data,
        password = form.password.data
        if username and email and password:
            u = User(username, password, email)
            db.session.add(u)
            db.session.commit()
            flash("Usuario registrado com sucesso", "success")

            os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], str(u.username)))
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
        if user and user.password == form.password.data:
            login_user(user)
            app.config['UPLOAD_FOLDER'] += user.username
            files_index.rootdir = RootDirectory(os.path.curdir +
                                                    '/' + app.config['UPLOAD_FOLDER'], autoindex=files_index)
            return redirect(url_for('home'))
        else:
            flash("Your email or password doesn't match!", "error")
    else:
        return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    app.config['UPLOAD_FOLDER'] = 'app/uploads/'
    return redirect(url_for('index'))

# abaixo, /uploads e /uploads/<filename>: tratam do upload e armazenamento dos arquivos


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_engine/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/home')
def home():
    if not os.listdir(app.config['UPLOAD_FOLDER']):
        flash("Diretório pessoal vazio!")
    return autoindex()


@app.route('/upload_engine', methods=['GET', 'POST'])
def upload_engine():
    if request.method == 'POST':

        if 'text' in request.form and 'filename' in request.form:
            newText = request.form['text']
            newFilename = request.form['filename']
            filename = secure_filename(newFilename)
            file = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'w')
            file.write(newText)
            return redirect(url_for('home', filename=filename))

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('home', filename=filename))

    return render_template('upload_engine.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


@app.route('/arquivos')
@app.route('/arquivos/<path:path>')
def autoindex(path='.'):
    return files_index.render_autoindex(path)
