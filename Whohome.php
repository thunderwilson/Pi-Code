ping.php

<?php

$command = "python /home/t-wil/raspi/tomhome_graphical.py 2>&1";

$pid = popen( $command,"rw");

while( !feof( $pid ) )

{

echo fread($pid, 256);

flush();

ob_flush();

usleep(100000);

}

pclose($pid);

?>
