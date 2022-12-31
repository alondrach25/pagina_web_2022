from flask import Blueprint, render_template, request, flash, redirect, url_for 
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/entrar', methods=['GET','POST'])
def entrar():
    if request.method == 'POST':
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')

        usuario = User.query.filter_by(email=email).first()
        if usuario:
            if check_password_hash(usuario.contraseña, contraseña):
                flash('¡Ha iniciado sesión exitosamente!', category='success')
                login_user(usuario, remember=True)
                return redirect(url_for('views.inicio'))
            else:
                flash('Contraseña incorrecta, inténtelo de nuevo.', category='error')    
        else:
            flash('Dirección de correo electrónico no registrado.', category='error')
    return render_template("entrar.html", user=current_user)

@auth.route('/salir')
@login_required
def salir():
    logout_user()
    return redirect(url_for('auth.entrar'))

@auth.route('/registrarse', methods=['GET','POST'])
def registrarse():
    if request.method == 'POST':
        email = request.form.get('email')
        primerNombre = request.form.get('primerNombre')
        contraseña1 = request.form.get('contraseña1')
        contraseña2 = request.form.get('contraseña2')
        
        usuario = User.query.filter_by(email=email).first()
        if usuario:
            flash('Esta dirección de correo electrónico ya se encuentra registrado.', category='error')
        elif len(email) < 4:
            flash('La dirección de correo electrónico debería tener más de 3 caracteres.', category='error')
        elif len(primerNombre) < 2:
            flash('El parámetro "Primer Nombre" debería tener más de 1 caracter.', category='error')
        elif contraseña1 != contraseña2:
            flash('Las contraseñas introducidas no coinciden.', category='error')
        elif len(contraseña1) < 7:
            flash('La contraseña debería tener al menos 7 caracteres.', category='error')
        else:
            nuevo_usuario = User(email=email, primer_nombre = primerNombre, contraseña = generate_password_hash(contraseña1,method='sha256'))
            db.session.add(nuevo_usuario)
            db.session.commit()
            login_user(usuario, remember=True)
            flash('¡Cuenta creada exitosamente!', category='success')
            return redirect(url_for('views.inicio'))

             
    return render_template("registrarse.html", user=current_user)
