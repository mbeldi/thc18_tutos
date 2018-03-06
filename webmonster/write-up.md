#### Write-up

Ce challenge présente un site permettant de récupérer la clé publique d'un utilisateur.
La formulaire accepte deux entrées `id` et `token`. On constate directement que l'id est `webmonster` d'après la description de challenge.

*index.php*
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

Et à partir de code source `index.php`, on constate que `token` est un **hash\_hmac** d'une chaîne de caractères.
On peut essayer directement d'aller à la page `get_flag.php` mais bien sûr que c'est interdit (ce n'est pas si facile).
Le premier objectif est de récupérer alors la clé publique `webmonster`.
Il faut passer la vérification `token`.
Si on réussit à trouver la valeur `$secret`, c'est facile à refaire chaque instruction pour trouver le token.
En fait, pour réussir la vérification de token, il faut juste regarder comment fonctionne la fonction php `hash_hmac`.

```
string hash_hmac ( string $algo , string $data , string $key [, bool $raw_output = false ] )
```
Dans ce challenge, le secret et l'algoritme sont inversés.
Comme `$algo='sha256'` (qui est le secret), par une simple assumption, on sait que `$secret='sha256'` (qui est l'algorithme utilisé).
Maintenant on connait le secret et l'algo, donc on refait chaque instruction. Voici un exemple de code sur python.
```
import base64, hashlib, hmac
login = 'webmonster'
secret = 'sha256'
# substr_replace
obs_login = login[:len(login)/2] + secret + login[len(login)/2:]
# hash_hmac w/ sha256
hmac64 = hmac.new(secret, base64.b64encode(obs_login), hashlib.sha256)
print 'id = ' + login + '\ntoken = ' + hmac64.hexdigest()
```
On trouve alors,
```
id = webmonster
token = 16a69f056965ba5f763033797d7a42b6c983d0121a494b3d610f99e0aa41d7f6
```
On réussit la première étape et on ne peut pas toujours accéder la page `get_flag.php`.
On récupère ensuite la clé publique d'utilisateur `webmonster`.
On a la clé publique mais on ne peut rien faire.
On essaie alors d'inspecter cette clé publique en utilisant cette commande
```
openssl rsa -in <pub_key> -pubin -text -modulus
```
On constate que c'est une clé de 768 bits. Elle est plus petite que la taille conseillée 1024 bits.
Comme on a la valeur `N`, on regarde si elle est factorisée sur le site factordb.com
afin de trouver les valeurs `p` et `q` (*lisez une explication simple de RSA https://www.pagedon.com/rsa-explained-simply/programming*).

Voila, jackpot! `N` est factorisée. On a toutes les valeurs nécessaires pour créer la clé privée correspondante.
```
N: cad984557c97e039431a226ad727f0c6d43ef3d418469f1b375049b229843ee9f83b1f97738ac274f5f61f401f21f191
   3e4b64bb31b55a38d398c0dfed00b1392f0889711c44b359e7976c617fcc734f06e3e95c26476091b52f462e79413db5
p: d982ec7b440e2869d2535e51f91bacc3eb6eba042e106e6f875c3d17e53db65fffd6e4e9a36084ce60f83d754dd7f701 
q: eebe6dd23ce7e99c0e2249fecc4418c34af74e418bfa714c3791828414ab18f32fd7e093062a49b030225cc845f99ab5
e: 10001
```

On peut utiliser plusieurs outils sur le net pour construire la clé privée, par exemple `rsatool` (https://github.com/ius/rsatool).
Dans cet exemple, on utilise un code python trouvé ici https://gist.github.com/gnpar/89224485386acf83ec01daf7503b2c3b

```
python gen-key.py p q e > asn1.conf
openssl asn1parse -genconf asn1.conf  -out key.der
openssl rsa -in key.der -inform der -text -check
```
```
-----BEGIN RSA PRIVATE KEY-----
MIIBywIBAAJhAMrZhFV8l+A5Qxoiatcn8MbUPvPUGEafGzdQSbIphD7p+Dsfl3OKwnT19h9AHyHx
kT5LZLsxtVo405jA3+0AsTkvCIlxHESzWeeXbGF/zHNPBuPpXCZHYJG1L0YueUE9tQIDAQABAmB0
DeSHYEQoNbqtXhmQRTqdFtt5dtP4u5i/mcDAHL6bnBK4CMgGg9HjRsFseawWKHTyjKYQwbl+Xh/6
6VclzgxrAxw+GIsXGHp5OzIsxABMVo52ybJYVC6iotbs1GL/9AECMQDZgux7RA4oadJTXlH5G6zD
6266BC4Qbm+HXD0X5T22X//W5OmjYITOYPg9dU3X9wECMQDuvm3SPOfpnA4iSf7MRBjDSvdOQYv6
cUw3kYKEFKsY8y/X4JMGKkmwMCJcyEX5mrUCMQCXWi353DJJ1tDe6Bv8TlCah+GlmLEBCAedVgbA
8OhPVl+tBd65q7jd7sXt5glDxQECMQCnEe/8Xc7U9fYWHL4H5+eEUuO5ibkRK1Pw1w0ErQoGzbe/
VFLOz6z9dNG3KBd/0rkCMH6J+q8/eK2Vi+vGXc92zSHplI4rshqBvhCfrDcrtBuu7b38Z1dz+ky1
xc4ZO17bnA==
-----END RSA PRIVATE KEY-----
```

On voit que le serveur ssh tourne sur le port `2222` (attention au mapping de port) et on essaie alors de se connecter.
```
$ ssh -i <priv_key> webmonster@localhost -p 2222
This service allows sftp connections only.
Connection to localhost closed.
```
*-i: préciser la clé privée à utiliser*

*note: faites attention à la version du client ssh (OpenSSH), la version récente n'accepte plus la clé de taille moins de 1024 bits.*

Malheureusement, la connexion ssh est interdit mais pas sftp.
On se connecte en sftp afin de télécharger le code source `get_flag.php`.
```
$acl_ok = ['127.0.0.1', '::1'];
if (in_array($_SERVER['REMOTE_ADDR'], $acl_ok)) {
	echo exec('cat /usr/share/flag');
} else {
    echo "Ops, still forbidden.";
}
```
On comprend maintenant qu'il faut se connecter à partir de `localhost` pour récupérer le flag.
Il reste alors de faire une redirection ssh (on peut toujours faire la redirection même si la connexion ssh est interdit pour cet utilisateur).
```
ssh -i <priv_key> -N -L 8888:localhost:80 webmonster@localhost -p 2222
```
*-N: forcer ssh de faire seulement la redirection de port*  
*-L: redirection ssh*

On visite `http://localhost:8888/get_flag.php` et récupère le flag! `THC18{M0nsterISzSc4ry!}`

