from flask import Flask, request, Response
import json

app = Flask(__name__,static_url_path="/static")


@app.route('/add', methods=["GET"])
def add():
	num1 = float(request.args.get('num1'))
	num2 = float(request.args.get('num2'))
	if not num1 or not num2:
		return Response(status=404)

	result = num1 + num2
	print(num1, num2, result)
	response = Response(
		response=json.dumps({"answer": result}),
		status=200,
		mimetype='application/json'
	)
	return response


@app.route('/sub', methods=["POST"])
def sub():
	#x-www-form-urlencoded
	data = request.form
	num1 = float(data['num1'])
	num2 = float(data['num2'])
	if not num1 or not num2:
		return Response(status=404)

	result = num1 - num2
	print(num1, num2, result)
	response = Response(
		response=json.dumps({"answer": result}),
		status=200,
		mimetype='application/json'
	)
	return response


@app.route('/mult', methods=["POST"])
def mult():
	# application/json
	if request.headers['Content-Type'] == 'application/json':
		arguments = request.get_json()
		if 'num1' not in arguments or 'num2' not in arguments:
			response = Response(status=404)
		else:
			num1 = float(arguments['num1'])
			num2 = float(arguments['num2'])
			result = num1 * num2
			print(num1, num2, result)
			response = Response(
				response=json.dumps({"answer": result}),
				status=200,
				mimetype='application/json'
			)
	else:
		response = Response(status=404)
	return response

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8000, debug=True)

