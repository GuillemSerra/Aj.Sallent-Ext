#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, make_response
from database import *
import PyICU

blu_busc = Blueprint('buscador', __name__, template_folder='templates')

def order_tlfs(db):
    OG_keys = {}
    for element in db.keys():
        OG_keys[int(element)] = element
        
    sorted_tlfs = sorted(map(int, db.keys()))
    
    ordered_list = []
    for tlf in sorted_tlfs:
        params = db[OG_keys[tlf]]
        ordered_list += [{'tlf': OG_keys[tlf], 'nom': params[0], \
                          'dept': params[1], 'tlf_dir': params[2], \
                          'email': params[3], 'area': params[4]}]

    return ordered_list
    
@blu_busc.route('/tlf/<user>', methods = ['POST'])
def tlf(user):
    busc_value_dirty = request.form["buscador_tlf"]
    
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
          
    ordered_list = order_tlfs(db)

    if user == 'main':
        admin = False
    else:
        admin = True

    # Si nomes hi ha un resultat, contacte.html
    if len(ordered_list) == 1:
        contacte = ordered_list[0]
        return redirect(url_for('tlf.contacte', contacte=contacte['nom'], user=user))
    else:
        return render_template('main.html', \
                               title = "Buscador", \
                               resultDict = ordered_list, \
                               admin = admin)

@blu_busc.route('/dept/<user>', methods = ['POST'])
def dept(user):
    busc_value = request.form["buscador_dept"]
    
    if (len(busc_value) == 0):
        flash("Escriu departament a buscar", "error")
        return redirect(url_for(user))

    busc_value_clean = formatNom(busc_value)
    db = getDepartamentDict(busc_value_clean)
    if len(db) == 0:
        flash("Aquest departament no existeix", "error")
        return redirect(url_for(user))
          
    ordered_list = order_tlfs(db)
    depts = []
    for element in ordered_list:
        if element['dept'] not in depts:
            depts += [element['dept']]

    if user == 'main':
        admin = False
    else:
        admin = True

    # Si nomes hi ha un departament, departament.html
    if len(depts) == 1:
        contacte = ordered_list[0]
        return redirect(url_for('tlf.dept', dept=contacte['dept'], user=user))
    else:
        return render_template('main.html', \
                               title = "Buscador", \
                               resultDict = ordered_list, \
                               admin = admin)
    
@blu_busc.route("/autocomplete_tlf", methods=['GET'])
def autocomplete_tlf():
    db = getAllTLFDict()
    
    OG_keys = {}
    for element in db.keys():
        OG_keys[int(element)] = element
        
    sorted_tlfs = sorted(map(int, db.keys()))
    
    sorted_db = []
    for tlf in sorted_tlfs:
        sorted_db += [OG_keys[tlf] + ' - ' + db[OG_keys[tlf]][0]]
    
    return jsonify(json_list = sorted_db)

@blu_busc.route("/autocomplete_dept", methods=['GET'])
def autocomplete_dept():
    collator = PyICU.Collator.createInstance(PyICU.Locale('es_ES.UTF-8'))
    
    depts = getDepartaments()
    sorted_depts = sorted(depts, key=collator.getSortKey)
    
    return jsonify(json_list = sorted_depts)
