#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from tlf import blu_tlf
from database import *
import PyICU

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('SERRA_SETTINGS', silent=True)
app.secret_key = os.environ["SESSION_SECRET_KEY"]
app.register_blueprint(blu_tlf, url_prefix='/tlf')
app.config['JSON_AS_ASCII'] = False # jsonify utf-8

@app.route('/', methods = ["GET"])
def main():
    db = getAllTLFDict()
    sorted_tlfs = sorted(map(int, db.keys()))
    
    ordered_list = []
    for tlf in map(str, sorted_tlfs):
        ordered_list += [{'tlf': tlf, 'nom': db[tlf]}]
        
    return render_template('main.html', \
                           title = "Buscador", \
                           resultDict = ordered_list, \
                           admin = False)

@app.route('/admin', methods=['GET'])
def admin():
    db = getAllTLFDict()
    sorted_tlfs = sorted(map(int, db.keys()))
    
    ordered_list = []
    for tlf in map(str, sorted_tlfs):
        ordered_list += [{'tlf': tlf, 'nom': db[tlf]}]
        
    return render_template('main.html', \
                           title = "Buscador", \
                           resultDict = ordered_list, \
                           admin = True)

@app.route('/buscador/<user>', methods = ['POST'])
def buscador(user):
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
        ordered_list += [{'tlf': tlf, 'nom': db[tlf]}]

    if user == 'main':
        admin = False
    else:
        admin = True
        
    return render_template('main.html', \
                           title = "Buscador", \
                           resultDict = ordered_list, \
                           admin = admin)
    
@app.route("/autocomplete", methods=['GET'])
def autocomplete():
    search = request.args.get('buscador')

    collator = PyICU.Collator.createInstance(PyICU.Locale('es_ES.UTF-8'))
    
    db = getAllTLFDict()
    sorted_tlfs = sorted(map(int, db.keys()))
    
    sorted_db = []
    for tlf in map(str, sorted_tlfs):
        sorted_db += [tlf + ' - ' + db[tlf]]
    
    app.logger.debug(search)
    return jsonify(json_list = sorted_db)


if __name__ == "__main__":
    app.debug = 0
    app.run('0.0.0.0', port=80, threaded=True)


    
