<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Atmospheric Pressure Script</title>
    </head>
    <body>
        <?php
            $path = '/home/pi/Project/task6_pressure.py';
            if(file_exists($path)){
                $output = shell_exec("python $path");
                if($output !== null){
                    echo"<pre>"."Atmospheric pressure reading:".$output."</pre>";
                }
                else{
                    echo "<pre>"."An error occured, no output from the file. Please, try again."."</pre>";
                }
            }
        ?>
    </body>
</html>
