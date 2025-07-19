<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSON Output</title>
</head>
<body>
    <form action="" method="get">
        <label>JSON DATA IS BELOW:</label><br>
        <input type="hidden" name="x"><br>
        <input type="hidden" name="y"><br>
        <input type="hidden" name="pressure"><br>
        <input type="hidden" name="humidity"<br>
        <input type="hidden" name="temperature"><br>
        <input type="hidden" name="selected_sensor"
        <!input type="hidden" value="submit">
    </form>
    
    <?php
    $array = array();
    
    $x = $_GET["x"] ?? null;
    $y = $_GET["y"] ?? null;
    
    $pressure = $_GET["pressure"] ?? null;
    $humidity = $_GET["humidity"] ?? null;
    $temperature = $_GET["temperature"] ?? null;
    
    $R = $_GET["R"] ?? null;
    $G = $_GET["G"] ?? null;
    $B = $_GET["B"] ?? null;
    $RGB = [$R, $G, $B];
    $RGB_by_element = array_map('htmlspecialchars', $RGB);
    
    $gyro_x = $_GET["gyro_x"] ?? null;
    $gyro_y = $_GET["gyro_y"] ?? null;
    $gyro_z = $_GET["gyro_z"] ?? null;
    $gyro = [$gyro_x, $gyro_y, $gyro_z];
    
    $magnet_x = $_GET["magnet_x"] ?? null;
    $magnet_y = $_GET["magnet_y"] ?? null;
    $magnet_z = $_GET["magnet_z"] ?? null;
    $magnet = [$magnet_x, $magnet_y, $magnet_z];
    
    $accel_x = $_GET["accel_x"] ?? null;
    $accel_y = $_GET["accel_y"] ?? null;
    $accel_z = $_GET["accel_z"] ?? null;
    $accel = [$accel_x, $accel_y, $accel_z];
    
    
    $keys = array("x", "y", "pressure", "humidity", "temperature", "R", "G", "B",
                  "gyro_x", "gyro_y", "gyro_z", "magnet_x", "magnet_y", "magnet_z",
                  "accel_x", "accel_y", "accel_z");
    $sensor_keys = array("IMU", "Sensors", "RGB matrix");
    
    $IMU = array();
    $Sensors = array();
    $RGB_matrix = array();
    
    $arr = array();
    $file = 'C:\Users\limok\OneDrive\Рабочий стол\JSON.txt';
    if(isset($x) || isset($y) || isset($pressure) || isset($humidity) || isset($temperature)
            || isset($RGB) || isset($gyro) || isset($magnet) || isset($accel)){         
        if(htmlspecialchars($x) == NULL){
           echo "<pre>". "Value of x coordinate of RGB matrix: "."Please, set the value". "<br>";
        }
        else if($x > 8 || $x < 1){
           echo "<pre>". "Value of x coordinate of RGB matrix: "."Value is out of range. Please, try again."."<br>";
        }
        else if($x <= 8 && $x >= 1){
            echo "<pre>". "Value of x coordinate of RGB matrix: ". htmlspecialchars($x);
        }
        
        if(htmlspecialchars($y) == NULL){
           echo "<pre>". "Value of y coordinate of RGB matrix: "."Please, set the value". "<br>";
        }
        else if($y > 8 || $y < 1){
           echo "<pre>". "Value of y coordinate of RGB matrix: "."Value is out of range. Please, try again."."<br>";
        }
        else if($y <= 8 && $y >= 1){
            echo "<pre>". "Value of y coordinate of RGB matrix: ". htmlspecialchars($y);
        }
        
        
        echo "<pre>". "Pressure: ". htmlspecialchars($pressure);
        if(htmlspecialchars($pressure) == NULL){
           echo "Please, set the value". "<br>";
        }
        echo "<pre>". "Humidity: ". htmlspecialchars($humidity);
        if(htmlspecialchars($humidity) == NULL){
           echo "Please, set the value". "<br>";
        }
        echo "<pre>". "Temperature: ". htmlspecialchars($temperature);
        if(htmlspecialchars($temperature) == NULL){
           echo "Please, set the value". "<br>";
        }
        
        
        if(is_null($R) && is_null($G) && is_null($B)){
            echo "<pre>". "RGB: "."Please, set the value". "<br>";
        }
        else if(($R <= 255 && $R >= 0) && ($G <= 255 && $G >= 0) && ($B <= 255 && $B >= 0)){
            echo "<pre>". "RGB: ". "R=".$R, ", G=".$G, ", B=".$B;
        }
        else if(($R > 255 || $R < 0) || ($G > 255 || $G <0) || ($B > 255 || $B < 0)){
            echo "<pre>". "RGB: "."Value is out of range. Please, try again". "<br>";
        }
        
        
        if(is_null($gyro_x) && is_null($gyro_y) && is_null($gyro_z)){
            echo "<pre>". "Gyroscope: "."Please, set the value". "<br>";
        }
        else if((floatval($gyro_x) <= 245 && floatval($gyro_x) >= -245) && (floatval($gyro_y) <= 245 && floatval($gyro_y) >= -245) && (floatval($gyro_z) <= 245 && floatval($gyro_z) >= -245)){
            echo "<pre>". "Gyroscope: ". "x=".$gyro_x, ", y=".$gyro_y, ", z=".$gyro_z;
        }
        else if((floatval($gyro_x) > 245 || floatval($gyro_x) < -245) || (floatval($gyro_y) > 245 || floatval($gyro_y) < -245) || (floatval($gyro_z) > 245 || floatval($gyro_z) < -245)){
            echo "<pre>"."Gyroscope: "."Value is out of range. Please, try again". "<br>";
        }
        
        
        if(is_null($magnet_x) && is_null($magnet_y) && is_null($magnet_z)){
            echo "<pre>". "Magnetometer: "."Please, set the value". "<br>";
        }        
        else if((floatval($magnet_x) <= 400 && floatval($magnet_x) >= -400) && (floatval($magnet_y) <= 400 && floatval($magnet_y) >= -400) && (floatval($magnet_z) <= 400 && floatval($magnet_z) >= -400)){
            echo "<pre>". "Magnetometer: ". "x=".$magnet_x, ", y=".$magnet_y, ", z=".$magnet_z;
        }
        else if((floatval($magnet_x) > 400 || floatval($magnet_x) < -400) || (floatval($magnet_y) > 400 || floatval($magnet_y) < -400) || (floatval($magnet_z) > 400 || floatval($magnet_z) < -400)){
            echo "<pre>"."Magnetometer: "."Value is out of range. Please, try again". "<br>";
        }
        
        
        if(is_null($accel_x) && is_null($accel_y) && is_null($accel_z)){
            echo "<pre>". "Accelerometer: "."Please, set the value". "<br>";
        }        
        else if((floatval($accel_x) <= 2 && floatval($accel_x) >= -2) && (floatval($accel_y) <= 2 && floatval($accel_y) >= -2) && (floatval($accel_z) <= 2 && floatval($accel_z) >= -2)){
            echo "<pre>". "Accelerometer: ". "x=".$magnet_x, ", y=".$magnet_y, ", z=".$magnet_z;
        }
        else if((floatval($accel_x) > 2 || floatval($accel_x) < -2) || (floatval($accel_y) > 2 || floatval($accel_y) < -2) || (floatval($accel_z) > 2 || floatval($accel_z) < -2)){
            echo "<pre>"."Accelerometer: "."Value is out of range. Please, try again". "<br>";
        }
    }
    
   
    foreach($keys as $key){
        if(isset($_GET[$key])){

               $array["value"] = $_GET[$key];
               $arr[$key] = $array;
                if (in_array($key, ["R", "G", "B"]) && ($_GET[$key] <= 255 && $_GET[$key] > 0) ||
                    in_array($key, ["x", "y"]) && ($_GET[$key] <= 8 && $_GET[$key] > 0)) {
                       $RGB_matrix["RGB matrix"][$key] = ["value" => $_GET[$key]];
                } 
                else if(in_array($key, ["temperature"]) && ($_GET[$key] <= 120 && $_GET[$key] > -40) ||
                        in_array($key, ["humidity"]) && ($_GET[$key] <= 100 && $_GET[$key] > 0) ||
                        in_array($key, ["pressure"]) && ($_GET[$key] <= 1260 && $_GET[$key] > 260)) {
                         $Sensors["Sensors"][$key] = ["value" => $_GET[$key]];
                }
                else if(in_array($key, ["gyro_x", "gyro_y", "gyro_z"]) && ($_GET[$key] <=245 && $_GET[$key] >= -245) ||
                        in_array($key, ["magnet_x", "magnet_y", "magnet_z"]) && ($_GET[$key] <= 400 && $_GET[$key] >= -400) ||
                        in_array($key, ["accel_x", "accel_y", "accel_z"]) && ($_GET[$key] <=2 && $_GET[$key] >= -2)) {
                         $IMU["IMU"][$key] = ["value" => $_GET[$key]];
                }                
                $total = array_merge($RGB_matrix, $Sensors, $IMU);
        }
    }

    
    $json_encoded = json_encode($total, JSON_PRETTY_PRINT);
    if(file_exists($file)){
        if($json_encoded == '[]'){
            $json_encoded = NULL;
        }
        else{
            $contents = file_get_contents($file);
            file_put_contents($file, $json_encoded. $contents);
        }
    }
    else{
        echo "File doesn ot exist. Please try again.";
    }
    $contents_prepended = file_get_contents($file);
    echo "<pre>". "Contents of the file are below ". "<pre>" .htmlspecialchars($contents_prepended), "<pre>";
    
    class Sensors{
        public $barometer;
        public $thermometer;
        public $humidity_sensor;
        private $selected_sensor;
        private $selected_value;
        public $data;
        
        public function __construct($name){
            $this -> barometer = rand(260,1260);
            $this -> thermometer = rand(0, 100);
            $this -> humidity_sensor = rand(0, 100);
            
            $name = strtolower($name);
            if($name == 'barometer'){
               $this -> selected_sensor = 'barometer';
               $this -> selected_value = $this-> barometer;
            }
            else if($name =='thermometer'){
               $this -> selected_sensor = 'thermometer';
               $this -> selected_value = $this -> thermometer;
            }
            else if($name  == 'humidity sensor'){
               $this -> humidity_sensor = 'humidity_sensor';
               $this -> selected_value = $this -> humidity_sensor;
            }
            else
                $this -> selected_sensor = NULL;
        }
        
        public function choose_sensor(){
        
            if($this -> selected_sensor && property_exists($this, $this->selected_sensor)){
                echo "Chosen sensor: ".$this-> selected_sensor."=>";
                echo "Value: ".$this-> selected_value."<br>";
                return ["Chosen sensor" => $this-> selected_sensor,
                        "Value" => $this-> selected_value];
                
            }
            else if($this -> selected_sensor == NULL){
                echo "All sensor data is provided below: "."<br>";
                echo 'Barometer: ' ; echo $this -> barometer."<br>";
                echo 'Thermometer: '; echo $this ->  thermometer."<br>";
                echo 'Humidity sensor: '; echo $this -> humidity_sensor."<br>";
                return ['Barometer: ' => $this -> barometer,
                        'Thermometer: ' =>  $this ->  thermometer,
                        'Humidity sensor: ' => $this -> humidity_sensor];

            }
            else{
                echo 'The specified sensor was not found. Please try again.'. "<br>";
            }
        }
        
    }
    
    class JSON extends Sensors{
        protected $json;
        public function __construct($name){
            parent::__construct($name);
            $this -> json = $this->choose_sensor();
        }
        public function encode_to_json(){
            $data = json_encode($this -> json, JSON_PRETTY_PRINT);
            var_dump($data);
        }    
    }
    
    function limit_file($contents){
        $count = 0;
        $arr = array();
        for($i = 0; $i < strlen($contents); $i++){
                if($contents[$i] == '}'){
                    $count = $count + 1;
                }
                $arr[$count] = $i;
            }
        echo "Limited output of the file up to 10 JSON data structures<br>";
        for($j = 0; $j < $arr[10]; $j++){
                echo $contents[$j];
            }
        }
    

 
    $selected_sensor = $_GET["selected_sensor"] ?? null;
    #$sensor1 = new Sensors($selected_sensor); 
    #$sensor1 ->choose_sensor();
    $sensor1_json = new JSON($selected_sensor);
    $sensor1_json -> encode_to_json();
    limit_file($contents);
    ?>
</body>
</html>
