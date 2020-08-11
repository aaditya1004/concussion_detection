# from concussion_detection.app import app
from app import app
from app import r
from app import q
from app import y
import boto3
from flask import render_template, request, send_file
from app.tasks import detect_image, detect_video


aws_access_key_id= "ASIA4ACNOQ42EIJRFNE5"
aws_secret_access_key="Sr1vnaIhuIWVn8A7wdNiBKqumEvhHNMAaoSNZsLb"
aws_session_token="FwoGZXIvYXdzEIz//////////wEaDHY/eaVPusDXM7nMISK8ARzz1NvTQnJGUliJfhjlazNKNwZ78B9sqp7hepH41aWu294dpNwoHuh135RyPrbrzYg56jyXy3NbSWZ7EwbCUYiqSW35j/GLs59DPVvVFzo3QMQs7I201DMT+IFEdm1yYJtRT3u/9Ujrlm4zBPbbW8iC5XJ/TeWhXxCgq+Rf4nHkhRVWU4tzPwtafbX3qLDYWldyGYdCh2pk9NrgYw29WrmlahDFF68VSl6JCe5xAYnlVQoTKBMN9EJweEjjKNmOyPkFMi1GqXWbFxvjUDI0pdTsQiNCuu8QCLugjJcNpjjTszXHYVdSa7GaI51deULLSdM="

s3_client = boto3.client(
's3',
aws_access_key_id=aws_access_key_id,
aws_secret_access_key=aws_secret_access_key,
aws_session_token=aws_session_token)

bucket = "concussioninput"
bucket2 = "concussionoutput"
base = "db/"

@app.route('/')
def upload_file():
	print("home")
	return render_template('upload.html')
	
@app.route('/predict', methods = ['GET', 'POST'])
def process():
	jobs = q.jobs
	message = ""
	if request.method == 'POST':
		f = request.files['file']
		file_name = f.filename
		in_path = base+"input/"+f.filename
		out_path = base+"output/"+f.filename
		f.save((in_path))
		s3_client.upload_file(in_path, bucket, file_name)
		if (check_ext(f.filename)):
			# file_name = f.filename
			# in_path = base+"input/"+f.filename
			# out_path = base+"output/"+f.filename
			# f.save((in_path))
			# s3_client.upload_file(in_path, bucket, file_name)
			task = q.enqueue(detect_image, in_path, out_path, file_name)  # Send a job to the task queue
			jobs = q.jobs  # Get a list of jobs in the queue
			q_len = len(q)  # Get the queue length
			message = f"Task queued at {task.enqueued_at.strftime('%a, %d %b %Y %H:%M:%S')}. {q_len} jobs"
		else:
			# file_name = f.filename
			# in_path = base+"input/"+f.filename
			# out_path = base+"output/"+f.filename
			# f.save((in_path))
			# s3_client.upload_file(in_path, bucket, file_name)
			task = q.enqueue(detect_video, in_path, out_path, file_name)  # Send a job to the task queue
			jobs = q.jobs  # Get a list of jobs in the queue
			q_len = len(q)
			message = f"Task queued at {task.enqueued_at.strftime('%a, %d %b %Y %H:%M:%S')}. {q_len} jobs"

	# return message
	return render_template("add_task.html", message=message, jobs=jobs)
		
def check_ext(filename):
	import os.path
	extension = os.path.splitext(filename)[1]
	if (extension == ".jpg"):
		return True
	else:
		return False

# @app.route('/predictVideo', methods = ['GET', 'POST'])
# def process_video():
# 	jobs = q.jobs
# 	message = ""
# 	if request.method == 'POST':
# 		f = request.files['file']
# 		print(f)
# 		in_path = base+"input/"+f.filename
# 		out_path = base+"output/"+f.filename
# 		f.save((in_path))
# 		task = q.enqueue(detect_video, in_path, out_path)  # Send a job to the task queue
# 		jobs = q.jobs  # Get a list of jobs in the queue
# 		q_len = len(q)  # Get the queue length
# 	message = f"Task queued at {task.enqueued_at.strftime('%a, %d %b %Y %H:%M:%S')}. {q_len} jobs"
# 	return message
		