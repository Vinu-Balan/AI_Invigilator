import cv2
import json


def adjuster():
    # Load the cascade
    face_cascade = cv2.CascadeClassifier('./haarcascade/haarcascade_frontalface_default.xml')
    eyes_l_cascade = cv2.CascadeClassifier('./haarcascade/haarcascade_lefteye_2splits.xml')
    eyes_r_cascade = cv2.CascadeClassifier('./haarcascade/haarcascade_righteye_2splits.xml')
    """Video streaming generator function."""
    cap = cv2.VideoCapture(0)

    width_c = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height_c = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    start = 0
    begin=0
    end = 0
    no_face = False
    h_left_warn,h_right_warn,h_bf_warn,h_visible_warn = 1,1,1,1

    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        eyes_r = eyes_r_cascade.detectMultiScale(gray, 1.05, 4)
        eyes_l = eyes_l_cascade.detectMultiScale(gray, 1.05, 4)

        font = cv2.FONT_HERSHEY_SIMPLEX
        # if begin>10:
        #     f = open('./json/states.json', "r")
        #     data = json.load(f)
        #     data['states'][0]['precheck'] = "yes"
        #     f = open('./json/states.json', "w")
        #     json.dump(data, f)
        #     f.close()
        #     break
        if h_left_warn+h_right_warn+h_bf_warn+h_visible_warn != 0:
            start =1
        # elif start > 25 and h_left_warn+h_right_warn+h_bf_warn+h_visible_warn == 0:
        #     end = 1
        #     img = cv2.putText(img, """Press the take test button to continue""", (20, height_c - 100), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        #     begin+=1
        n = 0
        l = len(faces)
        dist_x = 0
        #dist_z = 0
        for (x, y, w, h) in faces:
            # .rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            distance = 360 / w
            dist_z = distance
            dist_x = (x / 100)
            n += 1
        # print(dist_x)
        # "warning
        # More than one people
            # Face not detected
        if len(faces) < 1 and end is 0:
            img = cv2.putText(img, "show you face clearly", (width_c // 4, height_c - 100), font, 1, (255, 255, 255), 2,
                              cv2.LINE_AA)
            no_face = True
            h_visible_warn = 1
        # Moving away in z direction
        elif dist_z > 6 and end is 0 and no_face != False:
            img = cv2.putText(img, "move forward", (width_c // 4, height_c - 100), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            h_bf_warn = 1

        # Moving away in x direction
        elif dist_x < 1.7 and end is 0 and no_face != False:
            img = cv2.putText(img, "Move Left", (width_c // 4, height_c - 100), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            h_left_warn = 1
        elif dist_x > 3.7 and end is 0:
            img = cv2.putText(img, "Move Right", (width_c // 4, height_c - 100), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            h_left_warn = 1

        elif len(eyes_r) and len(eyes_l) is 0 and end is 0:
            img = cv2.putText(img, "Eyes not detected", (width_c // 4, height_c - 100), font, 1, (255, 255, 255), 2,
                              cv2.LINE_AA)
        else:
            h_left_warn, h_right_warn, h_bf_warn, h_visible_warn = 0, 0, 0, 0
        if h_left_warn+h_right_warn+h_bf_warn+h_visible_warn is 0 and start <= 25:
            img = cv2.putText(img, "Perfect!Press the Take Test Button", (width_c // 9, height_c - 100), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            start+=1
        if start>1:
            with open("precheck.json", "w") as p:
                json.dump({"checked": True}, p)
            # print("done")
        if ret == True:
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break

