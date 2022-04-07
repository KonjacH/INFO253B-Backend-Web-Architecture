from flask import Flask, request, Response
import sqlite3
import json
import uuid

app = Flask(__name__)
conn = sqlite3.connect('task.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS database
				(id string, title varchar(255), is_completed boolean)''')

convert = lambda x: False if x == 0 else True 

@app.route('/v1/tasks', methods=["POST"])
def createNewTask():
    if request.headers['Content-Type'] == 'application/json':
        arguments = request.get_json()
        if "title" in arguments:
            title = arguments.get("title")
        else:
            response = Response(status=200)
            return response
        if "is_completed" in arguments:
            is_completed = arguments.get("is_completed")
        else:
            is_completed = False
    else:
        response = Response(status=200)
        return response

    new_id = str(uuid.uuid1())
    query = "INSERT INTO database (id, title, is_completed) VALUES (?, ?, ?)"
    print(new_id, title, is_completed)
    cursor.execute(query, [new_id, title, is_completed])
    conn.commit()


    response = Response(
		response=json.dumps({"id": new_id}), 
		status=200, 
		mimetype='application/json'
	)
    return response

@app.route('/v1/tasks', methods=["GET"])
def listAllTasks():
    query = "SELECT * from database"
    cursor.execute(query)
    value = cursor.fetchall()
    tasks = []
    for row in range(len(value)):
        tasks += [{
            "id": value[row][0],
            "title": value[row][1],
            "is_completed": convert(value[row][2])
        }]
    data = {"tasks": tasks}
    return Response(response=json.dumps(data), status=200, mimetype='application/json')


@app.route('/v1/tasks/<id>', methods=["GET"])
def getTask(id):
    query = "SELECT * FROM database WHERE id='{}'".format(id)
    cursor.execute(query)
    value = cursor.fetchone()

    if not value:
        response = Response(status=404)
    else:
        response = Response(
			response=json.dumps({"id": value[0], "title": value[1], "is_completed": convert(value[2])}), 
			status=200, 
			mimetype='application/json'
		)
    return response


@app.route('/v1/tasks/<id>', methods=["DELETE"])
def deleteTask(id):
    query = "DELETE FROM database WHERE id='{}'".format(id)
    cursor.execute(query)
    if cursor.rowcount == 0:
        response = Response(status=404)
    else:
        response = Response(status=200)
    return response

@app.route('/v1/tasks/<id>', methods=["PUT"])
def editTask(id):
    if request.headers['Content-Type'] == 'application/json':
        arguments = request.get_json()
        if "title" in arguments:
            title = arguments.get("title")
        else:
            response = Response(status=404)
            return response
            
        if "is_completed" in arguments:
            is_completed = arguments.get("is_completed")
        else:
            response = Response(status=404)
            return response
    else:
        response = Response(status=404)
        return response

    print(title, is_completed)
    query = "UPDATE database SET title='{}', is_completed = {} WHERE id ='{}'".format(title, is_completed, id)
    cursor.execute(query)
    if cursor.rowcount == 0:
        response = Response(status=404)
    else:
        response = Response(status=200)
    return response
    
