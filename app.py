from flask import Flask, render_template, request, send_file
# from werkzeug import secure_filename
import yolo
from yolo import YOLO, detect_video
from yolo_video import predict_video
from PIL import Image
import cv2
import numpy as np

# print("hell0")

# predict_video("data46.mp4","sample_2.mp4")

app = Flask(__name__)
y = YOLO()

@app.route('/')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader1', methods = ['GET', 'POST'])
def detect_image():
   if request.method == 'POST':
      f = request.files['file']
      in_path = "db/input/"+f.filename
      out_path = "db/output/"+f.filename
      f.save((in_path))
      image = Image.open((f))
      i,annotations = y.detect_image(image)
      i.save(out_path)
      return send_file(out_path)

@app.route('/uploader2', methods = ['GET', 'POST'])
def detect_video():
   if request.method == 'POST':
      f = request.files['file']
      print(f)
      in_path = "db/input/"+f.filename
      output_path = "db/output/"+f.filename
      f.save((in_path))
      # image = Image.open((f))
      # i,annotations = y.detect_image(image)
      # i.save(out_path)
      # return send_file(out_path)
      
      vid = cv2.VideoCapture(in_path)
      if not vid.isOpened():
        raise IOError("Couldn't open webcam or video")
      video_FourCC    = int(vid.get(cv2.CAP_PROP_FOURCC))
      video_fps       = vid.get(cv2.CAP_PROP_FPS)
      video_size      = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
      fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
      out = cv2.VideoWriter(output_path, fourcc, video_fps, video_size)
      isOutput = True if output_path != "" else False
      
      
      accum_time = 0
      curr_fps = 0
      fps = "FPS: ??"
      return_value, frame = vid.read()
      print("sarting")
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
      res = cv2.VideoCapture(output_path)
      # return send_file(res);
      return "done"


if __name__ == '__main__':
   app.run(debug = True)