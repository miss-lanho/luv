<?php
if (isset($_GET['ping'])) {
    header('Content-Type: application/json');
    echo json_encode(['status' => 'ok', 'time' => date('Y-m-d H:i:s')]);
    exit;
}
header('Content-Type: application/json');
if (!isset($_GET['username']) || !isset($_GET['password'])) {
    $data = array(
        'status' => 'false',
        'text' => 'Thiếu tham số username hoặc password'
    );
    echo json_encode($data);
    exit;
}
$username = $_GET['username'];
$password = $_GET['password'];

if (empty($username) || empty($password)) {
    $data = array(
        'status' => 'false',
        'text' => 'Username hoặc password không được để trống'
    );
    echo json_encode($data);
    exit;
}
$password = md5(urldecode($password));
$get_password = get_password($username, $password);
$get = json_decode(curl("https://sso.garena.com/api/prelogin?app_id=10100&account=".$username."&format=json&id=".microtime_float().""), true);
$pass = EnCode($password, hash('sha256', hash('sha256', $password.$get['v1']).$get['v2']));
$url = json_decode(curl("https://sso.garena.com/api/login?account=".$username."&password=".$pass."&format=json&id=".microtime_float()."&app_id=10100"), true);


    $ozTrungg = json_decode(curl1("https://account.garena.com/api/account/init?session_key=".$url['session_key']), true); 
    $data['status'] = "success";
    if($ozTrungg['user_info']['email_v'] == 0) $data['verimail'] = "Chưa xác thực mail";  
    if(!empty($ozTrungg['user_info']['email'])) $data['email'] = $ozTrungg['user_info']['email']; 
    if(!empty($ozTrungg['user_info']['username'])) $data['username'] = $ozTrungg['user_info']['username']; 
    if(!empty($ozTrungg['user_info']['mobile_no'])) $data['mobile_no'] = $ozTrungg['user_info']['mobile_no'];
    if(!empty($ozTrungg['user_info']['acc_country'])) $data['acc_country'] = $ozTrungg['user_info']['acc_country']; 
    if(!empty($ozTrungg['user_info']['uid'])) $data['uid'] = $ozTrungg['user_info']['uid'];       
    else 
    $data['status'] = "success";
    if($ozTrungg['user_info']['email_v'] == 1) $data['verimail'] = "Đã xác thực mail";  
    if(!empty($ozTrungg['user_info']['email'])) $data['email'] = $ozTrungg['user_info']['email']; 
    if(!empty($ozTrungg['user_info']['username'])) $data['username'] = $ozTrungg['user_info']['username']; 
    if(!empty($ozTrungg['user_info']['mobile_no'])) $data['mobile_no'] = $ozTrungg['user_info']['mobile_no'];
    if(!empty($ozTrungg['user_info']['acc_country'])) $data['acc_country'] = $ozTrungg['user_info']['acc_country']; 
    if(!empty($ozTrungg['user_info']['uid'])) $data['uid'] = $ozTrungg['user_info']['uid'];

echo json_encode($data);

function get_password($username, $passmd5)
{
    $get = json_decode(curl("https://sso.garena.com/api/prelogin?app_id=10100&account=".$username."&format=json&id=".microtime_float().""), true);
    $pass = EnCode($passmd5, hash('sha256', hash('sha256', $passmd5.$get['v1']).$get['v2']));
    return $pass;    
}

function EnCode($plaintext, $key)
{
    $chiperRaw = openssl_encrypt(hex2bin($plaintext), "AES-256-ECB", hex2bin($key), OPENSSL_RAW_DATA);
    return substr(bin2hex($chiperRaw), 0, 32);
}

function microtime_float()
{
    list($usec, $sec) = explode(" ", microtime());
    $return = ((float)$usec + (float)$sec);
    $return = str_replace(".", "", $return);
    return substr($return, 0, -1);
}

