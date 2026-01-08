import sqlite3
from datetime import datetime
import requests 
conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

API_KEY = "80ad0124410dd85906904a668d52b0b8"

def get_weather(city):
    """Récupère les données météo depuis OpenWeatherMap"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=fr"
    response = requests.get(url).json()
    return response

def is_raining(city):
    """Retourne True si pluie dans la dernière heure"""
    data = get_weather(city)
    return data.get("rain", {}).get("1h", 0) > 0

def ajouter_pari(date, lieu):
    """Ajoute un pari pour tous les utilisateurs"""
    c.execute("SELECT id FROM users")
    users = c.fetchall()

    for (user_id,) in users:
        c.execute(
            "INSERT INTO paris (user_id, date, valeur, lieu, status) VALUES (?, ?, ?, ?, ?)",
            (user_id, date, 0, lieu, 0)
        )
    conn.commit()

def verifier_paris():
    """Vérifie tous les paris du jour et met à jour les crédits"""
    today = datetime.now().strftime("%Y-%m-%d")

    c.execute("SELECT id, user_id, date, valeur, lieu, status FROM paris")
    paris = c.fetchall()

    for pid, user_id, date, valeur, lieu, status in paris:
        if date != today:
            continue

        rainy = is_raining(lieu)

        # Récupérer le montant actuel de l'utilisateur
        c.execute("SELECT montant FROM users WHERE id = ?", (user_id,))
        current_money = c.fetchone()[0]

        # Gagner si la prévision est correcte
        if (rainy and status == 1) or (not rainy and status == 2):
            gain = int(valeur) * 2
            new_money = current_money + gain
            c.execute("UPDATE users SET montant = ? WHERE id = ?", (new_money, user_id))

        # Supprimer le pari traité
        c.execute("DELETE FROM paris WHERE id = ?", (pid,))

    conn.commit()

def loop():
    """Appel à faire toutes les heures depuis un scheduler ou cron"""
    now = datetime.now()
    if now.hour == 13:  # Vérifie les paris à 13h
        verifier_paris()
