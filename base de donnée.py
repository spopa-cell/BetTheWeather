import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# IMPORTANT : activer les clés étrangères en SQLite
c.execute("PRAGMA foreign_keys = ON;")

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT ,
    password TEXT,
    montant INTEGER
);
""")

c.execute("""
CREATE TABLE IF NOT EXISTS paris (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date DATE,
    valeur REAL,
    lieu TEXT,
    status INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
""")

conn.commit()
conn.close()

print("Base de données créée !")