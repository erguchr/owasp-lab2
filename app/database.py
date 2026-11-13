import sqlite3
import pathlib

path = pathlib.Path(__file__).resolve().parent / "database.db"
con = sqlite3.connect(path)
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS users("
            "id INTEGER PRIMARY KEY AUTOINCREMENT," 
            "username TEXT UNIQUE NOT NULL,"
            "password TEXT NOT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS tasks("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "user_id INTEGER NOT NULL,"
            "content TEXT NOT NULL)")
con.commit()
con.close()