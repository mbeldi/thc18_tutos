<?php
function check_id($id) {
	if(strtolower($id) === "webmonster")
		return true;
	else
		return false;
}

function get_secret($id) {
	return 'sha256';
}

function get_pub_key($token) {
    $key = '<textarea cols=80 rows=6>-----BEGIN PUBLIC KEY-----
MHwwDQYJKoZIhvcNAQEBBQADawAwaAJhAMrZhFV8l+A5Qxoiatcn8MbUPvPUGEaf
GzdQSbIphD7p+Dsfl3OKwnT19h9AHyHxkT5LZLsxtVo405jA3+0AsTkvCIlxHESz
WeeXbGF/zHNPBuPpXCZHYJG1L0YueUE9tQIDAQAB
-----END PUBLIC KEY-----</textarea>';
    return $key;
}


?>
