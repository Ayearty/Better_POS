from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.user import Users
from flask_app.models.dish import Dish
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')

@app.route('/register', methods=["POST"])
def create_user():
    if not Users.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "login":request.form["login"],
        "password":pw_hash,
        "admin":request.form["admin"]
    }
    users_in_db = Users.get_by_login(data)
    if users_in_db:
        flash("Login must be unique.")
        return redirect('/')
    user_id = Users.save(data)
    session["user_id"] = user_id
    return redirect('/dashboard')

@app.route('/login', methods=["POST"])
def login():
    user_in_db = Users.get_by_login(request.form)
    if not user_in_db:
        flash("Invalid login/password.")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid login/password.")
        return redirect('/')
    session["user_id"] = user_in_db.id
    return redirect('/dashboard')

@app.route('/dashboard')
def show():
    if not session.get("user_id"):
        return redirect ('/')
    data = {
        "id" : session["user_id"]
    }
    logged_in_user = Users.get_one(data)
    dishes = Dish.get_all()
    return render_template("dashboard.html", dishes = dishes, user = logged_in_user)

@app.route('/breakdown')
def breakdown():
    dishes = Dish.get_all()
    return render_template("end_day.html", dishes = dishes)

@app.route('/end_day')
def end_day():
    Dish.end_day()
    return redirect('/')