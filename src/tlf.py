#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from database import *

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

    if not checkRepeatTLF(tlf):
        flash("Aquest telèfon ja existeix", "error")
        return redirect(url_for('admin'))
                        
    if not checkRepeatNom(nom):
        flash("Aquest nom ja existeix", "error")
        return redirect(url_for('admin'))

    insertTLF(formatTLF(tlf), formatNom(nom))
    flash("Telèfon afegit correctament")
    return redirect(url_for('admin'))

@blu_tlf.route("/get", methods=['GET'])
def getAllTLFView():
    return jsonify(getAllTLFDict())

@blu_tlf.route("/update", methods=['POST'])
def update():
    nou_tlf = request.form['nou_tlf']
    nou_nom = request.form['nou_nom']
    old_tlf = request.form['old_tlf']
    old_nom = request.form['old_nom']

    if not nou_tlf.isdigit():
        flash("El telèfon només pot contenir digits", "error")
        return render_template('main.html', nom = old_nom, title = "Buscador", tlf = old_tlf, admin = True)
    
    if not checkRepeatTLF(nou_tlf):
        flash("Aquest telèfon ja existeix", "error")
        return render_template('main.html', nom = old_nom, title = "Buscador", tlf = old_tlf, admin = True)
                        
    if not checkRepeatNom(nou_nom):
        flash("Aquest nom ja existeix", "error")
        return render_template('main.html', nom = old_nom, title = "Buscador", tlf = old_tlf, admin = True)

    if (len(nou_nom) == 0) and (len(nou_tlf) == 0):
        flash("No has escrit res per modificar", "error")
        return render_template('main.html', nom = old_nom, title = "Buscador", tlf = old_tlf, admin = True)

    if len(nou_nom) == 0:
        updateTLF(old_nom, nou_tlf)
        flash("Contacte modificat")
        return render_template('main.html', nom = old_nom, title = "Buscador", tlf = nou_tlf, admin = True)
        
    if len(nou_tlf) == 0:
        updateNom(old_tlf, nou_nom)
        flash("Contacte modificat")
        return render_template('main.html', nom = nou_nom, title = "Buscador", tlf = old_tlf, admin = True)

    updateNom(old_tlf, nou_nom)
    updateTLF(old_nom, nou_tlf)
    flash("Contacte modificat")
    return render_template('main.html', nom = nou_nom, title = "Buscador", tlf = nou_tlf, admin = True)

@blu_tlf.route("/delete", methods=['POST'])
def delete():
    delete_tlf = request.form['delete_tlf']
    delete_nom = request.form['delete_nom']
    
    deleteTLF(formatTLF(delete_tlf))

    flash("El contacte de: %s s'ha eliminat" % (delete_nom, ))
    return redirect(url_for('admin'))

