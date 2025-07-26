<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GET method for shell_exec</title>
    </head>
    <body>
        <form action="" method="get">
            <input type="hidden" name="P"><br>
            <input type="hidden" name="T"><br> 
            <input type="hidden" name="H"><br> 
        </form>
        <?php
            $P = $_GET["P"];
            $T = $_GET["T"];
            $H = $_GET["H"];

            $path = '/home/pi/Project/SensorData.py';
            
            $string = "python $path";  
            if(file_exists($path)){
                if(isset($P) && ($P == "mmHg" || $P == "hPa")){
                    $string .= " -P $P";
                }
                if(isset($T) && ($T == "C" || $T == "F")){
                    $string .= " -T $T";
                }
                if(isset($H) && ($H == "%" || $H == "decimal")){
                    $string .= " -H $H";
                }
                $cmd = escapeshellcmd($string);
                $output = shell_exec($cmd);
                if($output !== null){
                    echo "<pre>"."Sensor reading:".$output."</pre>";
                }
            }
            else{
                echo "<pre>"."File does not exist. Please, try again."."</pre>";
            }
            
            
            
           
        ?>
    </body>
</html>