function curl($url)
{
    $tmpfname = dirname(__FILE__).'/cookie_garena.txt';
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'GET');
    curl_setopt($ch, CURLOPT_ENCODING, 'gzip, deflate');
    curl_setopt($ch, CURLOPT_COOKIEJAR, $tmpfname);
    $headers = array();
    $headers[] = 'Accept: application/json, text/plain, */*';
    $headers[] = 'Accept-Language: vi,en-US;q=0.9,en;q=0.8';
    $headers[] = 'Connection: keep-alive';
    $headers[] = 'Cookie: _ga=GA1.1.1950320156.1722745539; _ga_XB5PSHEQB4=GS1.1.1723723536.3.1.1723723600.0.0.0; token_session=0c10d14c8df2338e9ea3003a61d23e4eb01b14f463ce1dd88f2b35e40206f69c8336c13c498f7c7d36b1c820b8d4c9e3; _ga_G8QGMJPWWV=GS1.1.1723991467.12.0.1723991474.0.0.0; _ga_1M7M9L6VPX=GS1.1.1723999750.9.1.1723999753.0.0.0; datadome=9WVJeGQ6H3zeRLFWl7D2ty~unhM4hqyrqUBVsPHONcYhLW2KN4clfss~G5OqbtbxzUMWPEGz3vO4wIXVAUmRK5gn2cwvKsr0~OYXFrxP448Dsfj70edMykmLrfAdfPVT';
    $headers[] = 'Referer: https://sso.garena.com/universal/login?app_id=10100&redirect_uri=https%3A%2F%2Faccount.garena.com%2F&locale=vi-VN';
    $headers[] = 'Sec-Fetch-Dest: empty';
    $headers[] = 'Sec-Fetch-Mode: cors';
    $headers[] = 'Sec-Fetch-Site: same-origin';
    $headers[] = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36';
    $headers[] = 'Sec-Ch-Device-Memory: 8';
    $headers[] = 'Sec-Ch-Ua: \"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"';
    $headers[] = 'Sec-Ch-Ua-Arch: \"x86\"';
    $headers[] = 'Sec-Ch-Ua-Full-Version-List: \"Not)A;Brand\";v=\"99.0.0.0\", \"Google Chrome\";v=\"127.0.6533.120\", \"Chromium\";v=\"127.0.6533.120\"';
    $headers[] = 'Sec-Ch-Ua-Mobile: ?0';
    $headers[] = 'Sec-Ch-Ua-Model: \"\"';
    $headers[] = 'Sec-Ch-Ua-Platform: \"Windows\"';
    $headers[] = 'X-Datadome-Clientid: 9WVJeGQ6H3zeRLFWl7D2ty~unhM4hqyrqUBVsPHONcYhLW2KN4clfss~G5OqbtbxzUMWPEGz3vO4wIXVAUmRK5gn2cwvKsr0~OYXFrxP448Dsfj70edMykmLrfAdfPVT';
    $headers[] = 'Cache-Control: no-cache';
    
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, FALSE);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
    curl_setopt($ch, CURLOPT_TIMEOUT, 60);
    curl_setopt($ch, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);      
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 60);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);
    $result = curl_exec($ch);
    if (curl_errno($ch)) {
        echo 'Error:' . curl_error($ch);
    }
    curl_close($ch);
    return $result;
}

function curl1($url)
{
    $tmpfname = dirname(__FILE__).'/cookie_garena.txt';
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'GET');
    curl_setopt($ch, CURLOPT_ENCODING, 'gzip, deflate');
    curl_setopt($ch, CURLOPT_COOKIEJAR, $tmpfname);
    curl_setopt($ch, CURLOPT_COOKIEFILE, $tmpfname);
    $headers = array();
    $headers[] = 'Accept: application/json, text/plain, */*';
    $headers[] = 'Accept-Language: vi,en-US;q=0.9,en;q=0.8';
    $headers[] = 'Connection: keep-alive';
    $headers[] = 'Referer: https://sso.garena.com/universal/login?app_id=10100&redirect_uri=https%3A%2F%2Faccount.garena.com%2F&locale=vi-VN';
    $headers[] = 'Sec-Fetch-Dest: empty';
    $headers[] = 'Sec-Fetch-Mode: cors';
    $headers[] = 'Sec-Fetch-Site: same-origin';
    $headers[] = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36';
    $headers[] = 'Sec-Ch-Device-Memory: 8';
    $headers[] = 'Sec-Ch-Ua: \"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"';
    $headers[] = 'Sec-Ch-Ua-Arch: \"x86\"';
    $headers[] = 'Sec-Ch-Ua-Full-Version-List: \"Not)A;Brand\";v=\"99.0.0.0\", \"Google Chrome\";v=\"127.0.6533.120\", \"Chromium\";v=\"127.0.6533.120\"';
    $headers[] = 'Sec-Ch-Ua-Mobile: ?0';
    $headers[] = 'Sec-Ch-Ua-Model: \"\"';
    $headers[] = 'Sec-Ch-Ua-Platform: \"Windows\"';
    $headers[] = 'X-Datadome-Clientid: 9WVJeGQ6H3zeRLFWl7D2ty~unhM4hqyrqUBVsPHONcYhLW2KN4clfss~G5OqbtbxzUMWPEGz3vO4wIXVAUmRK5gn2cwvKsr0~OYXFrxP448Dsfj70edMykmLrfAdfPVT';
    $headers[] = 'Cache-Control: no-cache';
    
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, FALSE);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
    curl_setopt($ch, CURLOPT_TIMEOUT, 60);
    curl_setopt($ch, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);      
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 60);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);
    $result = curl_exec($ch);
    if (curl_errno($ch)) {
        echo 'Error:' . curl_error($ch);
    }
    curl_close($ch);
    
    return $result;       
}
