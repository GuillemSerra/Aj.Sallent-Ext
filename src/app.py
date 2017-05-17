#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, request, redirect, url_for
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

@app.route('/', methods = ["GET"])
def main():
    return render_template('main.html', title = "Buscador")

@app.route('/', methods = ['POST'])
def mainPost():
    busc_value = request.form["buscador"]

    if (len(busc_value) == 0):
        flash("Escriu telèfon o nom a buscar")
        return redirect(url_for('main'))

    if busc_value.isdigit():
        return "tlf"
    else:
        return render_template('main.html', Nom = getTLF(busc_value), title = "Buscador", tlf = busc_value)
    return "OK"
        
@app.route("/autocomplete", methods=['GET'])
def autocomplete():
    search = request.args.get('buscador')

    app.logger.debug(search)
    return jsonify(json_list=getAllDBList())

if __name__ == "__main__":
    app.debug = 1
    app.run('0.0.0.0', port=80, threaded=True)

