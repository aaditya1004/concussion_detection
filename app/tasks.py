# from app import app 
from app import r
from app import q
from app import y
from flask import render_template, request, send_file
from PIL import Image
import cv2
import numpy as np

def detect_image(in_path, out_path):

	image = Image.open((in_path))
	i,annotations = y.detect_image(image)
	i.save(out_path)

def detect_video(in_path, out_path):

	vid = cv2.VideoCapture(in_path)
	if not vid.isOpened():
		raise IOError("Couldn't open webcam or video")
	video_FourCC    = int(vid.get(cv2.CAP_PROP_FOURCC))
	video_fps       = vid.get(cv2.CAP_PROP_FPS)
	video_size      = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
	                 int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
	fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
	out = cv2.VideoWriter(out_path, fourcc, video_fps, video_size)
	isOutput = True if out_path != "" else False
	accum_time = 0
	curr_fps = 0
	fps = "FPS: ??"
	return_value, frame = vid.read()
	while True & (frame is not None):
		image = Image.fromarray(frame)
 
		image,annotations = y.detect_image(image)
 
		result = np.asarray(image)
 
		cv2.putText(result, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
             fontScale=0.50, color=(255, 0, 0), thickness=2)
		if isOutput:
			out.write(result)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		return_value, frame = vid.read()

	res = cv2.VideoCapture(out_path)
	return out_path
	

    