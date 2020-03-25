import serial

def setSpeeds(intArray):  # put values between 20 and 180
    global msg
    s = ""
    for val in intArray:
        s += str(val) + " "
    msg = s.encode("ascii")


def sendMsg(s):
    ser.write(s)
    return ser.readline().decode("utf-8")


ser = serial.Serial("COM3", 9600)
msg = b"20 20 20 20 "
val = 71
# ta i mot 0 til 70
while True:
    returnMsg = sendMsg(msg)  # distance in mm.
    data = returnMsg.strip().split(" ")
    dist = data[0]
    loads = data[1:]
    print("dist: " + dist + "\tloads: ", end="")
    print(loads)
    setSpeeds([val, val, val, val])
    #val += 2
