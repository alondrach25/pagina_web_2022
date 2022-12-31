from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def inicio():
    if request.method == 'POST':
        nota = request.form.get('note')

        if len(nota) < 1:
           flash('¡La nota es muy corta!', category='error')
        else:
            nueva_nota = Note(data=nota, user_id=current_user.id)
            db.session.add(nueva_nota)
            db.session.commit()
            flash('¡Nota registrada!', category='success')

    return render_template("inicio.html", user=current_user)

@views.route('/bienvenida')
def bienvenida():
    return render_template("bienvenida.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def borra_nota():
    note=json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id :
           db.session.delete(note)
           db.session.commit()
           
    return jsonify({}) 

