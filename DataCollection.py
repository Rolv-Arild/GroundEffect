import ArduinoCommunicator
import Measurement

writer = Measurement.MeasurementWriter("measurements.csv")
arduino = ArduinoCommunicator.ArduinoCommunicator()
arduino.start()

i = 0
while True:
	arduino.setSpeeds([i, i, i, i])
	i += 2
	data = arduino.readData(blocking=True)
	dist = data[0]
	loads = data[1:5]
	speeds = data[5:]
	writer.write(dist, speeds, loads)
	writer.flush()

	print("dist: %d mm. loads: " % dist, end="")
	print(loads, end="")
	print(" speeds: ", end="")
	print(speeds)