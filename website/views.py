
from typing import no_type_check

from flask import Blueprint, abort, flash, jsonify, redirect, render_template,request, url_for
from flask_login import login_required,current_user
import json
from  .models import Note, User 
from . import db

views = Blueprint('views', __name__)
@views.route('/',methods=['GET','POST'])
@login_required

def home():
    if request.method=='POST':
        note=request.form.get('note')
        
        if len(note)<1:
            flash('Note is too short',category='error')
        else:
            new_note=Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!',category='success')
            print("Adding note:", note)
        return redirect(url_for('views.home'))
    return render_template('home.html',user=current_user)
#create admin panel route
@views.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        abort(403)  # Forbidden

    users = User.query.all()
    notes = Note.query.all()

    return render_template("admin.html", users=users, notes=notes)
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = request.get_json()
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            print("Deleting note:", note)
           
    return jsonify({})
 