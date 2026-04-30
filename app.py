from flask import Flask, render_template, request, redirect, session, jsonify
from flask_cors import CORS
import sqlite3
import numpy as np
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)
app.secret_key = "secret123"
CORS(app)

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ================= ML MODEL =================
X = np.array([
    [10, 300, 2],
    [200, 180, 50],
    [50, 400, 5],
    [500, 200, 100],
    [30, 500, 3],
    [1000, 100, 200]
])

y = np.array([1, 0, 1, 0, 1, 0])

model = LogisticRegression()
model.fit(X, y)

# ================= ROUTES =================

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        result = c.fetchone()
        conn.close()

        if result:
            session["user"] = user
            return redirect("/dashboard")
        else:
            return "Invalid Credentials"

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, pwd))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", user=session["user"])
    return redirect("/login")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    followers = int(data["followers"])
    following = int(data["following"])
    posts = int(data["posts"])

    prediction = model.predict([[followers, following, posts]])[0]

    if prediction == 1:
        result = "⚠️ Fake Profile"
    else:
        result = "✅ Real Profile"

    return jsonify({"prediction": result})

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)