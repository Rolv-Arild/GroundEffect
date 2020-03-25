import serial
import threading
import queue
import time

class ArduinoCommunicator(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.reportingQueue = queue.Queue()
		self.speedLock = threading.Lock()
		self.comsLock = threading.Lock()
		#self.ser = serial.Serial("COM3", 9600)
		self.speeds = b"0 0 0 0 "  # do not change manually. use the setSpeeds command.
		self.nextSpeeds = b"0 0 0 0"

	def setSpeeds(self, intArray):  # put values between 0 and 70
		s = ""
		for val in intArray:
			s += str(val) + " "
		self.nextSpeeds = s.encode("ascii")

	def sendMsg(self, s):
		self.ser.write(s)
		return self.ser.readline().decode("utf-8")

	def readData(self, blocking=True):
		if not blocking and self.reportingQueue.empty():
			return None
		data = self.reportingQueue.get(True)
		return data

	def run(self):
		while True:
			self.speeds = self.nextSpeeds
			#returnMsg = self.sendMsg(self.speeds)  # distance in mm.
			returnMsg = "1 2 3 4 5"
			time.sleep(1)
			data = returnMsg.strip().split(" ")  # dist, w1, w2, w3, w4
			for val in self.speeds.decode("utf-8").split(" "):
				if val is not "":
					data.append(val)
			self.reportingQueue.put(data, True)
