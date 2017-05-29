#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb as mariadb
import os
import re
import csv

DB_HOST = os.environ["DB_HOST"] 
DB_USER = os.environ["DB_USER"] 
DB_PASSWD = os.environ["DB_PSWD"] 
DB_NAME = os.environ["DB_NAME"]

def connectMariaDB():
    return mariadb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, charset = "utf8")

def insertTLF(tlf, nom, dept='', tlf_dir='', email='', area=''):
    with connectMariaDB() as cur:
        cur.execute("INSERT INTO telefons VALUES(id, %s, %s, %s, %s, %s, %s)", (tlf, nom, dept, tlf_dir, email, area))

def deleteTLF(tlf):
    with connectMariaDB() as cur:
        cur.execute("DELETE FROM telefons WHERE tlf=%s", (tlf,))

def getAllTLFDict():
    tlfDict = {}
    
    with connectMariaDB() as cur:
        cur.execute("SELECT * FROM telefons")
        for row in cur.fetchall():
            tlfDict[row[1]] = [row[2], row[3], row[4], row[5], row[6]]

    return tlfDict

def getAllDBLike(tlf = '0000000000', nom = '0000000000', dept='000000000'):
    contactDict = {}
    
    with connectMariaDB() as cur:
        cur.execute("SELECT * FROM telefons WHERE tlf LIKE %s OR nom LIKE %s OR dept LIKE %s", ('%'+tlf+'%', '%'+nom+'%', '%'+dept+'%'))
        contacts = cur.fetchall()

        for row in contacts:
            contactDict[row[1]] = [row[2], row[3], row[4], row[5], row[6]]

    return contactDict

def getContacte(nom):
    with connectMariaDB() as cur:
        cur.execute("SELECT * FROM telefons where nom=%s", (nom,))
        row = cur.fetchone()
        
    if row is None:
        return None
    else:
        return row[1:]

def getDepartaments():
    deptList = []

    with connectMariaDB() as cur:
        cur.execute("SELECT dept FROM telefons")
        rows  = cur.fetchall()

        for row in rows:
            if row[0] not in deptList and row[0] != '':
                deptList += [row[0]]

    return deptList
    
def getDepartamentDict(dept):
    deptDict = {}
    
    with connectMariaDB() as cur:
        cur.execute("SELECT * FROM telefons WHERE dept=%s", (dept,))
        for row in cur.fetchall():
            deptDict[row[1]] = [row[2], row[3], row[4], row[5], row[6]]

    return deptDict
    
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
        
def updateTLF(tlf, nou_tlf):
    with connectMariaDB() as cur:
        cur.execute("UPDATE telefons SET tlf=%s WHERE tlf=%s", (nou_tlf, tlf))
    
def checkRepeatTLF(tlf):
    with connectMariaDB() as cur:
        cur.execute("SELECT * FROM telefons WHERE tlf=%s", (tlf,))
        return cur.fetchone() is not None
    
def checkRepeatNom(nom):
    with connectMariaDB() as cur:
        cur.execute("SELECT * FROM telefons WHERE nom=%s", (nom,))
        return cur.fetchone() is not None

def formatTLF(tlf):
    reg = re.compile('[^0-9]', re.UNICODE)
    return re.sub(reg, '', tlf)

def formatNom(nom):
    return nom.lstrip().rstrip().replace('-', '_').replace('\r', '').replace('/', '_')

def exportContacts():
    allDBCSV = []
    
    with connectMariaDB() as cur:
        cur.execute("SELECT * FROM telefons")
        rows = cur.fetchall()

    for row in rows:
        allDBCSV += [[row[1], row[2], row[3], row[4], row[5], row[6]]]

    return allDBCSV

def importContacts(filename):
    contactes = False
    with open(filename, 'r') as f:
        rows = f.read().split('\n')

        for row in rows:
            if row == '':
                continue

            camps = row.split(',')
            
            tlf = formatTLF(camps[0])
            nom = formatNom(camps[1])
            dept = formatNom(camps[2])
            tlf_dir = formatTLF(camps[3])
            email = formatNom(camps[4])
            area = formatNom(camps[5])
            
            if checkRepeatTLF(tlf) or len(tlf) > 9 or tlf == '' or checkRepeatNom(nom):
                continue
            else:
                contactes = True
                insertTLF(tlf, nom, dept, tlf_dir, email, area)

    return True
            
