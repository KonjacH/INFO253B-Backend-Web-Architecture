from flask import Flask, request, Response
import sqlite3
import json

app = Flask(__name__,static_url_path="/static")
conn = sqlite3.connect('key_val.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS database
				(key varchar(255), value varchar(255))''')

@app.route('/', methods=["POST", "DELETE"])
def access():
	arguments = key = value = None
	if request.headers['Content-Type'] == 'application/json':
		arguments = request.get_json()
		key = arguments.get('key')
		value = arguments.get('value')
		if request.method == 'POST':
			query = "SELECT key FROM database WHERE key='{}'".format(key)
			cursor.execute(query)
			result = cursor.fetchone()
			if not result:
				query = "INSERT INTO database (key, value) VALUES (?, ?)"
				cursor.execute(query, [key, value])
			else:
				query = "UPDATE database SET value='{}' WHERE key='{}'".format(value, key)
				cursor.execute(query)

			conn.commit()
			response = Response(
				response=json.dumps({"key": key, "value": value, "message": "success"}),
				status=201,
				mimetype='application/json'
			)

	        
		elif request.method == 'DELETE':
			query = "DELETE FROM database WHERE key= '" + key +"'"
			cursor.execute(query)
			conn.commit()
			if cursor.rowcount == 0:
				response = Response(status=404)
			else:
				response = Response(
	        		response=json.dumps({"key": key, "message": "success"}),
	        		status=200,
	        		mimetype='application/json'
	    		)
	else:
		logging.warning("Invalid content type: only application/json is allowed")
		response = Response(status=400)

	return response

@app.route('/<key>', methods=["GET"])
def get(key):
	query = "SELECT value FROM database WHERE key='{}'".format(key)
	cursor.execute(query)
	value = cursor.fetchone()

	if not value:
		response = Response(status=404)
	else:
		value = value[0]
		response = Response(
			response=json.dumps({"value": value}), 
			status=200, 
			mimetype='application/json'
		)
	return response
