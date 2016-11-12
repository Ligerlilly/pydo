# curl -H "Content-Type: application/json" -X POST -d '{"todo": "monkey"}' http://localhost:5000/todos/2
# import code
import os
import todo_dao as dao

from flask import Flask, json, request
from flask_mysqldb import MySQL
app = Flask(__name__)
 
# MySQL configurations
app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = 'pydo'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

@app.route("/todos", methods=['GET', 'POST'])
def todos():
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        return dao.get_todos(cur)

    if request.method == 'POST':
        return dao.create_todo(mysql, cur, request.json)

@app.route("/todos/<todo_id>", methods=['GET', 'PUT', 'DELETE'])
def todo(todo_id):
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        return dao.get_todo(cur, todo_id)

    if request.method == 'PUT':
        return dao.update_todo(mysql, cur, todo_id, request.json)

    if request.method == 'DELETE':
        return dao.delete_todo(mysql, cur, todo_id)

if __name__ == "__main__":
    app.run()
