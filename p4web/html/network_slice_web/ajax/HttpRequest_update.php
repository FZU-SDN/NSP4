<?php
header('Content-type:text/json'); 
require_once "httpRequest.class.php";

$http = new httpRequeset;

//$url = "http://123.207.95.161/buyTogether/Login.php";
$url = "http://192.168.2.101:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:2/flow-node-inventory:table/1";
$post_data = array("userId" => "汪培侨", "password" => "123");
$post_data = json_encode($post_data);
//public function httpRequeset($url, $requesetType, $post_data)
$output = $http->httpRequeset($url,'GET',$post_data);
$output = json_decode($output,true);

//print_r($output['flow-node-inventory:table'][0]['id']);
//print_r($output['flow-node-inventory:table'][0]['flow'][0]['match']['ipv4-source']);
//print_r($output['flow-node-inventory:table'][0]['flow'][0]['match']['ipv4-destination']);
//print_r($output['flow-node-inventory:table'][0]['flow'][0]['match']['in-port']);
//print_r($output['flow-node-inventory:table'][0]['flow'][0]['match']['ethernet-match']['ethernet-source']['address']);
//print_r($output['flow-node-inventory:table'][0]['flow'][0]['match']['ethernet-match']['ethernet-destination']['address']);
//print_r($output['flow-node-inventory:table'][0]['flow'][0]['instructions']['instruction'][0]['apply-actions']['action'][0]['output-action']['output-node-connector']);


//$output = json_encode($output);
var_dump($output);

$arr = array();
$arr['id'] = $output['flow-node-inventory:table'][0]['id'];
$arr['in-port'] = $output['flow-node-inventory:table'][0]['flow'][0]['match']['in-port'];
$arr['src-mac'] = $output['flow-node-inventory:table'][0]['flow'][0]['match']['ethernet-match']['ethernet-source']['address'];
$arr['des-mac'] = $output['flow-node-inventory:table'][0]['flow'][0]['match']['ethernet-match']['ethernet-destination']['address'];
$arr['src-ip'] = $output['flow-node-inventory:table'][0]['flow'][0]['match']['ipv4-source'];
$arr['des-ip'] = $output['flow-node-inventory:table'][0]['flow'][0]['match']['ipv4-destination'];
$arr['action'] = "out-controller".$output['flow-node-inventory:table'][0]['flow'][0]['instructions']['instruction'][0]['apply-actions']['action'][0]['output-action']['output-node-connector'];

//$arr = json_encode($arr,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE);
$arr1 = array();
$arr1[0] = $arr;
$arr = json_encode($arr1,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE);

echo $arr;

//print_r($output);