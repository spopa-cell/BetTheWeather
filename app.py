from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
app.secret_key = "meteo_secret_key"
bcrypt = Bcrypt(app)

assert 1==1
def get_user(username):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT username, montant FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

# Page login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = get_user(username)
        if user and bcrypt.check_password_hash(user[2], password):
            session["user"] = username
            session["user_id"] = user[0]  # Stocker l'id de l'utilisateur dans la session
            return redirect(url_for("home"))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect.", "danger")
    return render_template("login.html")

# Page inscription
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            montant = int(request.form.get("montant"))
        except ValueError:
            flash("Le montant doit être un nombre entier.", "danger")
            return render_template("register.html")

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password, montant) VALUES (?, ?, ?)", (username, hashed, montant))
            conn.commit()
            conn.close()
            flash("Inscription réussie ! Connectez-vous.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Nom d'utilisateur déjà utilisé.", "danger")
        except sqlite3.Error as e:
            flash(f"Erreur base de données : {e}", "danger")

    return render_template("register.html")

# Déconnexion
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    flash("Déconnecté.", "info")
    return redirect(url_for("login"))

# Récupérer les paris pour un utilisateur
def get_paris_for_user(user_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        SELECT id, date, lieu, valeur, status
        FROM paris
        WHERE user_id = ?
        ORDER BY date
    """, (user_id,))
    paris = c.fetchall()
    conn.close()
    return paris

# Page protégée : home
@app.route("/", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    if request.method == "POST":
        paris_id = request.form.get("paris_id")
        choice = request.form.get("choice")
        valeur = int(request.form.get("amount"))

        status = 1 if choice == "oui" else 2

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        # Vérifier le pari existant
        c.execute("SELECT status, valeur FROM paris WHERE id = ? AND user_id = ?", (paris_id, user_id))
        result = c.fetchone()
        if result:
            old_status, old_valeur = result

            if old_status == 0:  # jamais parié → on peut retirer le montant
                # Retirer la mise
                c.execute("SELECT montant FROM users WHERE id = ?", (user_id,))
                current_money = c.fetchone()[0]

                if valeur > current_money:
                    flash("Vous n'avez pas assez de crédits pour ce pari.", "danger")
                else:
                    new_money = current_money - valeur
                    c.execute("UPDATE users SET montant = ? WHERE id = ?", (new_money, user_id))

                    # Mettre à jour le pari
                    c.execute("""
                        UPDATE paris
                        SET status = ?, valeur = ?
                        WHERE id = ? AND user_id = ?
                    """, (status, valeur, paris_id, user_id))
                    conn.commit()
            else:
                flash("Vous avez déjà parié sur ce pari.", "warning")

        conn.close()


    paris_list = get_paris_for_user(user_id)
    user = get_user_by_id(user_id)

    return render_template(
        "frontendtest1.html",
        paris=paris_list,
        username=user[0],
        credit=user[1]
    )
if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
