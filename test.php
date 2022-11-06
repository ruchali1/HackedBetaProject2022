<?php
    $command = escapeshellcmd('python test.py');
    $output = shell_exec($command);
    echo $output;
?>