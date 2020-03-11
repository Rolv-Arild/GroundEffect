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
i=0
while True:
    returnMsg = sendMsg(msg)  # distance in mm.
    data = returnMsg.strip().split(" ")
    dist = data[0]
    loads = data[1:]
    print("dist: " + dist + "\tloads: ", end="")
    print(loads)
    setSpeeds([i, i, i, i])
    i += 1