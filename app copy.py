from flask import Flask, render_template, request, session, redirect, url_for
import os
import sqlite3
import result
import asearch
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(16)


@app.route("/")
def home():
    return render_template("login.html")

@app.route("/home")
def login():
    if "username" in session:
        username = session["username"]
    else:
        username = "Not Logged in"
    return render_template("homepage.html", username = username)

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/fav")
def fav():
    return render_template("fav.html")

@app.route("/loginverify", methods=["POST"])
def loginverify():
    con = sqlite3.connect("database.db", )
    cur = con.cursor()
    cur.execute("""
                SELECT *
                FROM login
                WHERE username=? AND password=? """,
                (request.form["username"],request.form["password"]))

    rows = cur.fetchall()
    if len(rows) == 1:
        session["username"] = request.form["username"]
        return redirect("/home")
    else:
        return "login not recognised"

@app.route("/insert", methods=["POST"])
def insert():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("""
    INSERT INTO login (username,password)
    VALUES (?,?)""",
    (request.form["username"],request.form["password"]))
    con.commit()

    return redirect("/login")

@app.route("/ins")
def ins():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("""
    INSERT INTO login (username, password)
    VALUES ("bob" , "123")
    """)
    con.commit()
    return "bob created"

@app.route("/tbl")
def tbl():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE login
    (
    username VARCHAR(20) NOT NULL PRIMARY KEY,
    password VARCHAR(20) NOT NULL
    )
    """)

    return "table created"

@app.route("/tbl_favs")
def tbl_favs():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE Favs
    (
    username VARCHAR(20) NOT NULL PRIMARY KEY,
    product_name VARCHAR(20) NOT NULL,
    product_price VARCHAR(20) NOT NULL,
    product_image_url VARCHAR(300) NOT NULL,  
    product_link VARCHAR(300) NOT NULL,  
    price_date VARCHAR(20) NOT NULL                                            
    )
    """)

    con.commit()

@app.route("/logout")
def logout():
    session.pop("username")
    return redirect("/")

@app.route("/search")
def search():
    p = request.args.get("search")
    r = asearch.search(p)
    jobid = r["job_id"]
    # jobid = "64d8b705b437fc1679721546"
    print(jobid)
    o = result.result(jobid)
    return render_template("results.html", o = o)

#def new_fav(link):
# take link and then call api to get details and then save them to thge db

@app.route("/addfav", methods=["POST"])
def addfav():
    n = request.form.get("name")
    p = request.form.get("price")
    i = request.form.get("image")
    l = request.form.get("link")
    d = datetime.datetime.now()
    u = request.form.get("username")
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("""
    INSERT INTO Favs (username, product_name, product_price, product_image, product_link, product_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (u, n, p, i, l, d))
    con.commit()
    return redirect("/home") 

@app.route("/getfav", methods=["POST"])
def getfav():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("""
                SELECT * FROM favs WHERE USERNAME='bob'
""")
    return render_template("/home")           