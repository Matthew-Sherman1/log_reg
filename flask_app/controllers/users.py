from flask_app import app
from flask import render_template,flash,redirect,request,session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/register")
def validate():
    if User.validate_user(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "email":request.form["email"],
        "password":pw_hash,
        }
        user_id = User.insert_user(data)
        flash("User created!", "register")  
        session["user_id"] = user_id
        return redirect("/userpage")
    else:
        return redirect("/")

@app.post("/login")
def login():
    userdb = User.get_by_email(request.form)
    if not userdb:
        flash("invalid email/password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(userdb.password, request.form["password"]): 
        flash("invalid email/password", "login")
        return redirect("/")
    session["user_id"] = userdb.id
    return redirect("/userpage")

@app.route("/userpage")
def user_page():
    if ('user_id' not in session):
        return redirect('/')
    print (session['user_id'])
    user_data = {'id':session['user_id']}
    user = User.get_user(user_data)
    return render_template("userpage.html", user=user)

@app.route("/logout")
def logout():
    session.clear()
    flash("logged out!", "login")
    return redirect("/")

