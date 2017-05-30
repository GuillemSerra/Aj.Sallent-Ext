#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from tlf import blu_tlf
from buscador import blu_busc, order_tlfs
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
app.register_blueprint(blu_busc, url_prefix='/buscador')
app.config['JSON_AS_ASCII'] = False # jsonify utf-8

@app.route('/', methods = ["GET"])
def main():
    db = getAllTLFDict()

    # Mètode per no tenir problemes amb leading 0s
    ordered_list = order_tlfs(db)
        
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
        ordered_list += [{'tlf': tlf, 'nom': db[tlf][0], \
                          'dept': db[tlf][1], 'tlf_dir': db[tlf][2], \
                          'email': db[tlf][3], 'area': db[tlf][4]}]
                
    return render_template('main.html', \
                           title = "Buscador", \
                           resultDict = ordered_list, \
                           admin = True)



if __name__ == "__main__":
    app.debug = 1
    app.run('0.0.0.0', port=80, threaded=True)


    
