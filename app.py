import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():    
    if session and session["user"]:
        updates = mongo.db.update.find()
        return render_template("index.html", updates=updates)        
    else:
        return render_template("index.html")


@app.route("/add_update", methods=["GET", "POST"])
def add_update():
    if request.method == "POST":
        update = {
            "date": request.form.get("date"),
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "created_by": session["user"]
        }
        mongo.db.update.insert_one(update)
        flash("You Have Added an Update")
        return redirect(url_for("home"))

    return render_template("index.html")


@app.route("/update")
def update():
    return render_template("update.html")


@app.route("/accommodation")
def accommodation():
    return render_template("accommodation.html")


@app.route("/get_guest_info")
def get_guest_info():
    guest_info = mongo.db.guest_info.find_one(
        {"created_by": session["user"]})
    if guest_info is not None:
        return render_template("preferences.html", guest_info=guest_info)
    else:
        return render_template("add_preferences.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if email already exists in mongodb
        existing_user = mongo.db.user.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            flash("Sorry this email has already been used")
            return redirect(url_for("register"))

        register = {
            "firstName": request.form.get("firstName"),
            "lastName": request.form.get("lastName"),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.user.insert_one(register)

        # start the new users session
        session["user"] = request.form.get("email").lower()
        flash("Congrats, Registration Successful!")
        return redirect(url_for("get_guest_info"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if email exists in db
        existing_user = mongo.db.user.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            # ensure hashed password matches user input
      
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("email").lower()
                    flash("Welcome, {}".format(existing_user["firstName"]))
                    return redirect(url_for(
                        "home"))
            else:
                # invalid password match
                flash("Incorrect Email and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Email and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_preferences", methods=["GET", "POST"])
def add_preferences():
    if request.method == "POST":
        require_accommodation = "Yes" if request.form.get(
            "require_accommodation") else "No"
        dietary_restrictions = "Yes" if request.form.get(
            "dietary_restrictions") else "No"
        guest_information = {
            "number_of_party": request.form.get("number_of_party"),
            "require_accommodation": require_accommodation,
            "dietary_restrictions": dietary_restrictions,
            "dietary_restrictions_description": request.form.get(
                "dietary_restrictions_description"),
            "arrival_date": request.form.get("arrival_date"),
            "add_note": request.form.get("add_note"),
            "created_by": session["user"]
        }
        mongo.db.guest_info.insert_one(guest_information)
        flash("Thanks for Adding Your Preferences")
        return redirect(url_for("get_guest_info"))

    return render_template("add_preferences.html")


@app.route("/edit_preferences/<guest_info_id>", methods=["GET", "POST"])
def edit_preferences(guest_info_id):
    if request.method == "POST":
        require_accommodation = "Yes" if request.form.get(
            "require_accommodation") else "No"
        dietary_restrictions = "Yes" if request.form.get(
            "dietary_restrictions") else "No"
        guest_information = {
            "number_of_party": request.form.get("number_of_party"),
            "require_accommodation": require_accommodation,
            "dietary_restrictions": dietary_restrictions,
            "dietary_restrictions_description": request.form.get(
                "dietary_restrictions_description"),
            "arrival_date": request.form.get("arrival_date"),
            "add_note": request.form.get("add_note"),
            "created_by": session["user"]
        }
        mongo.db.guest_info.update(
            {"_id": ObjectId(guest_info_id)}, guest_information)
        flash("Thanks for Updating Your Preferences")
        return redirect(url_for("get_guest_info"))

    guest_info = mongo.db.guest_info.find_one({"_id": ObjectId(guest_info_id)})
    return render_template("edit_preferences.html", guest_info=guest_info)


@app.route("/delete_preferences/<guest_info_id>")
def delete_preferences(guest_info_id):
    mongo.db.guest_info.remove({"_id": ObjectId(guest_info_id)})
    flash("Preference Deleted")
    return render_template("add_preferences.html") 


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
