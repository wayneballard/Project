<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial_scale=1.0">
        <title>GET method for shell_exec</title>
    </head>
    <body>
        <form action="" method="post">
            <input type="hidden" name="matrix" value="1"><br>
            <button type="submit">GET</button><br>
        </form>
        <?php
        $matrix_get = $_GET["matrix"] ?? null;
        $x = $_POST["x"] ?? null;
        $y = $_POST["y"] ?? null;
        $r = $_POST["r"] ?? null;
        $g = $_POST["g"] ?? null;
        $b = $_POST["b"] ?? null;
        
        if($_SERVER["REQUEST_METHOD"] == 'GET' && isset($matrix_get)){
            $output_get = shell_exec('python /home/pi/Project/SensorData.py');
            echo "<pre>".$output_get."</pre>";
        }
        else if($_SERVER["REQUEST_METHOD"] == 'POST'){
            $path = '/home/pi/Project/SensorData.py';
            if(isset($x) && ($x <= 0 || $x > 7)){
                echo "<pre>"."x is out of range. Please, enter the correct value within the range form 0 to 7"."</pre>";
            }
            if(isset($y) && ($y <= 0 || $y > 7)){
                echo "<pre>"."y is out of range. Please, enter the correct value within the range form 0 to 7"."</pre>";
            }
            if(isset($r) && ($r <= 0 || $r >= 255)){
                echo "<pre>"."Red is out of range. Please, enter the correct value within the range form 0 to 255"."</pre>";
            }
            if(isset($g) && ($g <= 0 || $g >= 255)){
                echo "<pre>"."Green is out of range. Please, enter the correct value within the range form 0 to 255"."</pre>";
            } 
            if(isset($b) && ($b <= 0 || $b >= 255)){
                echo "<pre>"."Blue is out of range. Please, enter the correct value within the range form 0 to 255"."</pre>";
            }
            else{
                $cmd = escapeshellcmd("python $path -x $x -y $y -r $r -g $g -b $b");
                $output_post = shell_exec($cmd);
                echo "<pre>".$output_post."</pre>";}
        }
        ?>
    </body>
</html>
