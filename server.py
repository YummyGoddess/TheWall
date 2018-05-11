from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
from mysqlconnection import MySQLConnector
import md5

mysql = MySQLConnector(app,'the_wall')

app = Flask(__name__)
bcrypt = Bcrypt(app) # creating an object called bcrypt
app.secret_key = '1fish2fishredfishbluefish' #setting secret key
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['POST'])
def login():
    query = "SELECT * FROM users where email = :email"

    data = { "username" : request.form['username'],
             "password_hash" : pw_hash }
    result = mysql.query_db(query, data)
    if result:
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            session['userid'] = result[0]['id']
            return redirect('/success')

    return redirect('/')

    flash("You could not be loggin in")
    return redirect('/')

# @app.route('/createUser', methods=['POST'])
# def createUser():
#     pw_hash = bcrypt.generate_password_hash(request.form['password'])
#     print(pw_hash)
#
#     query = "INSERT INTO users (username, password) VALUE (%(username)s, %(password_hash)s);"
#     data = { "username" : request.form['username'],
#              "password_hash" : pw_hash }
#     result = mysql.query_db(query, data)
#     if result:
#         if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
#             session['userid'] = result[0]['id']
#             return redirect('/success')
#
#     return redirect('/')
#
#     flash("You could not be loggin in")
#     return redirect('/')

@app.route('/users', methods=['POST'])
def create():
    print(request.form)
    print('Name', request.form[name])
    print('')

if __name__ =="__main__":
    app.run(debug=True)
