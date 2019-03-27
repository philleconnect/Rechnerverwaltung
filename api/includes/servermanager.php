<?php
    $pararray = (array) $client_request->servermanager->data;
    $options = array(
        'http' => array(
            'header' => "Content-type: application/x-www-form-urlencoded\r\n",
            'method' => 'POST',
            'content' => http_build_query($pararray)
        )
    );
    $context = stream_context_create($options);
    $client_response['servermanager'] = file_get_contents($client_request->servermanager->url, false, $context);
?>
