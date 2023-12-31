from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3 as sql
import resul
import asearch
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(16)

conn = sql.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS login (username VARCHAR(20) NOT NULL PRIMARY KEY,email VARCHAR(20) NOT NULL, password VARCHAR(100) NOT NULL)')
print("Login table created successfully")

cur = conn.cursor()  # Create a cursor object
cur.execute("""
    CREATE TABLE IF NOT EXISTS favs
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(20) NOT NULL,
    product_name VARCHAR(20) NOT NULL,
    product_price VARCHAR(20) NOT NULL,
    product_image_url VARCHAR(300) NOT NULL,  
    product_link VARCHAR(300) NOT NULL,  
    price_date VARCHAR(20) NOT NULL,
    sterm NOT NULL                                           
    )
    """)
print("Fav's table created successfully")

#conn.execute('ALTER TABLE favs ADD sterm NOT NULL DEFAULT "ipad"')

cur = conn.cursor()  # Create a cursor object
cur.execute("""
    CREATE TABLE IF NOT EXISTS stats
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fav_id INTEGER NOT NULL,        
    product_price_stats VARCHAR(20) NOT NULL,  
    price_date_stats VARCHAR(20) NOT NULL,
    FOREIGN KEY (fav_id) REFERENCES favs (id)
    )
    """)
print("Stats's table created successfully")
conn.commit()  # Commit the transaction
conn.close()  # Close the connection

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/home")
def login():
    if "username" in session:
        username = session["username"]
        con = sql.connect("database.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("""
        SELECT * FROM favs 
        WHERE favs.USERNAME = ?
        """, (username,))
        rows = cur.fetchall(); 
        cur.close()
        con.close()
        return render_template("homepage.html", username=username, rows=rows)
    else:
        username = "Not Logged in"
    return redirect("/")


@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/fav")
def fav():
    return render_template("fav.html")

@app.route("/loginverify", methods=["POST"])
def loginverify():
    con = sql.connect("database.db", )
    cur = con.cursor()
    cur.execute("""
                SELECT *
                FROM login
                WHERE username=? OR email=?""",
                (request.form["user_input"],request.form["user_input"]))

    row = cur.fetchone()
    if row and check_password_hash(row[2], request.form["password"]):
        session["username"] = row[0]
        return redirect("/home")
    else:
        return render_template("login.html", error="Account not found")

@app.route("/logininsert", methods=["POST"])
def login_insert():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("""
                SELECT *
                FROM login
                WHERE username=? AND email=?""",
                (request.form["username"],request.form["email"]))
    
    row = cur.fetchone()
    if not row:
        hashed_password = generate_password_hash(request.form["password"], method='pbkdf2:sha256')
        cur.execute("""
                    INSERT INTO login (username,email,password)
                    VALUES (?,?,?)""",
                    (request.form["username"],request.form["email"], hashed_password))
        con.commit()        
        return redirect("/")
    else:
        return render_template("signup.html", error="username or email already in use")
    


@app.route("/logout")
def logout():
    session.pop("username")
    return redirect("/")

global_sterm = ""

@app.route("/search")
def search():
    global global_sterm
    p = request.args.get("search")
    r = asearch.search(p)
    jobid = r["job_id"]
    #jobid = "658eedbc4e52473d45e20b57"
    print(jobid)
    global_sterm = p
    o = resul.result(jobid)
    return render_template("results.html",  o = o)

@app.route("/addfav", methods=["POST"])
def addfav():
    global global_sterm
    n = request.form.get("name")
    p = request.form.get("price")
    i = request.form.get("image")
    l = request.form.get("link")
    d = datetime.now().strftime('%Y-%m-%d-%H:%M')
    s = global_sterm

    if "username" in session:
        u = session["username"]
    else:
        print("No username in session")
        return redirect("/login")  
    con = sql.connect("database.db")
    try:
        cur = con.cursor()
        cur.execute("""
        INSERT INTO favs (username, product_name, product_price, product_image_url, product_link, price_date, sterm)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (u, n, p, i, l, d, s))
        fav_id = cur.lastrowid  # Get the ID of the last inserted row
        con.commit()
    finally:
        cur.close()  # Ensure the cursor is closed even if an error occurs

    con = sql.connect("database.db")
    try:
        cur = con.cursor()
        cur.execute("""
        INSERT INTO stats (fav_id, product_price_stats, price_date_stats)
        VALUES (?, ?, ?)
        """, (fav_id, p, d))  
        con.commit()
    finally:
        cur.close()  # Ensure the cursor is closed even if an error occurs

    print("Fav added to db")
    return redirect("/home")





@app.route("/deletefav/<id>")
def delete_fav(id):
    # Connect to the SQLite database
    con = sql.connect("database.db")
    cur = con.cursor()

    # Execute the DELETE statement
    cur.execute("DELETE FROM favs WHERE id = ?", (id,))

    # Commit the changes and close the connection
    con.commit()
    con.close()
    print("fav deleted")
    return redirect("/home")

# """ @app.route("/addstat")
# def addstat_form():
#     return render_template("addstat.html") """

# """ @app.route("/stats")
# def stats_page():
#     return render_template("stats.html") """

# """ @app.route("/addstats", methods=["POST"])
# def addstats():
#     fav_id = request.form.get("fav_id")
#     p = request.form.get("product_price")
#     d = datetime.now().strftime('%Y-%m-%d-%H:%M')

#     con = sql.connect("database.db")
#     cur = con.cursor()
#     # Update the current price and date in the main table
#     cur.execute("""
#     # UPDATE favs
#     # SET product_price = ?, price_date = ?
#     # WHERE id = ?
#     """, (p, d, fav_id))

#     # Insert the historical price and date into the stats table
#     cur.execute("""
#     # INSERT INTO stats (fav_id, product_price_stats, price_date_stats)
#     # VALUES (?, ?, ?)
#     """, (fav_id, p, d))
#     con.commit()
#     print("Stat added to db")
#     return redirect("/home") """


@app.route('/getstats/<id>')
def get_stats(id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("""
                SELECT fav_id, product_price_stats, price_date_stats
                FROM stats
                WHERE fav_id = ? """,
                (id,))  
    rows = cur.fetchall()
    # Get column names from the cursor description
    column_names = [column[0] for column in cur.description]      
    # Convert rows to list of dictionaries
    data = [dict(zip(column_names, row)) for row in rows]
    # Sort data by 'product_price' in descending order
    data = sorted(data, key=lambda x: float(x['product_price_stats']), reverse=False)
    global sdata
    sdata = jsonify(data)
    print(data)
    return redirect('http://141.147.64.158:8501')


@app.route('/getstatschart/')
def get_stats_chart():
    return sdata

@app.route('/show_stats')
def show_stats():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM stats")
    stats_data = cur.fetchall()
    con.close()
    return render_template('show_stats.html', stats_data=stats_data)


if __name__ == '__main__':
    app.run(debug=True)



# flask run -p 4999  
# python3 -m venv venv
# .\.venv\Scripts\activate 
# set FLASK_DEBUG=1
 
# streamlit run stats.py 