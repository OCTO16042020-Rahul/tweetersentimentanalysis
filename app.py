from urllib import request

from flask import Flask, render_template, request, session, url_for, redirect, logging
import pymysql
from flask_login import logout_user

from tweeter import TwitterClient

connection = pymysql.connect(host="localhost", user="root", password="", database="mydb1")
cursor = connection.cursor()

app = Flask(__name__)
app.secret_key = 'random string'


@app.route('/')
def index1():
    return render_template("register.html")
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        username = request.form.get("username")

        password = request.form.get("password")

        # print("insert into userdetails(fname, lname, password) values('"+fname+"','"+lname+",'"+password+")")

        # cursor.execute("insert into userdetails(fname, lname, password) values(:fname, :lname, :password)",{"fname":fname,"lname":fname,"password":password})
        cursor.execute(
            "insert into userdetails(name, phone, username ,password) values('" + name + "','" + phone + "','" + username + "','" + password + "')")

        connection.commit()

        return render_template("login.html")
    else:
        return render_template("about.html")


@app.route('/login1', methods=["POST", "GET"])
def login1():
    if request.method == "POST":

        username = request.form.get("username")


        password = request.form.get("password")
        cursor.execute('SELECT * FROM userdetails WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        print(account)

        # If account exists in accounts table in out database
        if account:

            session['user'] = account[0]
            msg = 'Logged in successfully'

            return render_template('search.html', username=session['user'])
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
        # Show the login form with message (if any)
    return render_template('login.html', msg=msg)


@app.route('/foo')
def foo():
    cursor.execute("select * from tweeterdata ORDER BY id DESC")
    data = cursor.fetchall()  # data from database
    msg = 'Incorrect username/password!'
    return render_template("alldata.html", value=data)


@app.route('/search', methods=["POST", "GET"])
def search():
    if request.method == "POST":

        sql3 = "DELETE FROM tablename1"
        cursor.execute(sql3)
        sql4 = "DELETE FROM tweeterdata"
        cursor.execute(sql4)
        connection.commit()

        t1 = TwitterClient()
        username = request.form.get("search")
        t1.main(username)
        cursor.execute("select * from testtable2 ORDER BY id1 DESC")
        data = cursor.fetchall()  # data from database
        msg = 'Successfully fetched data'
        return render_template("search.html", msg=msg)


@app.route('/piechart') 
def piechart():

        cursor.execute("select avg(psrate),avg(nsrate),avg(neutral) from tweeterdata")
        data = cursor.fetchall()  # data from database
        print(data)
        msg = 'Incorrect username/password!'
        return render_template("chart.html", value=data)

@app.route('/search1')
def search1():
    cursor.execute("select * from tablename1  ORDER BY id DESC")
    data = cursor.fetchall()  # data from database
    msg = 'Incorrect username/password!'
    return render_template("positive.html", value=data)




@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/register1')
def register1():
    return render_template("register.html")


@app.route("/logout")
def logout():

    return render_template("index.html")


@app.route('/search12')
def search12():
    return render_template("search.html")


if __name__ == '__main__':
    app.run(debug="True")
