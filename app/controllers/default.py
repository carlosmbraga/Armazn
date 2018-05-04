from flask import render_template
from app import app, db, lm
from flask import Flask, request, redirect, url_for, session, g, flash, \
<<<<<<< HEAD
     render_template
from flask_login import login_user, logout_user	 
||||||| merged common ancestors
     render_template
=======
     render_template, send_from_directory
from werkzeug.utils import secure_filename
>>>>>>> e20e1dead3d92c65b2e09f4343c7eaaf8d20b145
from app.models import forms
from app.models import tables
<<<<<<< HEAD
from app.models.tables import User


@lm.user_loader
def load_user(id):
	return User.query.filter_by(id=id).first()
||||||| merged common ancestors
=======
import os


UPLOAD_FOLDER = 'app/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'png'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

>>>>>>> e20e1dead3d92c65b2e09f4343c7eaaf8d20b145

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=('GET', 'POST'))
def registro():
    form = forms.RegisterForm()
<<<<<<< HEAD
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
	
||||||| merged common ancestors
    if form.validate_on_submit():
        flash("Registro realizado com sucesso!", "success")
        forms.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('login'))
    return render_template('registro.html', form=form)
	
=======
    if form.validate_on_submit():
        flash("Registro realizado com sucesso!", "success")
        forms.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('login'))
    return render_template('registro.html', form=form)

>>>>>>> e20e1dead3d92c65b2e09f4343c7eaaf8d20b145
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

<<<<<<< HEAD
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))
	
	
@app.errorhandler(404)
def page_not_found(e):
  return render_template('error.html'), 404	
||||||| merged common ancestors
@app.errorhandler(404)
def page_not_found(e):
  return render_template('error.html'), 404	
=======
# abaixo, /uploads e /uploads/<filename>: tratam do upload e armazenamento dos arquivos
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
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
            return redirect(url_for('uploaded_file', filename=filename))

    return render_template('upload.html')
>>>>>>> e20e1dead3d92c65b2e09f4343c7eaaf8d20b145

# precisa de melhoria do layout dessas paginas de upload, mas o funcionamento está ok
# (eles salvam na pasta uploads que eu criei no diretório do app) e
# precisa tbm melhorar o tratamento de erros (nos if's), caso o arquivo enviado
# não seja da extensão permitida ou caso não haja arquivo enviado
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# error handling
@app.errorhandler(404)
def page_not_found(e):
  return render_template('error.html'), 404
