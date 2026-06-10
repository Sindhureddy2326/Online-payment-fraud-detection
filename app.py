from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import tensorflow as tf
from tinydb import TinyDB, Query
import os

app = Flask(__name__)
app.secret_key = "yasodhasolutions"

db = TinyDB("users.json")
User = Query()

model = tf.keras.models.load_model(
    r"C:\Users\USER\PycharmProjects\FinancialFraud\.venv\New_FinancialFraud_DeepLearning_2026\ModelFiles\cnn_model.h5"
)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db.search((User.username == username) & (User.password == password))
        if user:
            session["user"] = username
            return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        db.insert({
            "name": request.form["name"],
            "username": request.form["username"],
            "password": request.form["password"],
            "email": request.form["email"],
            "mobile": request.form["mobile"]
        })
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    prediction = None

    if request.method == "POST":
        values = [
            float(request.form["amount"]),
            float(request.form["quantity"]),
            float(request.form["customer_age"]),
            float(request.form["account_age"]),
            float(request.form["hour"]),
            float(request.form["payment"]),
            float(request.form["category"]),
            float(request.form["device"])
        ]

        X = np.array(values).reshape(1, -1, 1)
        prob = model.predict(X)[0][1]
        prediction = "Fraudulent Transaction" if prob > 0.4 else "Legitimate Transaction"

    return render_template(
        "dashboard.html",
        prediction=prediction
    )

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
