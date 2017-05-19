#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb as mariadb
import os
import re

DB_HOST = os.environ["DB_HOST"] 
DB_USER = os.environ["DB_USER"] 
DB_PASSWD = os.environ["DB_PSWD"] 
DB_NAME = os.environ["DB_NAME"]

def connectMariaDB():
    return mariadb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, charset = "utf8")

def insertTLF(tlf, nom):
    with connectMariaDB() as cur:
        cur.execute("INSERT INTO telefons VALUES(id, %s, %s)", (tlf, nom))

def deleteTLF(tlf):
    with connectMariaDB() as cur:
        cur.execute("DELETE FROM telefons WHERE tlf=%s", (tlf,))

def getAllDBList():
    tlfList = []
    nomList = []
    
    with connectMariaDB() as cur:
        cur.execute("SELECT * FROM telefons")
        for row in cur.fetchall():
            tlfList += [row[1]]
            nomList += [row[2]]

    return tlfList+nomList

def getAllTLFDict():
    tlfDict = {}
    
    with connectMariaDB() as cur:
        cur.execute("SELECT * FROM telefons")
        for row in cur.fetchall():
            tlfDict[row[1]] = row[2]

    return tlfDict

def getAllDBLikeTLF(tlf):
    contactList = []
    
    with connectMariaDB() as cur:
        cur.execute("SELECT * FROM telefons WHERE tlf LIKE %s", ('%'+tlf+'%',))
        contacts = cur.fetchall()

        for row in contacts:
            contactList += [{'tlf': row[1], 'nom': row[2]}]

    return contactList

def getAllDBLikeNom(nom):
    contactList = []
    
    with connectMariaDB() as cur:
        cur.execute("SELECT * FROM telefons WHERE nom LIKE %s", ('%'+nom+'%',))
        contacts = cur.fetchall()

        for row in contacts:
            contactList += [{'tlf': row[1], 'nom': row[2]}]

    return contactList

def getNom(tlf):
    with connectMariaDB() as cur:
        cur.execute("SELECT nom FROM telefons where tlf=%s", (tlf,))
        row = cur.fetchone()
    if row is None:
        return None
    else:
        return row[0]
           
def getTLF(nom):
    with connectMariaDB() as cur:
        cur.execute("SELECT tlf FROM telefons where nom=%s", (nom,))
        row = cur.fetchone()
    if row is None:
        return None
    else:
        return row[0]

def updateNom(tlf, nou_nom):
    with connectMariaDB() as cur:
        cur.execute("UPDATE telefons SET nom=%s WHERE tlf=%s", (nou_nom, tlf))
        
def updateTLF(nom, nou_tlf):
    with connectMariaDB() as cur:
        cur.execute("UPDATE telefons SET tlf=%s WHERE nom=%s", (nou_tlf, nom))
    
def checkRepeatTLF(tlf):
    with connectMariaDB() as cur:
        cur.execute("SELECT * FROM telefons WHERE tlf=%s", (tlf,))
        return cur.fetchone() is None
    
def checkRepeatNom(nom):
    with connectMariaDB() as cur:
        cur.execute("SELECT * FROM telefons WHERE nom=%s", (nom,))
        return cur.fetchone() is None

def formatTLF(tlf):
    reg = re.compile('[^0-9]', re.UNICODE)
    return re.sub(reg, '', tlf)

def formatNom(nom):
    return nom.lstrip().rstrip().replace('-', '_')
