### webmonster (web / crypto / réseau) : hard

#### Description

```
http://localhost:8888
```
Our web administrator *webmonster* accidently deleted his public key.
Luckily we provide a website to retrieve back his public key.

A part of the source code `index.php` is provided
```
...
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
...
```

#### To run
```
docker pull izharr/webmonster
docker run -d --name <container_name> -p 8888:80 -p 2222:22 izharr/webmonster
```
*\*note: pay attention to the port mapping*


