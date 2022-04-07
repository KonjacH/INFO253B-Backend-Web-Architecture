from flask import Flask, request, Response
from redis import Redis
from rq import Queue
from rq.job import Job

app = Flask(__name__,static_url_path="/static")
redis_connection = Redis(host='redis', port=6379)
queue = Queue(connection=redis_connection)

@app.route('/count', methods=['GET'])
def count():
	if request.headers['Content-Type'] == 'application/json':
		arguments = request.get_json()
		if 'text' in arguments:
			text = arguments.get('text')
			job = queue.enqueue('worker.count_words', text)
			response = Response(
				response=json.dumps({"Job ID": job.id, "Enqueue Time": job.enqueued_at}),
				status=200,
				mimetype='application/json'
			)
		else:
			response = Response(status=404)
	else:
		response = Response(status=404)

	return response

@app.route('/status/<job_id>', methods=['GET'])
def status(job_id):
	job = Job.fetch(job_id, connection=redis_connection)
	if job:
		response = Response(
			response=json.dumps({"result": job.result}),
			status=200,
			mimetype='application/json'
		)
	else:
		response = Response(
			status=404
		)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True) 


