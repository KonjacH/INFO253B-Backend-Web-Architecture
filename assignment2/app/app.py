from flask import Flask, request, Response
import mysql.connector
from redis import Redis
from rq import Queue
from rq.job import Job
import json
import uuid
import sys

app = Flask(__name__)
config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'demo'
    }

r = Redis(host="redis", port=6379)
queue = Queue(connection=r)

convert = lambda x: False if x == 0 else True 


@app.route('/v1/tasks', methods=["POST"])
def createNewTask():
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
            is_completed = False

        if "notify" in arguments:
            notify = arguments.get("notify")
        else:
            notify = ""

    else:
        response = Response(status=404)
        return response

    new_id = str(uuid.uuid1())
    print(new_id, title, is_completed, notify)
    query = "INSERT INTO tasks (id, title, is_completed, notify) VALUES (%s, %s, %s, %s)"
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(query, [new_id, title, is_completed, notify])
    conn.commit()
    cursor.close()
    conn.close()

    if is_completed:
        queue.enqueue("messenger.send_message", args=(notify, title))


    response = Response(
		response=json.dumps({"id": new_id}), 
		status=200, 
		mimetype='application/json'
	)
    return response

@app.route('/v1/tasks', methods=["GET"])
def listAllTasks():
    query = "SELECT * from tasks"
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(query)
    value = cursor.fetchall()
    tasks = []
    for row in range(len(value)):
        tasks += [{
            "id": value[row][0],
            "title": value[row][1],
            "is_completed": convert(value[row][2]),
            "notify": value[row][3]
        }]
    data = {"tasks": tasks}
    conn.commit()
    cursor.close()
    conn.close()
    return Response(response=json.dumps(data), status=200, mimetype='application/json')


@app.route('/v1/tasks/<id>', methods=["GET"])
def getTask(id):
    query = "SELECT * FROM tasks WHERE id=%s"
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(query, (id,))
    value = cursor.fetchone()

    if not value:
        response = Response(status=404)
    else:
        response = Response(
			response=json.dumps({
                "id": value[0], 
                "title": value[1], 
                "is_completed": convert(value[2]), 
                "notify": value[3]
            }), 
			status=200, 
			mimetype='application/json'
		)

    conn.commit()
    cursor.close()
    conn.close()
    return response


@app.route('/v1/tasks/<id>', methods=["DELETE"])
def deleteTask(id):
    query = "DELETE FROM tasks WHERE id=%s"
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(query, (id,))
    if cursor.rowcount == 0:
        response = Response(status=404)
    else:
        response = Response(status=200)
    conn.commit()
    cursor.close()
    conn.close()
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

        if "notify" in arguments:
            notify = arguments.get("notify")
        else:
            response = Response(status=404)
            return response

        print(title, is_completed, notify)
    else:
        response = Response(status=404)
        return response

    if is_completed:
        queue.enqueue("messenger.send_message", args=(notify, title))

    query = "UPDATE tasks SET title=%s, is_completed=%s, notify=%s WHERE id =%s"
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(query, (title, is_completed, notify, id))
    if cursor.rowcount == 0:
        response = Response(status=404)
    else:
        response = Response(status=200)

    conn.commit()
    cursor.close()
    conn.close()
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0")
     
