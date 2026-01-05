import sqlite3

conn=sqlite3.connect("database.db")
c=conn.cursor()

def ajouter_pari(date, lieu):
    cursor = conn.execute("SELECT id FROM users")
    for row in cursor.fetchall():
        id=row[0]
        c.execute(f'INSERT INTO paris(user_id, date, valeur, lieu, status) VALUES ({id}, "{date}", {int(0)}, "{lieu}", 0);')
        conn.commit()