from sense_hat import SenseHat
import argparse 
import json

sense = SenseHat();
parser = argparse.ArgumentParser(prog='SenseHAT parser', description='Parses CMD arguments')

parser.add_argument('-r', '--red', action='store', type=int, help='Set the red color of RGB matrix')
parser.add_argument('-g', '--green', action='store', type=int, help='Set the green color of RGB matrix')
parser.add_argument('-b', '--blue', action='store', type=int, help='Set the blue color of RGB matrix')
parser.add_argument('-x', '--x', action='store',
                    type=int, help='Set the x coordinate of RGB matrix')
parser.add_argument('-y', '--y', action='store',
                    type=int, help='Set the y coordinate of RGB matrix')
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
            print("Please, set the coordinates between 8 and 1 in both x and y direction")

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
    def __init__(self):
        super().__init__()
        self._acceleration = [0,0,0]
        self._magnetometer = [0,0,0]
        self._gyroscope = [0,0,0]

    def get_imu_data(self):
        self._acceleration = self.get_accelerometer_raw();
        self._magnetometer = self.get_compass_raw();
        self._gyroscope  = self.get_gyroscope_raw();
        self._rgb_matrix = self.get_pixels();

        self.x_accel = self._acceleration['x'];
        self.y_accel = self._acceleration['y'];
        self.z_accel = self._acceleration['z'];

        self.x_mag = self._magnetometer['x'];
        self.y_mag = self._magnetometer['y'];
        self.z_mag = self._magnetometer['z'];

        self.x_gyro = self._gyroscope['x'];
        self.y_gyro = self._gyroscope['y'];
        self.z_gyro = self._gyroscope['z'];


    def print_imu_data(self):
        print("acceleration in x direction={0}, acceleration in y direction={1}, acceleration in z direction={2}\n". format(round(self.x_accel,5), round(self.y_accel,5), round(self.z_accel,5)));
        print("magnetic field strength in x direction={0}, magnetifc field strength in y direction={1},\
        magnetic field strength in z direction={2}\n". format(round(self.x_mag,5), round(self.y_mag,5), round(self.z_mag,5)));
        print("agnular velocity in x direction={0}, agnular velocity in y direction={1}, agnular velocity in z direction={2}\n". format(round(self.x_gyro,5), round(self.y_gyro,5), round(self.z_gyro,5)));


class Sensors(SenseHat):
    def __init__(self):
        super().__init__()
        self.temperature_raw = ' '
        self.humidity_raw = ' '
        self.pressure_raw = ' '
    
    def get_sensor_data(self):
        self.temperature_raw = self.get_temperature()
        self.humidity_raw = self.get_humidity()
        self.pressure_raw = self.get_pressure()

    def print_sensor_data(self):
        print("temperature:{0}, humidity:{1}, pressure{2}".format(self.temperature_raw, self.humidity_raw, self.pressure_raw))


class JSON(IMU, Sensors, Matrix):
    def __init__(self):
        super().__init__() 
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
        
        IMU = {"accelerometer":accel,
               "magnetometer": mag,
               "gyroscope":gyro}

        sensors = {"temperature_sensor":self.temperature_raw,
                   "humidity_sensor":self.humidity_raw,
                   "pressure_sensor":self.pressure_raw}

        json_object = {"SenseHAT": {"IMU":IMU, 
                                    "Sensors":sensors,
                                    "RGB matrix":self.rgb_matrix
                                    }}
        print(json.dumps(json_object, indent=4))
    
        

while True:


    json_instance = JSON()
    json_instance.get_matrix_data()
    json_instance.get_imu_data()
    json_instance.get_sensor_data()
    json_instance.print_raw_data_json();
    
