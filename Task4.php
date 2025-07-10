<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial_scale=1.0">
        <title>POST method</title>
    </head>
    <body>
        <form action="" method="post">
            <label>POST/GET methods</label><br>
            <input type="hidden" name="post">
            <button type="submit">Send</button>
        </form>
        <?php
        if($_SERVER["REQUEST_METHOD"] == 'POST'){
            echo "OK-POST"."<br>";
        }
        else if($_SERVER["REQUEST_METHOD"] == 'GET'){
            echo "OK-GET"."<br>";
        }
        ?>
    </body>
</html>




