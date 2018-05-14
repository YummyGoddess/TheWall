from flask import Flask, render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
import os, binascii
import hashlib

mysql = connectToMySQL('theGreatwall')

app = Flask(__name__)
bcrypt = Bcrypt(app) # creating an object called bcrypt
app.secret_key = '1fish2fishredfishbluefish' #setting secret key
@app.route('/')
def index(user=None):

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']
    password = request.form['password']
    bytePassword = password.encode()
    query = f"SELECT * FROM users WHERE email='{email}'"
    data = {
        'email': email
    }
    userResult = mysql.query_db(query, data)
    print(userResult)
    if not userResult:
        print("User not found!")
        return redirect('/')
    else:
        print("User found!")
        if hashlib.md5(bytePassword).hexdigest() == userResult[0]['password_hash']:
            session['userid'] = userResult[0]['email_id']
            return redirect('/wall')
        else:
            print(hashlib.md5(bytePassword).hexdigest())

            return redirect('/')


    # data = { "email" : request.form['email'],
    #          "password_hash" : pw_hash }
    # result = mysql.query_db(query, data)
    # if result:
    #     if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
    #         session['userid'] = result[0]['id']
    #         return redirect('/success')

@app.route('/wall')
def wall():

    return "KING IN THE NORTH!"

@app.route('/register', methods=['POST'])
def register():

    email = request.form['email']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    bytePassword = password.encode()
    hashPassword=hashlib.md5(bytePassword).hexdigest()

    session['first_name'] = first_name
    session['last_name'] = last_name
    session['email'] = email
    session['password'] = hashPassword

    data = {
                'first_name': session['first_name'],
                'last_name': session['last_name'],
                'email': session['email'],
                'password_hash': session['password']
            }
    query = f"INSERT INTO users (email, password_hash, created_time, updated_time,first_name,last_name) VALUES('{email}','{hashPassword}',NOW(),NOW(),'{first_name}','{last_name}')"

    mysql.query_db(query, data)
    flash('Registered successfully. Please login')
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

#CANNOT USE /users as a name!!!!!!
# @app.route('/users', methods=['POST'])
# def create():
#     print(request.form)
#     print('Name', request.form[name])
#     print('')

if __name__ =="__main__":
    app.run(debug=True)
