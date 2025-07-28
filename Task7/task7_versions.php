<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Read Sensor Register</title>
    </head>
    <form action="" method="get">
        <input type="hidden" name="ver1"><br>
        <input type="hidden" name="ver2"><br>
    </form>
    <body>
        <?php
            $ver1 = $_GET["ver1"] ?? null;
            $ver2 = $_GET["ver2"] ?? null;
            
            if(isset($ver1) && $ver1 == 1){
                $output_ver1 = shell_exec(escapeshellcmd('python task6_pressure.py'));
                echo "<pre>".$output_ver1."</pre>"."\n";
            }
            if(isset($ver2) && $ver2 == 1){
                $request = "php task7_sensor.php";
                $output_ver2 = shell_exec(escapeshellcmd($request));
                echo "<pre>".$output_ver2."</pre>"."\n";
            }
        ?>
    </body>
</html>   
