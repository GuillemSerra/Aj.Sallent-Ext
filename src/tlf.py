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
    dept = request.form['dept']
    tlf_dir = request.form['tlf_dir']
    email = request.form['email']
    area = request.form['area']

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

    insertTLF(formatTLF(tlf), formatNom(nom), \
              formatNom(dept), formatTLF(tlf_dir), \
              formatNom(email), formatNom(area))
    
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
    old_tlf = request.form['old_tlf']
    nou_tlf = request.form['nou_tlf']
    nou_nom = request.form['nou_nom']
    nou_dept = request.form['nou_dept']
    nou_tlf_dir = request.form['nou_tlf_dir']
    nou_email = request.form['nou_email']
    nou_area = request.form['nou_area']
    
    old_tlf = request.form['old_tlf']
    old_tlf = request.form['old_tlf']
    old_nom = request.form['old_nom']
    old_dept = request.form['old_dept']
    old_tlf_dir = request.form['old_tlf_dir']
    old_email = request.form['old_email']
    old_area = request.form['old_area']

    if not nou_tlf.isdigit():
        flash("El telèfon només pot contenir digits", "error")
        return redirect(url_for('admin'))

    if (len(nou_nom) == 0) or (len(nou_tlf) == 0):
        flash("És necessari un nom i telèfon", "error")
        return redirect(url_for('admin'))
    
    deleteTLF(formatTLF(old_tlf))
    
    if checkRepeatTLF(nou_tlf):
        insertTLF(formatTLF(old_tlf), formatNom(old_nom), \
                  formatNom(old_dept), formatTLF(old_tlf_dir), \
                  formatNom(old_email), formatNom(old_area))
        flash("Aquest telèfon ja existeix", "error")
        return redirect(url_for('admin'))
                        
    if checkRepeatNom(nou_nom):
        insertTLF(formatTLF(old_tlf), formatNom(old_nom), \
                  formatNom(old_dept), formatTLF(old_tlf_dir), \
                  formatNom(old_email), formatNom(old_area))
        flash("Aquest nom ja existeix", "error")
        return redirect(url_for('admin'))

    insertTLF(formatTLF(nou_tlf), formatNom(nou_nom), \
              formatNom(nou_dept), formatTLF(nou_tlf_dir), \
              formatNom(nou_email), formatNom(nou_area))
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

@blu_tlf.route("/contacte/<contacte>/", methods=['GET'])
@blu_tlf.route("/contacte/<contacte>/<user>", methods=['GET'])
def contacte(contacte, user='main'):
    contactes = getContacte(contacte)
    
    if user == 'main':
        admin = False
    else:
        admin = True
        
    return render_template('contacte.html', \
                           admin = admin, \
                           title=contacte, \
                           tlf=contactes[0], nom=contactes[1], \
                           dept=contactes[2], tlf_dir=contactes[3], \
                           email=contactes[4], area=contactes[5])

@blu_tlf.route("/dept/<dept>/", methods=['GET'])
@blu_tlf.route("/dept/<dept>/<user>", methods=['GET'])
def dept(dept, user='main'):
    db = getDepartamentDict(dept)
    sorted_tlfs = sorted(map(int, db.keys()))
    
    ordered_list = []
    for tlf in map(str, sorted_tlfs):
        ordered_list += [{'tlf': tlf, 'nom': db[tlf][0], \
                          'dept': db[tlf][1], 'tlf_dir': db[tlf][2], \
                          'email': db[tlf][3], 'area': db[tlf][4]}]
    if user == 'main':
        admin = False
    else:
        admin = True
        
    return render_template('departament.html', \
                           title = dept, \
                           resultDict = ordered_list, \
                           admin = admin)
