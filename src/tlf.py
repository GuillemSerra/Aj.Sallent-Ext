#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from database import *

blu_tlf = Blueprint('tlf', __name__, template_folder='templates')

@blu_tlf.route("/insert", methods=['GET'])
def insertTLFView():
    return render_template('insertTLF.html', title="Afegeix un telèfon")

@blu_tlf.route("/insert", methods=['POST'])
def insertTLFViewPost():
    tlf = request.form['tlf']
    nom = request.form['nom']

    print tlf
    print nom
    
    if (len(tlf) == 0) or (len(nom) == 0):
        flash("S'han de completar tots els camps", "error")
        return redirect(url_for('.insertTLFView'))

    if (len(tlf) > 9):
        flash("Telèfon massa llarg", "error")
        return redirect(url_for('.insertTLFView'))

    if not tlf.isdigit():
        flash("El telèfon només pot contenir digits", "error")
        return redirect(url_for('.insertTLFView'))        

    if not checkRepeatTLF(tlf):
        flash("Aquest telèfon ja existeix", "error")
        return redirect(url_for('.insertTLFView'))
                        
    if not checkRepeatNom(nom):
        flash("Aquest nom ja existeix", "error")
        return redirect(url_for('.insertTLFView'))

    insertTLF(tlf, nom)
    flash("Telèfon afegit correctament")
    return redirect(url_for('.insertTLFView'))

@blu_tlf.route("/get", methods=['GET'])
def getAllTLFView():
    return jsonify(getAllTLFDict())

