from sense_hat import SenseHat

sense = SenseHat();

class Matrix(SenseHat):
    def init(self):
        self.x = [255, 0, 0]
        self.o = [255, 255, 255] 

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
matrix = Matrix();
matrix.create_pattern();

class IMU(SenseHat):
    def init(self):
        self.acceleration = [0,0,0]
        self.magnetometer = [0,0,0]
        self.gyroscope = [0,0,0]

    def get_raw_data(self):
        self.acceleration = self.get_accelerometer_raw();
        self.magnetometer = self.get_compass_raw();
        self.gyroscope = self.get_gyroscope_raw();

        x_accel = self.acceleration['x'];
        y_accel = self.acceleration['y'];
        z_accel = self.acceleration['z'];

        x_mag = self.magnetometer['x'];
        y_mag = self.magnetometer['y'];
        z_mag = self.magnetometer['z'];

        x_gyro = self.gyroscope['x'];
        y_gyro = self.gyroscope['y'];
        z_gyro = self.gyroscope['z'];


        print("acceleration in x direction={0}, acceleration in y direction={1}, acceleration in z direction={2}\n". format(x_accel, y_accel, z_accel));
        print("magnetic field strength in x direction={0}, magnetifc field strength in y direction={1},\
        magnetic field strength in z direction={2}\n". format(x_mag, y_mag, z_mag));
        print("agnular velocity in x direction={0}, agnular velocity in y direction={1}, agnular velocity in z direction={2}\n". format(x_gyro, y_gyro, z_gyro));


while True:
    imu = IMU();
    imu.get_raw_data();
