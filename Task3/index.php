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
    $RGB = [$_GET["R"] ?? null, $_GET["G"] ?? null, $_GET["B"] ?? null] ;
    $R = $_GET["R"] ?? null;
    $G = $_GET["G"] ?? null;
    $B = $_GET["B"] ?? null;
    $RGB_by_element = array_map('htmlspecialchars', $RGB);
    
    
    $keys = array("x", "y", "pressure", "humidity", "temperature", "R", "G", "B");
    $arr = array();
    $file = 'C:\Users\limok\OneDrive\Рабочий стол\JSON.txt';
    if(isset($x) || isset($y) || isset($pressure) || isset($humidity) || isset($temperature)
            || isset($RGB)){         
        if(htmlspecialchars($x) == NULL){
           echo "<pre>". "Value of x coordinate of RGB matrix: "."Please, set the value". "<br>";
        }
        else if($_GET["x"] >= 8 || $_GET["x"] <= 1){
           echo "<pre>". "Value of x coordinate of RGB matrix: "."Value is out of range. Please, try again."."<br>";
        }
        else if($_GET["x"] <= 8 && $_GET["x"] >= 1){
            echo "<pre>". "Value of x coordinate of RGB matrix: ". htmlspecialchars($x);
        }
        
        if(htmlspecialchars($y) == NULL){
           echo "<pre>". "Value of y coordinate of RGB matrix: "."Please, set the value". "<br>";
        }
        else if($_GET["y"] >= 8 || $_GET["y"] <= 1){
           echo "<pre>". "Value of y coordinate of RGB matrix: "."Value is out of range. Please, try again."."<br>";
        }
        else if($_GET["y"] <= 8 && $_GET["y"] >= 1){
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
        if(($R <= 255 && $R >= 0) && ($G <= 255 && $G >= 0) && ($B <= 255 && $B >= 0)){
            echo "<pre>". "RGB: ". "R=".$R, ", G=".$G, ", B=".$B;
        }
        else if($RGB == NULL){
            echo "Please, set the value". "<br>";
        }
        else{
            echo "Value is out of range. Please, try again". "<br>";
        }
    }
    
   
    foreach($keys as $key){
        if(isset($_GET[$key])){
            if(($R <= 255 && $R > 0) || ($G <= 255 && $G > 0) || ($B <= 255 && $B > 0) ||
               ($x <= 8 && $x > 0) || ($y <= 8 && $y > 0) || 
               ($pressure <= 1260 && $pressure > 260) || ($humidity <= 100 && $humidity > 0) || ($temperature <= 120 && $temperature > -40))
            {
               $array["value"] = $_GET[$key];
               $arr[$key] = $array;
            }
            else 
                ;
        }
    }
   # print_r($array);
    
    $json_encoded = json_encode($arr, JSON_PRETTY_PRINT);
   # echo "JSON object output: " . "<pre>". $json_encoded . "<pre>";
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