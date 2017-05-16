<?php

// error_reporting(E_ALL);
error_reporting(0);

class httpRequeset{
    public function httpRequeset($url, $requesetType, $post_data)
    {
//        echo '<br />';
        //        echo $post_data;
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_DIGEST);
//        curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $requesetType);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json','Authorization: Basic '. base64_encode("admin:admin")));
        curl_setopt($ch, CURLOPT_USERPWD, "admin:admin");
        curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
//        curl_setopt($ch, CURLOPT_PROXYUSERPWD, 'admin:admin');
        if ($requesetType == 'POST' || $requesetType == 'PUT') {
//            echo "<br />";
//            echo $post_data;
            curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
        }
//        echo 'h';
        $output = curl_exec($ch);
        curl_close($ch);
//        var_dump($output);
        return $output;
    }
}