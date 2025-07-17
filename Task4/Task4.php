<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial_scale=1.0">
        <title>POST method</title>
    </head>
    <body>
        <form action="" method="post">
            <label for="r">Red:</label><br>
            <input type="number" name="R" min="0" max="255" required><br>
            <label for="g">Green:</label><br>
            <input type="number" name="G" min="0" max="255" required><br>
            <label for="b">Blue:</label><br>
            <input type="number" name="B" min="0" max="255" required><br>
            <input type="hidden" name="x">
            <input type="hidden" name="y">
            <button type="submit">Send</button>
        </form>

        <?php
        $rgb_file = 'C:\Users\limok\OneDrive\Рабочий стол\RGB.txt';
        $matrix_file = 'C:\Users\limok\OneDrive\Рабочий стол\MATRIX.txt';
        $contents_json = file_get_contents($matrix_file);
        $lines = file($matrix_file, FILE_IGNORE_NEW_LINES);
        
        $x = $_GET["x"];
        $y = $_GET["y"];
        $R = $_POST["R"];
        $G = $_POST["G"];
        $B = $_POST["B"];
        if($_SERVER["REQUEST_METHOD"] == 'POST'){
            echo "OK-POST"."\n";
            if(isset($R) || isset($G) || isset($B)){
                if(($R <= 255) && ($R >=0 && $R != null) ||
                   ($G <= 255) && ($G >=0 && $G != null) ||
                   ($B <= 255) && ($B >=0 && $B != null)){
                    $rgbString = "R: $R, G: $G, B: $B\n";
                    if(file_exists($rgb_file)){
                        file_put_contents($rgb_file, $rgbString, FILE_APPEND);
                        echo "<pre>";
                        echo "Data saved to a file => ". $rgbString."\n";
                        echo "</pre>";
                        exit;
                }
            }
                else
                    echo "Values out of range. Please, try again\n";
            }
        }
        else if($_SERVER["REQUEST_METHOD"] == 'GET'){
            echo "OK-GET"."\n";
            $matrix = array_fill(0, 8, array_fill(0, 8, [0, 0, 0]));

            $data = json_decode($contents_json, true);
            $index = 0;

            for ($i = 0; $i < 8; $i++) {
                for ($j = 0; $j < 8; $j++) {
                    if (isset($data[$index])) {
                        $matrix[$i][$j] = $data[$index];
                    } else {
                        $matrix[$i][$j] = [0, 0, 0]; 
                    }
                    $index++;
                  
                }
            }
            
        echo "<pre>"; 

        foreach ($matrix as $r) {
            foreach ($r as $RGB) {
                echo "[" . implode(", ", $RGB) . "]";
            }
            echo "\n";            
        }

        if (isset($_GET["x"]) && isset($_GET["y"])) {
            echo "\nThe RGB values of pixel x = $x and y = $y is below:\n";
            print_r($matrix[$_GET["x"]][$_GET["y"]]);
        }

        echo "</pre>"; 
        exit;
        }
        ?>
    </body>
</html>




