<?php
$url = "http://123.207.95.161/buyTogether/Login.php";
$post_data = array("userId" => "汪培侨", "password" => "123");
$requesetType = 'POST';

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
//        curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_DIGEST);
//        curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $requesetType);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
//curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json','Authorization: Basic '. base64_encode("admin:admin")));
curl_setopt($ch, CURLOPT_USERPWD, "admin:admin");
curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
//        curl_setopt($ch, CURLOPT_PROXYUSERPWD, 'admin:admin');
if ($requesetType == 'POST' || $requesetType == 'PUT') {
//    echo 'hh';
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
}
$output = curl_exec($ch);
//var_dump($output);
$output = json_decode($output,true);

$output = json_encode($output);
print_r($output);
// print_r($output['data']['userName']);
//var_dump($output['phoneNumber']);
curl_close($ch);
return $output;