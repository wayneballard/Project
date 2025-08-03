from SensorData import Sensors
import serial
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import time
import numpy as np

s = Sensors(pressure_units="hPa", temperature_units="C", humidity_units="%");

temperature_samples = []
t = []
t_value = 0

while True:
	s.get_sensor_data();
	log_temp = s.temperature_raw;
	log_pres = s.pressure_raw;
	log_hum = s.humidity_raw;


	temperature_samples.append(log_temp)
	t.append(t_value)
	t_value = t_value + 1
	print(log_temp)
	print(t_value)
	print(temperature_samples)
	plt.ion()
	plt.clf()
	plt.title("Sensor Logger")
	plt.xlabel("Time[s]")
	plt.ylabel("Value")
	plt.plot(t, temperature_samples, '.', markersize=5)
	plt.show()
	plt.pause(0.0001)
	plt.savefig('plot.png')
