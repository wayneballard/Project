<?php
   header('Content-Type: application/json');
   $set = 'i2cset -y 1 0x5c 0x20 0xB0';
   $low_part = 'i2cget -y 1 0x5c 0x28';
   $middle_part = 'i2cget -y 1 0x5c 0x29';
   $high_part = 'i2cget -y 1 0x5c 0x2A';
   
   $data = array();
   shell_exec(escapeshellcmd($set));
   
   $low_part_value = shell_exec(escapeshellcmd($low_part));
   $middle_part_value = shell_exec(escapeshellcmd($middle_part));
   $high_part_value = shell_exec(escapeshellcmd($high_part));
   if($low_part_value !== null | $middle_part_value !== null | $high_part_value !== null)
   {
       echo "Low part:".$low_part_value."Middle part: ".$middle_part_value."High part: ".$high_part_value;
   }
   else echo "An error occured. Please, try again.";
   $total_value = (hexdec($high_part_value) << 16) | (hexdec($middle_part_value) << 8) | (hexdec($low_part_value));
   $data["pressure_sensor"]["value"] = ($total_value / 4096);
   $data["pressure_sensor"]["units"] = "hPa";

   $json_data = json_encode($data, JSON_PRETTY_PRINT);

   echo $json_data;
?>
