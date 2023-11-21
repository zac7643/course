from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    f = open("user.txt", "w")
    f.write(username + "," + password)
    f.close()

    return username + " has signed up"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/verify", methods=["POST"])
def verify():
    f = open("user.txt", "r")
    file = f.read()
    split = file.split(",")
    print(file)
    print(split)
    if request.form["username"] == split[0] and request.form["password"] == split[1]:
        return "correct username and password"
    else:
        return "error"





