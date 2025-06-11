<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSON Output</title>
</head>
<body>
    <form action="server.php" method="post"></form>
    <label>JSON DATA IS BELOW:</label><br>
    <label>Choose your method:GET\POST</label><br>
    <input type="text" name="Method"><br>
    <input type ="submit" value="Accept"><br>
</body>
</html>
<?php 
echo $_GET["Accept"];
if(isset($_GET["Method"])){
    $entered = htmlspecialchars($var);
    echo "You entered: {$entered}";
    $return = strcmp($entered, "GET");
    if($return === TRUE){
        if (file_exists('C:\Users\limok\PycharmProjects\RaspberryProject\output.json')) {
            $contents = file_get_contents('C:\Users\limok\PycharmProjects\RaspberryProject\output.json');
            $decoded = json_decode($contents, true);
            $dump = var_dump($decoded);
            print_r($dump);
        } else {
            echo "File not found";
        }
    }
else{
    $var = NULL;
  }
}    
?>
