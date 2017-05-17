#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb as mariadb
import os

DB_HOST = os.environ["DB_HOST"] 
DB_USER = os.environ["DB_USER"] 
DB_PASSWD = os.environ["DB_PSWD"] 
DB_NAME = os.environ["DB_NAME"]

def connectMariaDB():
    return mariadb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

def insertTLF(tlf, nom):
    with connectMariaDB() as cur:
        cur.execute("INSERT INTO telefons VALUES(%s, %s)", (tlf, nom))

def deleteTLF(tlf):
    with connectMariaDB() as cur:
        cur.execute("DELETE FROM telefons WHERE tlf=%s", (tlf))

def updateTLFNom(tlf, nom):
    with connectMariaDB() as cur:
        cur.execute("UPDATE telefons SET nom=%s WHERE tlf=%s", (nom, tlf))

def getAllDBList():
    tlfList = []
    nomList = []
    
    with connectMariaDB() as cur:
        cur.execute("SELECT * FROM telefons")
        for row in cur.fetchall():
            tlfList += [row[0]]
            nomList += [row[1]]

    return tlfList+nomList

def getAllTLFDict():
    tlfDict = {}
    
    with connectMariaDB() as cur:
        cur.execute("SELECT * FROM telefons")
        for row in cur.fetchall():
            tlfDict[row[0]] = row[1]

    return tlfDict
           
def getTLF(nom):
    with connectMariaDB() as cur:
        cur.execute("SELECT tlf FROM telefons where nom=%s", (nom,))
        row = cur.fetchone()
    return row[0]
    
def checkRepeatTLF(tlf):
    with connectMariaDB() as cur:
        cur.execute("SELECT * FROM telefons WHERE tlf=%s", (tlf,))
        return cur.fetchone() is None
    
def checkRepeatNom(nom):
    with connectMariaDB() as cur:
        cur.execute("SELECT * FROM telefons WHERE nom=%s", (nom,))
        return cur.fetchone() is None
        

