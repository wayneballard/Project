from sense_hat import SenseHat
import argparse 
import json
import math
import time

sense = SenseHat();
time.sleep(1)
parser = argparse.ArgumentParser(prog='SenseHAT parser', description='Parses CMD arguments')

parser.add_argument('-r', '--red', action='store', type=int, help='Set the red color of RGB matrix')
parser.add_argument('-g', '--green', action='store', type=int, help='Set the green color of RGB matrix')
parser.add_argument('-b', '--blue', action='store', type=int, help='Set the blue color of RGB matrix')
parser.add_argument('-x', '--x', action='store',
                    type=int, help='Set the x coordinate of RGB matrix')
parser.add_argument('-y', '--y', action='store',
                    type=int, help='Set the y coordinate of RGB matrix')

parser.add_argument('-roll', '--roll_angle', action='store_true', help='Get the roll angle of IMU')
parser.add_argument('-pitch', '--pitch_angle', action='store_true', help='Get the pitch angle of IMU')
parser.add_argument('-yaw', '--yaw_angle', action='store_true', help='Get the yaw angle pf IMU')
parser.add_argument('-u', '--units', choices=["degrees", "radians", None], nargs='?', action='store', const=True, default=None, type=str, help='Change the unit of orientation')

parser.add_argument('-P', '--pressure_units', choices=["hPa", "mmHg", None], nargs='?', action='store', type=str, help='Change the pressure sensor units')
parser.add_argument('-T', '--temperature_units', choices=["C", "F", None], nargs='?', action='store', type=str, help='Change the temperature sensor units')
parser.add_argument('-H', '--humidity_units', choices=['%', 'decimal', None], nargs='?', action='store', type=str, help='Change the humidity sensor units')
args = parser.parse_args();




class Matrix(SenseHat):
    def __init__(self, x=0, y=0, red=0, green=0, blue=0):
        super().__init__()
        #self.x = [red, green, blue]
        self.o = [red, green, blue]
        self.x = x
        self.y = y
        self.red = red
        self.green = green
        self.blue = blue
    
    def get_matrix_data(self):
        self.rgb_matrix = self.get_pixels()
    
    def print_matrix_data(self):
        print(f"RGB Matrix:\n{self.rgb_matrix}");

    def set_pixel_matrix(self):
        if ((self.x is not None and self.y is not None) and 
            (self.x <= 7 and self.x >= 0 and self.y <= 7 and self.y >= 0)):
            
            if (((self.red is not None) and (self.red <= 255 and self.red >= 0)) or 
                ((self.green is not None) and (self.green <= 255 and self.green >= 0)) or 
                ((self.blue is not None) and (self.blue <= 255 and self.blue >= 0))):
                
                if (self.red is None):
                    self.red = 0
                if (self.green is None):
                    self.green = 0
                if (self.blue is None):
                    self.blue = 0
                sense.set_pixel(self.x, self.y, self.red, self.green, self.blue)

            elif(self.red is None and self.green is None and self.blue is None):
                self.red = 0
                self.green = 0
                self.blue = 0
                print("Since no arguments for colors were provided, all colors were set to zero")
            else:
                print("You provided the value out of range. Please, try again")
        else:
            print("Please, set the coordinates between 7 and 0 in both x and y direction")

    def create_pattern(self):
        X = self.x;
        O = self.o;
        question_mark = [
        O, O, O, X, X, O, O, O,
        O, O, X, O, O, X, O, O,
        O, O, O, O, O, X, O, O,
        O, O, O, O, X, O, O, O,
        O, O, O, X, O, O, O, O,
        O, O, O, X, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, X, O, O, O, O
        ]

        sense.set_pixels(question_mark)

matrix = Matrix(args.x, args.y, args.red, args.green, args.blue);
matrix.set_pixel_matrix()


