#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from tlf import blu_tlf
from database import *

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
    busc_value = request.form["buscador"]

    if (len(busc_value) == 0):
        flash("Escriu telèfon o nom a buscar", "error")
        return redirect(url_for('main'))

    if busc_value.isdigit():
        return render_template('main.html', nom = getNom(busc_value), title = "Buscador", tlf = busc_value)
    else:
        return render_template('main.html', nom = busc_value, title = "Buscador", tlf = getTLF(busc_value))
    return "OK"
        
@app.route("/autocomplete", methods=['GET'])
def autocomplete():
    search = request.args.get('buscador')

    app.logger.debug(search)
    return jsonify(json_list=getAllDBList())

if __name__ == "__main__":
    app.debug = 1
    app.run('0.0.0.0', port=80, threaded=True)

