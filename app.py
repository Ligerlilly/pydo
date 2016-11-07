# curl -H "Content-Type: application/json" -X POST -d '{"todo": "hi"}' http://localhost:5000/todos
import code
import os

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
        cur.execute('''SELECT task FROM todos''')
        result = cur.fetchall()
        result_list = list(sum(result, ()))
        
        return json.dumps({'todos': str(result_list)})

    if request.method == 'POST':
        req_json = json.dumps(request.json)
        req_json_dict = json.loads(req_json)
        cur.execute("INSERT INTO todos (task) VALUES ({str(req_json_dict['todo'])})")
        cur.execute('''SELECT task FROM todos''')
        result = cur.fetchall()
        result_list = list(sum(result, ()))
        mysql.connection.commit()

        return json.dumps({'todos': str(result_list)})

@app.route("/todos/<todo_id>", methods=['GET', 'PUT', 'DELETE'])
def todo(todo_id):
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        cur.execute("SELECT task FROM todos Where id = %s", todo_id)
        result = cur.fetchall()
        result_list = list(sum(result, ()))
        
        return json.dumps({'todos': str(result_list)})

    if request.method == 'PUT':
        req_json = json.dumps(request.json)
        req_json_dict = json.loads(req_json)
        # code.interact(local=dict(globals(), **locals()))
        
        cur.execute("UPDATE todos SET task = %s WHERE id = %s", [str(req_json_dict['todo']), todo_id])
        cur.execute("SELECT task FROM todos Where id = %s", todo_id)
        result = cur.fetchall()
        result_list = list(sum(result, ()))
        mysql.connection.commit()
        
        return json.dumps({'todos': str(result_list)})

    if request.method == 'DELETE':
        cur.execute("DELETE FROM todos WHERE id = %s", [todo_id])
        cur.execute("SELECT task FROM todos")
        result = cur.fetchall()
        result_list = list(sum(result, ()))
        mysql.connection.commit()
        
        return json.dumps({'todos': str(result_list)})

if __name__ == "__main__":
    app.run()