class IMU(SenseHat):
    def __init__(self, roll=False, pitch=False, yaw=False, units=None):
        super().__init__()
        self._acceleration = [0,0,0]
        self._magnetometer = [0,0,0]
        self._gyroscope = [0,0,0]
        self._orientation = [0,0,0]
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
        self.units = units
        self.imu_orientation = {}

    def get_imu_data(self):
        self._acceleration = self.get_accelerometer_raw();
        self._magnetometer = self.get_compass_raw();
        self._gyroscope  = self.get_gyroscope_raw();
        self._rgb_matrix = self.get_pixels();
        self._orientation = self.get_orientation();

        self.x_accel = self._acceleration['x'];
        self.y_accel = self._acceleration['y'];
        self.z_accel = self._acceleration['z'];

        self.x_mag = self._magnetometer['x'];
        self.y_mag = self._magnetometer['y'];
        self.z_mag = self._magnetometer['z'];

        self.x_gyro = self._gyroscope['x'];
        self.y_gyro = self._gyroscope['y'];
        self.z_gyro = self._gyroscope['z'];

        self.roll_orient = self._orientation['roll'];
        self.pitch_orient = self._orientation['pitch'];
        self.yaw_orient  = self._orientation['yaw'];

    def print_imu_data_raw(self):
        print("acceleration in x direction={0}, acceleration in y direction={1}, acceleration in z direction={2}\n". format(round(self.x_accel,5), round(self.y_accel,5), round(self.z_accel,5)));
        print("magnetic field strength in x direction={0}, magnetifc field strength in y direction={1},\
        magnetic field strength in z direction={2}\n". format(round(self.x_mag,5), round(self.y_mag,5), round(self.z_mag,5)));
        print("agnular velocity in x direction={0}, agnular velocity in y direction={1}, agnular velocity in z direction={2}\n". format(round(self.x_gyro,5), round(self.y_gyro,5), round(self.z_gyro,5)));
    
    def print_imu_orientation(self):
        if not(self.roll or self.pitch or self.yaw):
            self.units = "Not set"
            self.imu_orientation["roll"] = "Not set"
            self.imu_orientation["pitch"] = "Not set"
            self.imu_orientation["yaw"] = "Not set"
            return
            
        print("IMU Orientation:\n") 
  
        if(self.units == 'degrees'):
            self.units = "\u00B0"
            if(self.roll is True):
                self.imu_orientation["roll"] = self.roll_orient
                print(f"Roll:{self.roll_orient:.4f}");
            if(self.pitch is True):
                self.imu_orientation["pitch"] = self.pitch_orient
                print(f"Pitch:{self.pitch_orient:.4f}");
            if(self.yaw is True):
                self.imu_orientation["yaw"] = self.yaw_orient
                print(f"Yaw:{self.yaw_orient:.4f}");
        elif(self.units == 'radians'):
            if(self.roll is True):
                self.imu_orientation["roll"] = math.radians(self.roll_orient)
                print(f"Roll:{math.radians(self.roll_orient):.4f}\n");
            if(self.pitch is True):
                self.imu_orientation["pitch"] = math.radians(self.pitch_orient)
                print(f"Pitch:{math.radians(self.pitch_orient):.4f}\n");
            if(self.yaw is True):
                self.imu_orientation["yaw"] = math.radians(self.yaw_orient)
                print(f"Yaw:{math.radians(self.yaw_orient):.4f}\n");
        elif(self.units is True):
            self.units = "Not set"
            if(self.roll is True):
                self.imu_orientation["roll"] = f"{self.roll_orient:.4f}"
                print(f"Roll:{self.roll_orient:.4f}");
            if(self.pitch is True):
                self.imu_orientation["pitch"] = f"{self.pitch_orient:.4f}"
                print(f"Pitch:{self.pitch_orient:.4f}");
            if(self.yaw is True):
                self.imu_orientation["yaw"] = f"{self.yaw_orient:.4f}"
                print(f"Yaw:{self.yaw_orient:.4f}");               
        else:
            self.units = "\u00B0"
            if(self.roll is True):
                self.imu_orientation["roll"] = f"{self.roll_orient:.4f}"
                print(f"Roll:{self.roll_orient:.4f}");
            if(self.pitch is True):
                self.imu_orientation["pitch"] = f"{self.pitch_orient:.4f}"
                print(f"Pitch:{self.pitch_orient:.4f}");
            if(self.yaw is True):
                self.imu_orientation["yaw"] = f"{self.yaw_orient:.4f}"
                print(f"Yaw:{self.yaw_orient:.4f}");

#imu = IMU(args.roll_angle, args.pitch_angle, args.yaw_angle, args.units)
#imu.get_imu_data();
#imu.print_imu_orientation();

