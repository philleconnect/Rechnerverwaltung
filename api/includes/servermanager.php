<?php
    $curl = curl_init();
    $url = $client_request->servermanager->url;
    curl_setopt($curl, CURLOPT_POST, 1);
    if (isset($client_request->servermanager->data)) {
        curl_setopt($curl, CURLOPT_POSTFIELDS, $client_request->servermanager->data);
    }
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
    $client_response['servermanager'] = curl_exec($curl);
    curl_close($curl);
?>
