import webbrowser
import time
from frontpageUI import ks_code
from tester import predicter
from Adjustments import adjuster
from tab_detect import tab_detection
from exam_terminated import malpractice
from succesfull import complete
from time_up import time_over

def test():
    #Initia UI
    subject = ks_code()

    f_l = open('./csv_files/links.csv','r')
    line = f_l.readlines()
    line = line[-1]
    line = line.split(",")
    if subject == "Mathematics":
        line = line[0]
    elif subject == "Chemistry":
        line = line[1]
    else:
        line = line[2]
    f_l.close()

    t_l = open('./csv_files/time_in_seconds.csv','r')
    time_limit = t_l.readlines()
    time_limit = time_limit[-1]
    time_limit = time_limit.split(",")
    if subject == "Mathematics":
        time_limit = int(eval(time_limit[0]))
    elif subject == "Chemistry":
        time_limit = int(eval(time_limit[1]))
    else:
        time_limit = int(eval(time_limit[2]))
    t_l.close()

    #initial adjustments
    adjuster()

    #opening the form
    webbrowser.open(str(line))
    #starting the timer
    start_time = time.time()
    #starting the algorithm
    cred_score,time_up = predicter(start_time,time_limit)

    #Final Window
    if cred_score>75 and time_up:
        time_over(cred_score)
    elif cred_score<75:
        malpractice(cred_score)
    else:
        complete(cred_score)
