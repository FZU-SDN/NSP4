<?php

require_once "httpRequest.class.php";
// echo "jj";
$http = new httpRequeset;

//$url = "http://123.207.95.161/buyTogether/Login.php";
$url = "http://192.168.2.101:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:2/flow-node-inventory:table/0";
// $post_data = array("userId" => "汪培侨", "password" => "123");
$post_data = json_encode($post_data);
//public function httpRequeset($url, $requesetType, $post_data)
$output = $http->httpRequeset($url,'GET',$post_data);
//$output = json_decode($output);
//$output = json_encode($output);
//var_dump($output);
print_r($output);