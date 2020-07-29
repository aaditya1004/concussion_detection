from app import app
from app import r
from app import q
from app import y

from flask import render_template, request, send_file
from app.tasks import detect_image, detect_video

base = "/Users/aadityasrivathsan/Documents/GitHub/concussion_detection/db/"

@app.route('/')
def upload_file():
	print("home")
	return render_template('upload.html')
	
@app.route('/predictImage', methods = ['GET', 'POST'])
def process_image():
	jobs = q.jobs
	message = ""
	if request.method == 'POST':
		f = request.files['file']
		in_path = base+"input/"+f.filename
		out_path = base+"output/"+f.filename
		f.save((in_path))
		task = q.enqueue(detect_image, in_path, out_path)  # Send a job to the task queue
		jobs = q.jobs  # Get a list of jobs in the queue
		q_len = len(q)  # Get the queue length
		message = f"Task queued at {task.enqueued_at.strftime('%a, %d %b %Y %H:%M:%S')}. {q_len} jobs"
		return message
		# return render_template("add_task.html", message=message, jobs=jobs)
		

@app.route('/predictVideo', methods = ['GET', 'POST'])
def process_video():
	jobs = q.jobs
	message = ""
	if request.method == 'POST':
		f = request.files['file']
		print(f)
		in_path = base+"input/"+f.filename
		out_path = base+"output/"+f.filename
		f.save((in_path))
		task = q.enqueue(detect_video, in_path, out_path)  # Send a job to the task queue
		jobs = q.jobs  # Get a list of jobs in the queue
		q_len = len(q)  # Get the queue length
		message = f"Task queued at {task.enqueued_at.strftime('%a, %d %b %Y %H:%M:%S')}. {q_len} jobs"
		return message
		