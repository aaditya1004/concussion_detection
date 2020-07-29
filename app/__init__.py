from flask import Flask
import redis
from rq import Queue
from yolo import YOLO
app = Flask(__name__)

r = redis.Redis()

q = Queue(connection=r)

y = YOLO()
from app import views
from app import tasks

