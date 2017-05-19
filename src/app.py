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
    return render_template('main.html', title = "Buscador")

@app.route('/buscador', methods = ['POST'])
def buscador():
    busc_value_dirty = request.form["buscador"]

    if (len(busc_value_dirty) == 0):
        flash("Escriu telèfon o nom a buscar", "error")
        return redirect(url_for('main'))
    
    busc_value_clean = busc_value_dirty.split('-')[0]

    if (formatTLF(busc_value_clean).isdigit()):
        busc_value_clean = formatTLF(busc_value_clean)
        
        resultList = getAllDBLikeTLF(busc_value_clean)
        if len(resultList) == 0:
            flash("Aquest telèfon no existeix", "error")
            return redirect(url_for('main'))
        else:
            return render_template('main.html', \
                                   title = "Buscador", \
                                   resultDict = resultList)
    
    else:
        busc_value_clean = formatNom(busc_value_clean)

        resultList = getAllDBLikeNom(busc_value_clean)
        if len(resultList) == 0:
            flash("Aquest nom no existeix", "error")
            return redirect(url_for('main'))
        else:
            return render_template('main.html', \
                                   title = 'Buscador', \
                                   resultDict = resultList)
    
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

@app.route("/admin", methods=['GET'])
def admin():
    return render_template('main.html', title = 'Admin', admin = True)

@app.route("/admin", methods=['POST'])
def buscadorAdmin():
    busc_value_dirty = request.form["buscador"]

    if (len(busc_value_dirty) == 0):
        flash("Escriu telèfon o nom a buscar", "error")
        return redirect(url_for('main'))
    
    busc_value_clean = busc_value_dirty.split('-')[0]

    if (formatTLF(busc_value_clean).isdigit()):
        busc_value_clean = formatTLF(busc_value_clean)
        
        resultList = getAllDBLikeTLF(busc_value_clean)
        if len(resultList) == 0:
            flash("Aquest telèfon no existeix", "error")
            return redirect(url_for('main'))
        else:
            return render_template('main.html', \
                                   title = "Buscador", \
                                   resultDict = resultList, \
                                   admin = True)
    
    else:
        busc_value_clean = formatNom(busc_value_clean)

        resultList = getAllDBLikeNom(busc_value_clean)
        if len(resultList) == 0:
            flash("Aquest nom no existeix", "error")
            return redirect(url_for('main'))
        else:
            return render_template('main.html', \
                                   title = "Buscador", \
                                   resultDict = resultList, \
                                   admin = True)

if __name__ == "__main__":
    app.debug = 1
    app.run('0.0.0.0', port=80, threaded=True)


    
