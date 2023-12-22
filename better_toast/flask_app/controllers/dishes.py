from flask_app import app
from flask import render_template, request, redirect,session, flash
from flask_app.models.dish import Dish
from flask_app.models.user import Users

@app.route("/create_dish", methods=["POST"])
def new_dish():
    if not Dish.validate_dish(request.form):
        return redirect ("/dishes/new")
    data = {
        "title":request.form["title"],
        "instructions":request.form["instructions"],
        "description":request.form["description"],
        "ingredients":request.form["ingredients"],
        "creator_id":request.form["creator_id"]
    }
    title_in_db = Dish.get_by_title(data)
    if title_in_db == False:
        flash("Title already exists.")
        return redirect('/dishes/new')
    if title_in_db == True:
        user = Dish.save(data)
        session["creator_id"] = user
        return redirect('/dashboard')

@app.route("/dishes/new")
def form():
    recipes = Dish.get_all()
    print(recipes)
    user = {
        "id" : session["user_id"]
    }
    return render_template("new_recipe.html", user = user)

@app.route("/delete/<int:id>")
def delete(id):
    Dish.delete(id)
    return redirect("/dashboard")

@app.route("/edit/<int:id>")
def update(id):
    data = {
        "id" : id
    }
    dish = Dish.get_one(data)
    return render_template("edit_dish.html", dish = dish)

@app.route("/update/dish/<int:id>", methods=["POST"])
def update_dish(id):
    if not Dish.validate_dish(request.form):
        return redirect (f"/edit/{id}")
    data = {
        "id":id,
        "title":request.form["title"],
        "instructions":request.form["instructions"],
        "ingredients":request.form["ingredients"],
        "description":request.form["description"],
    }
    title_in_db = Dish.get_by_title(data)
    if title_in_db == False:
        flash("Title already exists.")
        return redirect(f'/edit/{id}')
    Dish.update_one(data)
    return redirect(f"/display/recipe/{id}")

@app.route("/display/recipe/<int:id>")
def display_recipe(id):
    data = {
        'id' : id
    }
    user = {
        "id" : session["user_id"]
    }
    dish = Dish.get_one(data)
    logged_in_user = Users.get_by_id(user)
    return render_template("recipe_card.html", dish = dish, logged_in_user = logged_in_user)

@app.route("/add_order/<int:id>", methods=["POST"])
def add_order(id):
    data = {
        'id' : id
    }
    Dish.add_order(data)
    return redirect("/dashboard")