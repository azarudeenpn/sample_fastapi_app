"""Script to initialize sqlite database. This script should be run from root directory. Otherwise, it will result in
database not found exception as database will be created in inner-directory."""

import sqlite3

con = sqlite3.connect("address_db.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE address(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, email TEXT, country TEXT, lat NUMERIC, lon NUMERIC)")
con.commit()
