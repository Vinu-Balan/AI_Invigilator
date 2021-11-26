import time
import cv2
from flask import Flask, render_template,request, Response
from precheck import adjuster
from tester import predicter
import json
#from tester import predicter

app = Flask(__name__)

name = None
reg_no = None
dept = None

@app.route('/',methods=['GET', 'POST'])
def index():
    """home page."""
    global name,reg_no,dept
    if request.method == "POST":
        name = request.form.get("name")
        reg_no = request.form.get("reg_no")
        dept = request.form.get("depts")

    return render_template('HomePage.html')


@app.route('/precheck')
def adjustment():
    """Precheck page"""
    return render_template('precheck.html')

@app.route('/precheck/test')

def take_test():
    return render_template('takeTest.html')
# def gen():
#     """Video streaming generator function."""
#     cap = cv2.VideoCapture(0)
#
#     # Read until video is completed
#     while(cap.isOpened()):
#       # Capture frame-by-frame
#         ret, img = cap.read()
#         if ret == True:
#             img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
#             frame = cv2.imencode('.jpg', img)[1].tobytes()
#             yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#         else:
#             break

@app.route('/precheck_video_feed')
def adj_video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(adjuster(),mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/test_video_feed')
def test_video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(predicter(),mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/testEnded')
def testEnded():
    """Test End"""
    global name,reg_no,dept
    with open("warnings.json", "r") as p:
        data = json.load(p)
    status = None
    if data["warning"]>9:
        status = "Malpractice"
    else:
        status = "Completed"
    # with open("student_details.csv", 'w') as fd:
    #     fd.write(str(name)+","+str(reg_no)+","+str(dept)+","+str(data["warning"])+","+status+"\n")
    return render_template('testEnded.html',data=data)

if __name__=='__main__':
    app.run(debug=True)
