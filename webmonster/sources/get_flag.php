<?php

$acl_ok = ['127.0.0.1', '::1'];

if (in_array($_SERVER['REMOTE_ADDR'], $acl_ok)) {
	echo exec('cat /usr/share/flag');
} else {
    echo "Ops, still forbidden.";
}

?>