class Sensors(SenseHat):
    def __init__(self, pressure_units=None, temperature_units=None, humidity_units=None):
        super().__init__()
        self.temperature_raw = ' '
        self.humidity_raw = ' '
        self.pressure_raw = ' '

        self.pressure_units = pressure_units
        self.temperature_units = temperature_units
        self.humidity_units = humidity_units
    
    def get_sensor_data(self):
        self.temperature_raw = self.get_temperature()
        self.humidity_raw = self.get_humidity()
        self.pressure_raw = self.get_pressure()

    def print_sensor_data(self):
        print("temperature:{0}, humidity:{1}, pressure{2}".format(self.temperature_raw, self.humidity_raw, self.pressure_raw))
    
    def match_units(self):
        if((self.pressure_units == "hPa" or self.pressure_units == "mmHg" or self.pressure_units == None) and
            (self.temperature_units == "C" or self.temperature_units == "F" or self.temperature_units == None) and
            (self.humidity_units == "%" or self.humidity_units == "decimal" or self.humidity_units == None)):
            match self.pressure_units:
                case "hPa":
                    self.pressure_raw = self.pressure_raw
                    print(self.pressure_raw)
                case "mmHg":
                    self.pressure_raw = self.pressure_raw * 0.75006157584566
                    print(self.pressure_raw)
                case None:
                    self.pressure_raw = self.pressure_raw #set default
                    self.pressure_units = "hPa"
            match self.temperature_units:
                case "C":
                    self.temperature_raw = self.temperature_raw
                    print(self.temperature_raw)
                case "F":
                    self.temperature_raw = self.temperature_raw * (9/5) + 32
                    print(self.temperature_raw)
                case None:
                    self.temperature_raw = self.temperature_raw #set default
                    self.temperature_units = "C"
            match self.humidity_units:
                case "%":
                    self.humidity_raw = self.humidity_raw
                    print(self.humidity_raw)
                case "decimal":
                    self.humidity_raw = self.humidity_raw / 100
                    print(self.humidity_raw)
                case None:
                    self.humidity_raw = self.humidity_raw #set default
                    self.humidity_units = "%"
            if(self.temperature_units == "C"): 
                self.temperature_units = "\u00B0C"
            print("pressure:{0} {1}, temperature:{2} {3}, humidity:{4} {5}".format(self.pressure_raw, self.pressure_units, self.temperature_raw, self.temperature_units, self.humidity_raw, self.humidity_units))



#sens = Sensors(args.pressure_units, args.temperature_units, args.humidity_units)
#sens.get_sensor_data()
#sens.match_units()

class JSON(Matrix, IMU, Sensors):
    def __init__(self, pressure_units=None, temperature_units=None, humidity_units=None, roll=False, pitch=False, yaw=False, units=None):
        Matrix.__init__(self)
        IMU.__init__(self, roll, pitch, yaw, units)
        Sensors.__init__(self, pressure_units, temperature_units, humidity_units)

    def print_raw_data_json(self):
        accel = {"x_accel":self.x_accel,
                "y_accel":self.y_accel,
                "z_accel":self.z_accel}
        mag = {"x_mag":self.x_mag,
                "y_mag":self.y_mag,
                "z_mag":self.z_mag}
        gyro = {"x_gyro":self.x_gyro,
                "y_gyro":self.y_gyro,
                "z_gyro":self.z_gyro}

        
        IMU = {"accelerometer_raw":{"value":accel,
                                    "units":"g"},
            "magnetometer_raw": {"value":mag, 
                                 "units":"\u03BCT"},
            "gyroscope_raw":{"value":gyro, 
                             "units":"\u00B0/s"},
            "orientation":{"value":self.imu_orientation,
                           "units":self.units}
        }

        sensors = {"temperature_sensor":{"value":self.temperature_raw,
                                        "units":self.temperature_units},
                "humidity_sensor":{"value":self.humidity_raw,
                                    "units":self.humidity_units},
                "pressure_sensor":{"value":self.pressure_raw,
                                    "units":self.pressure_units}
        }

        json_object = {"SenseHAT": {"IMU":IMU, 
                                    "Sensors":sensors,
                                    "RGB matrix":self.rgb_matrix
                                    }}
        print(json.dumps(json_object, ensure_ascii=False, indent=4))
        



json_instance = JSON(pressure_units = args.pressure_units, temperature_units = args.temperature_units, humidity_units = args.humidity_units,
                     roll=args.roll_angle, pitch=args.pitch_angle, yaw=args.yaw_angle, units=args.units)
json_instance.get_matrix_data()
json_instance.get_imu_data()
json_instance.print_imu_orientation()
json_instance.get_sensor_data()
json_instance.match_units()
json_instance.print_raw_data_json();
