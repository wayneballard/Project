from SensorData import Sensors, IMU
import serial
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
import numpy as np

s = Sensors(pressure_units="hPa", temperature_units="C", humidity_units="%");
imu = IMU(roll=True, pitch=True, yaw=True, units=None);

temperature_samples = []
pressure_samples = []
humidity_samples = []
roll_samples = []
pitch_samples = []
yaw_samples = []

t = []
t_value = 0

while True:
        s.get_sensor_data();
        imu.get_imu_data();

        time.sleep(0.5)
        log_temp = s.temperature_raw;
        log_pres = s.pressure_raw;
        log_hum = s.humidity_raw;

        log_roll = imu.roll_orient;
	log_pitch = imu.pitch_orient;
        log_yaw = imu.yaw_orient;


        temperature_samples.append(log_temp)
        pressure_samples.append(log_pres)
        humidity_samples.append(log_hum)
        roll_samples.append(log_roll)
        pitch_samples.append(log_pitch)
        yaw_samples.append(log_yaw)

        t.append(t_value)
        t_value = t_value + 0.5

        print(log_temp)
        print(t_value)
        print(temperature_samples)
        plt.ion()
        plt.clf()
        plt.subplot(2,2,1)
        plt.title("Temperature")
        plt.xlabel("Time[s]")
        plt.ylabel("Value")
        plt.plot(t, temperature_samples)
        plt.subplot(2,2,2)

        plt.title("Pressure")
        plt.xlabel("Time[s]")
        plt.ylabel("Value")
        plt.plot(t, pressure_samples, color='red')
	        plt.subplot(2,2,3)
        plt.title("Humidity")
        plt.xlabel("Time[s]")
        plt.ylabel("Value")
        plt.plot(t, humidity_samples, color='green')

        plt.subplot(2,2,4)
        plt.title("Roll, Pitch, Yaw")
        plt.xlabel("Time[s]")
        plt.ylabel("Value")
        plt.plot(t, roll_samples, t, pitch_samples, t, yaw_samples)

        plt.show()
        plt.pause(0.0001)
        plt.savefig('plot.png')

