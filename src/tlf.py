#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, make_response
from database import *
from werkzeug.utils import secure_filename
import csv
import StringIO
import os

blu_tlf = Blueprint('tlf', __name__, template_folder='templates')

@blu_tlf.route("/insert", methods=['POST'])
def insert():
    tlf = request.form['tlf']
    nom = request.form['nom']

    if (len(tlf) == 0) or (len(nom) == 0):
        flash("S'han de completar tots els camps", "error")
        return redirect(url_for('admin'))

    if (len(tlf) > 9):
        flash("Telèfon massa llarg", "error")
        return redirect(url_for('admin'))

    if not tlf.isdigit():
        flash("El telèfon només pot contenir digits", "error")
        return redirect(url_for('admin'))        

    if checkRepeatTLF(tlf):
        flash("Aquest telèfon ja existeix", "error")
        return redirect(url_for('admin'))
                        
    if checkRepeatNom(nom):
        flash("Aquest nom ja existeix", "error")
        return redirect(url_for('admin'))

    insertTLF(formatTLF(tlf), formatNom(nom))
    flash("Telèfon afegit correctament")
    return redirect(url_for('admin'))

@blu_tlf.route("/get", methods=['GET'])
def get():
    si = StringIO.StringIO()
    cw = csv.writer(si)
    cw.writerows(exportContacts())
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in set(['csv'])

@blu_tlf.route("/upload", methods=['POST'])
def upload():
     if 'file' not in request.files:
         flash("No has pujat cap fitxer", "error")
         return redirect(url_for('admin'))

     f = request.files['file']

     if not allowed_file(f.filename):
         flash("Tipus de fitxer no valid", "error")
         return redirect(url_for('admin'))

     if f.filename == '':
         flash("Fitxer buit", "error")
         return redirect(url_for('admin'))

     filename = secure_filename(f.filename)
     path_w_fn = os.path.join('./uploads', filename)
     f.save(path_w_fn)

     if importContacts(path_w_fn):
         flash("Dades importades correctament")
         os.remove(path_w_fn)
         return redirect(url_for('admin'))
     else:
         flash("TLF massa llarg o valors repetits", "error")
         os.remove(path_w_fn)
         return redirect(url_for('admin'))

@blu_tlf.route("/update", methods=['POST'])
def update():
    nou_tlf = request.form['nou_tlf']
    nou_nom = request.form['nou_nom']
    old_tlf = request.form['old_tlf']

    if len(old_tlf) == 0:
        flash("Escriu quin telèfon vols modificar", "error")
        return redirect(url_for('admin'))

    if not checkRepeatTLF(old_tlf):
        flash("El telèfon a modificar no existeix", "error")
        return redirect(url_for('admin'))
    
    if not nou_tlf.isdigit():
        flash("El telèfon només pot contenir digits", "error")
        return redirect(url_for('admin'))
    
    if checkRepeatTLF(nou_tlf):
        flash("Aquest telèfon ja existeix", "error")
        return redirect(url_for('admin'))
                        
    if checkRepeatNom(nou_nom):
        flash("Aquest nom ja existeix", "error")
        return redirect(url_for('admin'))

    if (len(nou_nom) == 0) and (len(nou_tlf) == 0):
        flash("No has escrit res per modificar", "error")
        return redirect(url_for('admin'))

    if len(nou_nom) == 0:
        # Només update de tlf
        updateTLF(old_tlf, nou_tlf)
        flash("Contacte modificat")
        return redirect(url_for('admin'))
        
    if len(nou_tlf) == 0:
        # Només update de nom
        updateNom(old_tlf, nou_nom)
        flash("Contacte modificat")
        return redirect(url_for('admin'))

    updateNom(old_tlf, nou_nom)
    updateTLF(old_tlf, nou_tlf)
    flash("Contacte modificat")
    return redirect(url_for('admin'))

@blu_tlf.route("/delete", methods=['POST'])
def delete():
    delete_tlf = request.form['delete_tlf']
    
    if checkRepeatTLF(delete_tlf):
        deleteTLF(delete_tlf)
        return "El contacte amb numero %s s'ha eliminat" % (delete_tlf,)
    else:
        return "El contacte %s ja esta eliminar o error" % (delete_tlf,)

