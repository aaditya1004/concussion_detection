from flask import Flask
import redis
from rq import Queue
from yolo import YOLO
app = Flask(__name__)

# r = redis.Redis(host = 'redis', port=6379, decode_responses=True)
r = redis.Redis(host = 'localhost', port=6379, decode_responses=True)
q = Queue(connection=r, job_timeout = '6h')
y = YOLO()

from app import views
from app import tasks

