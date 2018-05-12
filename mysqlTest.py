from flask import Flask
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL
app = Flask(__name__)
# invoke the connectToMySQL function and pass it the name of the database we're using
# connectToMySQL returns an- instance of MySQLConnection, which we will store in the variable 'mysql'
mysql = connectToMySQL('theGreatwall')
# now, we may invoke the query_db method
@app.route('/')
def index():
    print("all the users", mysql.query_db("SELECT * FROM users;"))
    return "How am I going to put this on my laptop?"

if __name__ == "__main__":
    app.run(debug=True)
