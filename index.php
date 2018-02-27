<!--
// Challenge description:
// Our web administrator webmonster accidently deleted his public key.
// Luckily we provide a site to retrieve back his public key.
-->

<style>
    hr {
    display: block;
    height: 1px;
    border: 0;
    border-top: 1px solid #ccc;
    margin: 1em 0;
    padding: 0;
    }
</style>

<h2>Retrieve your public key</h2>
<h3>Please enter your id and token</h3>

<form method=post action=index.php>
	Id: <input name="id" type="text" size="40"/> <br>
	Token: <input name="token" type="text" size="80"/> <br>
	<input type="submit" value="OK" /> <br>
</form>

<?php

if( !empty($_POST['id']) && !empty($_POST['token']) ) {

    include('/usr/share/ext_func.php');

    echo "<hr/>";
    
    if(!check_id($_POST['id'])) {
    	echo "<div>Login incorrect.</div>";
    	exit;
    }

    $secret = get_secret($_POST['id']);
    $algo = 'sha256';
    
    $obs_login = substr_replace($_POST['id'], $secret, floor(strlen($_POST['id'])/2), 0);
    
    $hmac64 = hash_hmac($secret, base64_encode($obs_login), $algo, false);

    if($hmac64 !== $_POST['token']) {
    	echo "<div>Token incorrect.</div>";
    } else {
        echo "<h3>You got it!</h3><br>";
        echo get_pub_key($_POST['token']);
        echo "<br><br>";
        echo "<b>Try get the flag</b>: <a href='get_flag.php'>link</a>";
    }
}
?>
