#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, make_response
from database import *
import PyICU

blu_busc = Blueprint('buscador', __name__, template_folder='templates')

@blu_busc.route('/lel/<man>', methods = ['GET'])
def test(man):
    return man
    
@blu_busc.route('/tlf/<user>', methods = ['POST'])
def tlf(user):
    busc_value_dirty = request.form["buscador"]
    
    if (len(busc_value_dirty) == 0):
        flash("Escriu telèfon o nom a buscar", "error")
        return redirect(url_for(user))
    
    busc_value_clean = busc_value_dirty.split('-')[0]

    if (formatTLF(busc_value_clean).isdigit()):
        # S'ha buscat un telefon
        busc_value_clean = formatTLF(busc_value_clean)
        db = getAllDBLike(tlf=busc_value_clean)
        if len(db) == 0:
            flash("Aquest telèfon no existeix", "error")
            return redirect(url_for(user))
    else:
        # S'ha buscat un nom
        busc_value_clean = formatNom(busc_value_clean)
        db = getAllDBLike(nom=busc_value_clean)
        if len(db) == 0:
            flash("Aquest nom no existeix", "error")
            return redirect(url_for(user))
          
    sorted_tlfs = sorted(map(int, db.keys()))

    ordered_list = []
    for tlf in map(str, sorted_tlfs):
        ordered_list += [{'tlf': tlf, 'nom': db[tlf][0], \
                          'dept': db[tlf][1], 'tlf_dir': db[tlf][2], \
                          'email': db[tlf][3]}]

    if user == 'main':
        admin = False
    else:
        admin = True

    # Si nomes hi ha un resultat, contacte.html
    if len(ordered_list) == 1:
        contacte = ordered_list[0]
        return redirect(url_for('tlf.contacte', user=contacte['nom']))
    else:
        return render_template('main.html', \
                               title = "Buscador", \
                               resultDict = ordered_list, \
                               admin = admin)

@blu_busc.route('/dept/<user>', methods = ['POST'])
def dept(user):
    busc_value = request.form["buscador"]
    
    if (len(busc_value) == 0):
        flash("Escriu departament a buscar", "error")
        return redirect(url_for(user))

    busc_value_clean = formatNom(busc_value)
    db = getAllDBLike(dept=busc_value_clean)
    if len(db) == 0:
        flash("Aquest departament no existeix", "error")
        return redirect(url_for(user))
          
    sorted_tlfs = sorted(map(int, db.keys()))

    ordered_list = []
    for tlf in map(str, sorted_tlfs):
        ordered_list += [{'tlf': tlf, 'nom': db[tlf][0], \
                          'dept': db[tlf][1], 'tlf_dir': db[tlf][2], \
                          'email': db[tlf][3]}]

    if user == 'main':
        admin = False
    else:
        admin = True

    # Si nomes hi ha un departament, departament.html
    if len(ordered_list) == 1:
        contacte = ordered_list[0]
        return redirect(url_for('tlf.departament', dept=contacte['dept']))
    else:
        return render_template('main.html', \
                               title = "Buscador", \
                               resultDict = ordered_list, \
                               admin = admin)
    
@blu_busc.route("/autocomplete_tlf", methods=['GET'])
def autocomplete_tlf():
    db = getAllTLFDict()
    sorted_tlfs = sorted(map(int, db.keys()))
    
    sorted_db = []
    for tlf in map(str, sorted_tlfs):
        sorted_db += [tlf + ' - ' + db[tlf][0]]
    
    return jsonify(json_list = sorted_db)

@blu_busc.route("/autocomplete_dept", methods=['GET'])
def autocomplete_dept():
    collator = PyICU.Collator.createInstance(PyICU.Locale('es_ES.UTF-8'))
    
    depts = getDepartaments()
    sorted_depts = sorted(depts, key=collator.getSortKey)
    
    return jsonify(json_list = sorted_depts)
