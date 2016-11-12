from flask import json
# import code

def get_todos(cursor):
    cursor.execute('''SELECT task FROM todos''')
    result = cursor.fetchall()
    result_list = list(sum(result, ()))
    return json.dumps({'todos': str(result_list)})

def create_todo(mysql, cursor, request_json):
    req_json = json.dumps(request_json)
    req_json_dict = json.loads(req_json)
    # code.interact(local=dict(globals(), **locals()))
    cursor.execute("INSERT INTO todos (task) VALUES (%s)", [str(req_json_dict['todo'])])
    cursor.execute('''SELECT task FROM todos''')
    result = cursor.fetchall()
    result_list = list(sum(result, ()))
    mysql.connection.commit()
    return json.dumps({'todos': str(result_list)})

def get_todo(cursor, todo_id):
    cursor.execute("SELECT task FROM todos Where id = %s", [todo_id])
    result = cursor.fetchall()
    result_list = list(sum(result, ()))
    return json.dumps({'todo': str(result_list[0])})

def update_todo(mysql, cursor, todo_id, request_json):
    req_json = json.dumps(request_json)
    req_json_dict = json.loads(req_json)
    cursor.execute("UPDATE todos SET task = %s WHERE id = %s", [str(req_json_dict['todo']), todo_id])
    cursor.execute("SELECT task FROM todos Where id = %s", todo_id)
    result = cursor.fetchall()
    result_list = list(sum(result, ()))
    mysql.connection.commit()
    return json.dumps({'todo': str(result_list)})

def delete_todo(mysql, cursor, todo_id):
    cursor.execute("DELETE FROM todos WHERE id = %s", [todo_id])
    cursor.execute("SELECT task FROM todos")
    result = cursor.fetchall()
    result_list = list(sum(result, ()))
    mysql.connection.commit()
    return json.dumps({'todos': str(result_list)})