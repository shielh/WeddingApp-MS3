import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from functools import wraps

if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)

"""
Config for Flask Mail
"""
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'shiel.helen@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = 'shiel.helen@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)
mongo = PyMongo(app)


# https://flask.palletsprojects.com/en/2.0.x/patterns/viewdecorators/
def must_be_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" in session:
            return f(*args, **kwargs)
        return redirect("login")
    return decorated_function


def must_be_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "is_admin" in session:
            return f(*args, **kwargs)
        # if user is logged in, direct to home page
        elif "user" in session:
            return redirect("home")
        # if user is not logged in, prompt to log in
        return redirect("login")
    return decorated_function


@app.route("/")
@app.route("/home")
def home():
    """
    Users that are logged in will see the
    updates on the home page
    """
    if session:
        updates = mongo.db.update.find()
        return render_template("index.html", updates=updates)
    else:
        return render_template("index.html")


@app.route("/accommodation")
@must_be_logged_in
def accommodation():
    """
    Renders accomodation page
    """
    return render_template("accommodation.html")


@app.route("/faq")
@must_be_logged_in
def faq():
    """
    Renders FAQ page
    """
    return render_template("faq.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Allows users to register for
    the site. Only allows an email
    to be registered once
    """
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
            "password": generate_password_hash(request.form.get("password")),
            "is_admin": False
        }
        mongo.db.user.insert_one(register)

        # start the new users session
        session["user"] = request.form.get("email").lower()
        flash("Congrats, Registration Successful!")
        return redirect(url_for("get_guest_info"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Checks if email exists in database and
    ensures hashed password matches user input.
    If there is an invalid password match a
    message will flash indicating that the
    username doesn't exist
    """
    if request.method == "POST":
        existing_user = mongo.db.user.find_one(
            {"email": request.form.get("email").lower()})
        if existing_user:
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("email").lower()
                    session["is_admin"] = existing_user["is_admin"]
                    flash("Welcome, {}".format(existing_user["firstName"]))
                    # Automatically signs user out after 15 mins of inactivity
                    session.permanent = True
                    return redirect(url_for(
                        "home"))
            else:
                # if incorrect password is entered
                flash("Incorrect Email and/or Password")
                return redirect(url_for("login"))
        else:
            flash("Incorrect Email and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Removes user from session cookie
    """
    if "is_admin" in session:
        session.pop("is_admin")

    if session["user"]:
        flash("You have been logged out")
        session.pop("user")
        return redirect(url_for("login"))


@app.route("/view_preferences")
@must_be_admin
def view_preferences():
    guest_infos = mongo.db.guest_info.find()
    if guest_infos is not None:
        return render_template("view_preferences.html",
            guest_infos=guest_infos)
    else:
        return redirect("get_guest_info")


@app.route("/get_guest_info")
@must_be_logged_in
def get_guest_info():
    """
    Allows users to view their preference or
    add them if they have not added them yet
    """
    guest_info = mongo.db.guest_info.find_one(
        {"created_by": session["user"]})
    if guest_info is not None:
        return render_template("preference.html", guest_info=guest_info)
    else:
        return render_template("add_preference.html")


@app.route("/add_preference", methods=["GET", "POST"])
def add_preference():
    """
    Allows users to add their preferences
    """
    if request.method == "POST" and session["user"]:
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
        flash("Thanks for Adding Your Preference")
        return redirect(url_for("get_guest_info"))

    return render_template("add_preference.html")


@app.route("/edit_preference/<guest_info_id>", methods=["GET", "POST"])
def edit_preference(guest_info_id):
    """
    Allows users to edit their own preference
    """
    if request.method == "POST" and session["user"]:
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
    return render_template("edit_preference.html", guest_info=guest_info)


@app.route("/delete_preference/<guest_info_id>")
def delete_preference(guest_info_id):
    """
    Allows users to delete their own preference
    """
    if session["user"]:
        mongo.db.guest_info.remove({"_id": ObjectId(guest_info_id)})
        flash("Preference Deleted")
        return render_template("add_preference.html")


@app.route("/update")
@must_be_admin
def update():
    return render_template("update.html")


@app.route("/add_update", methods=["GET", "POST"])
def add_update():
    """
    Allows an admin user to add an update and email all non-admin users
    when the update is added
    """
    if request.method == "POST" and session["is_admin"]:
        updates = {
            "date": request.form.get("date"),
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "created_by": session["user"]
        }
        mongo.db.update.insert_one(updates)

        # Sends email to all users with admin set to False
        users = mongo.db.user.find({"is_admin": False}, {"email": 1})
        email_list = [user["email"] for user in users if "email" in user]

        msg = Message('Update Added', recipients=email_list)
        msg.html = """Hey guys,<br><br>
            We have just added an update to the site which you can
             view by logging in <a href="https://wedding-app-ms3.herokuapp.com/login">
            here</a><br>
            <br>
            Thanks,<br>
            Emma and Dave
                """
        mail.send(msg)

        flash("You Have Added an Update")

        return redirect(url_for("home"))

    return render_template("index.html")


@app.route("/edit_update/<update_id>", methods=["GET", "POST"])
def edit_update(update_id):
    """
    Allows an admin user to edit an update
    """
    if request.method == "POST" and session["is_admin"]:
        update = {
            "date": request.form.get("date"),
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "created_by": session["user"]
        }
        mongo.db.update.update(
            {"_id": ObjectId(update_id)}, update)
        flash("Thanks for the Update")
        return redirect(url_for("home"))

    update = mongo.db.update.find_one({"_id": ObjectId(update_id)})
    return render_template("edit_update.html", update=update)


@app.route("/delete_update/<update_id>")
def delete_update(update_id):
    """
    Allows admin users to delete an update
    """
    if session["is_admin"]:
        mongo.db.update.remove({"_id": ObjectId(update_id)})
        flash("Update Deleted")
        return redirect(url_for("home"))
    else:
        return render_template("index.html")


@app.errorhandler(404)
def error_not_found(error):
    """
    Handles route to 404 error
    """
    return render_template("404.html", error=error), 404


@app.errorhandler(500)
def server_error(error):
    """
    Handles route to 500 error
    """
    return render_template("500.html", error=error), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
