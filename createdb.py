#!/usr/bin/python

import sqlite3 as lite

# connect to the sqlite db
conn=lite.connect('newalexa.db', 86400)
cur=conn.cursor()

# Table formats for SQLite Database
cur.execute("CREATE TABLE Top1Million(domain TEXT PRIMARY KEY, category TEXT, subcategory1 TEXT, subcategory2 TEXT, keywords TEXT, nonalexasites TEXT, Malicious TEXT)")
cur.execute("CREATE TABLE AlexaInstance(rankdate TEXT NOT NULL UNIQUE, rank TEXT NOT NULL, domain TEXT NOT NULL, date DATETIME NOT NULL DEFAULT CURRENT_DATE, url TEXT, headers BLOB, status BLOB, meta BLOB, encoding TEXT, body TEXT, webkitbody TEXT, snapshot BLOB)")