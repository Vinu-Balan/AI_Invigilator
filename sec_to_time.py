
#x = 3600*2+1800+30
def sec_to_time(x):
    hr = x//3600
    if hr is 0:
        m = x//60
        sec = x%60
    else:
        hr = x//3600
        m = (x-(hr*3600))//60
        sec = (x-(hr*3600))%60
    return {"hour":hr,"minute":m,"sec":sec}