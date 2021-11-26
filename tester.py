import cv2
import numpy as np
#import webbrowser
import json
from datetime import datetime
from playsound import playsound
from keras.models import load_model
from keras.preprocessing import image
def predicter():
    #db_name = "./csv_files/studentdetails.csv"
    submitted = False
    #multiple_tabs = False
    f_up, f_down,f_side,f_moved_back,f_moved_side,f_turned_head = 0,0,0,0,0,0
    final_warn = 0
    # Load the cascade
    eyes_l_cascade = cv2.CascadeClassifier('./haarcascade/haarcascade_lefteye_2splits.xml')
    eyes_r_cascade = cv2.CascadeClassifier('./haarcascade/haarcascade_righteye_2splits.xml')
    face_cascade = cv2.CascadeClassifier('./haarcascade/haarcascade_frontalface_default.xml')
    # To capture video from webcam.
    cap = cv2.VideoCapture(0)
    # To use a video file as input
    width_c = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height_c = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    mymodel=load_model('./h5models/eye_track_model.h5')

    warning = 0
    h_side_warn,h_bf_warn,e_side_warn,e_down_warn,e_blink,e_up_warn = 0,0,0,0,0,0
    m_tab_warn = 0
    time_up = False
    while (cap.isOpened()):
        # Read the frame
        ret, img = cap.read()
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_face = gray[0:height_c//2+height_c//3, :]
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray_face, 1.1, 4)
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Draw the rectangle around each face
        if e_blink>3:
            warning +=1
            f_down +=1
            final_warn+=1
            img = cv2.putText(img, "looking down", (width_c // 4, height_c - 100), font, 2, (255, 255, 255),
                              2,
                              cv2.LINE_AA)
            playsound('./Sound/beep-05.mp3')
            e_blink = 0
        if h_side_warn + h_bf_warn + e_down_warn + e_side_warn + e_up_warn >= 7:
            warning += 1
            final_warn+=1
            playsound('./Sound/beep-05.mp3')
            h_side_warn, h_bf_warn,e_down_warn,e_side_warn,e_up_warn = 0,0,0,0,0

        n = 0
        l = len(faces)
        dist_x = 0
        dist_z = 0
        #Face tracking
        for (x, y, w, h) in faces:
            #cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            distance = 360 / w
            dist_z = distance
            dist_x = (x / 100)
            n += 1
            if n==1:
                #Eyes tracking
                eyes_r = eyes_r_cascade.detectMultiScale(gray_face, 1.05, 4)
                eyes_l = eyes_l_cascade.detectMultiScale(gray_face, 1.05, 4)
                check = 0
                if True:
                    for (ex, ey, ew, eh) in eyes_l:
                        #cv2.rectangle(img, (ex, ey + ey // 11), (ex + ew, ey + eh), (0, 255, 0), 2)
                        roi_gray2 = gray[ey + ey // 11:ey + eh, ex:ex + ew]
                        try:
                            cv2.imwrite("./temp_images/temp.jpg",roi_gray2)
                        except:
                            pass
                        test_image = image.load_img('./temp_images/temp.jpg', target_size=(224, 224, 1))
                        test_image = image.img_to_array(test_image)
                        test_image = np.expand_dims(test_image, axis=0)
                        pred = mymodel.predict(test_image)[0]
                        check += 1
                        if check == 1:
                            if pred[0] == 1:
                                e_blink += 1.3
                            elif pred[1] == 1:
                                e_blink = 0
                            elif pred[2] == 1:
                                img = cv2.putText(img, "looking side", (width_c // 4, height_c - 100), font, 2, (255, 255, 255),
                                                  2,
                                                  cv2.LINE_AA)
                                e_side_warn += 2.5
                                f_side +=1
                                e_blink = 0
                            elif pred[3] == 1:
                                img = cv2.putText(img, "looking side", (width_c // 4, height_c - 100), font, 2, (255, 255, 255),
                                                  2,
                                                  cv2.LINE_AA)
                                e_side_warn += 2.5
                                f_side+=1
                                e_blink = 0
                            elif pred[4] == 1:
                                img = cv2.putText(img, "looking up", (width_c // 4, height_c - 100), font, 2, (255, 255, 255), 2,
                                                  cv2.LINE_AA)
                                e_up_warn += 1
                                f_up +=1
                                e_blink = 0
                        break
                if 1:
                    for (ex, ey, ew, eh) in eyes_r:
                        #cv2.rectangle(img, (ex, ey + ey // 11), (ex + ew, ey + eh), (0, 255, 0), 2)
                        roi_gray2 = gray[ey + ey // 11:ey + eh, ex:ex + ew]
                        try:
                            cv2.imwrite("./temp_images/temp.jpg",roi_gray2)
                        except:
                            pass
                        test_image = image.load_img('./temp_images/temp.jpg', target_size=(224, 224, 1))
                        test_image = image.img_to_array(test_image)
                        test_image = np.expand_dims(test_image, axis=0)
                        pred = mymodel.predict(test_image)[0]
                        check += 1
                        if check == 1:
                            # img = cv2.putText(img,str(np.round(pred)),(width_c//4,height_c-100),font,2,(255,10,20),2,cv2.LINE_AA)

                            if pred[0] == 1:
                                e_blink+=1.3

                            elif pred[1] == 1:
                                e_blink = 0
                            elif pred[2] == 1:
                                img = cv2.putText(img, "looking side", (width_c // 4, height_c - 100), font, 2, (255, 255, 255), 2,
                                                  cv2.LINE_AA)
                                e_side_warn+=2.5
                                f_side+=1
                                e_blink = 0
                            elif pred[3] == 1:
                                img = cv2.putText(img, "looking side", (width_c // 4, height_c - 100), font, 2, (255, 255, 255), 2,
                                                  cv2.LINE_AA)
                                e_side_warn+=2.5
                                f_side+=1
                                e_blink = 0
                            elif pred[4] == 1:
                                img = cv2.putText(img, "looking up", (width_c // 4, height_c - 100), font, 2, (255, 255, 255), 2,
                                                  cv2.LINE_AA)
                                e_up_warn+=2
                                f_up+=1
                                e_blink = 0
                        break


        #face warnings

        # Moving away in z direction
        if dist_z > 3:
            img = cv2.putText(img, "warning", (width_c // 4, height_c - 100), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
            h_bf_warn += 1
            if h_bf_warn>3:
                f_moved_back +=1

        # Moving away in x direction
        if dist_x < 1.5 or dist_x > 3.3:
            img = cv2.putText(img, "warning", (width_c // 4, height_c - 100), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
            h_side_warn += 1
            if h_side_warn>4:
                f_moved_side+=1

        # Face not detected
        if len(faces) < 1:
            h_side_warn += 1
            if h_side_warn>3:
                img = cv2.putText(img, "show your face clearly", (width_c // 4, height_c - 50), font, 1,
                                  (255, 255, 255), 2,
                                  cv2.LINE_AA)
                f_turned_head+=1
        if ret == True:
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break
        with open("warnings.json", "w") as p:
            json.dump({"warning": warning},p)
        # Stop if escape key is pressed
        if cv2.waitKey(1) & 0xFF == ord('~'):
            #if the 'q' is pressed quit.'OxFF' is for 64 bit.[if waitKey==True] is condition
            break
    # Release the VideoCapture object
    cap.release()
    #return cred_score,time_up