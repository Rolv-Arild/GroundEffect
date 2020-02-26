import serial


def sendMsg(s):
    ser.write(s)
    return ser.readline().decode("utf-8")


ser = serial.Serial("COM3", 9600)
while True:
    returnMsg = sendMsg(b"100")  # distance in mm.
    data = returnMsg.strip().split(" ")
    dist = data[0]
    loads = data[1:]
    print("dist: " + dist + "\tloads: ", end="")
    print(loads)