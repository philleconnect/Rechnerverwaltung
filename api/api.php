<?php
    session_start();
    include "dbconnect.php";
    include "accessConfig.php";
    $client_request = json_decode($_POST['request']);
    $client_response = array();
    if (isset($client_request->login)) {
        include "includes/checklogin.php";
    } else {
        if ($_SESSION['user'] == null || $_SESSION['user'] == '') {
            echo 'ERR_NOT_AUTHORIZED';
        } else {
            if (isset($client_request->addaccount)) {
                include "includes/addaccount.php";
            } elseif (isset($client_request->deleteaccount)) {
                include "includes/deleteaccount.php";
            } elseif (isset($client_request->addadmin)) {
                include "includes/addadmin.php";
            } elseif (isset($client_request->deletemachine)) {
                include "includes/deletemachine.php";
            } elseif (isset($client_request->saveaccount)) {
                include "includes/saveaccount.php";
            } elseif (isset($client_request->saveconfig)) {
                include "includes/saveconfig.php";
            } elseif (isset($client_request->saveglobal)) {
                include "includes/saveglobal.php";
            } elseif (isset($client_request->savemachine)) {
                include "includes/savemachine.php";
            } elseif (isset($client_request->adminpwd)) {
                include "includes/adminpwd.php";
            } elseif (isset($client_request->logging)) {
                include "includes/log.php";
            } elseif (isset($client_request->transitload)) {
                include "includes/transitload.php";
            } elseif (isset($client_request->modifyaccount)) {
                include "includes/modifyaccount.php";
            } elseif (isset($client_request->accountexists)) {
                include "includes/accountexists.php";
            } elseif (isset($client_request->deleteadmin)) {
                include "includes/deleteadmin.php";
            } elseif (isset($client_request->changeadmin)) {
                include "includes/changeadmin.php";
            } elseif (isset($client_request->addgroupfolder)) {
                include "includes/addgroupfolder.php";
            } elseif (isset($client_request->deletegroupfolder)) {
                include "includes/deletegroupfolder.php";
            } elseif (isset($client_request->changegroupfolder)) {
                include "includes/changegroupfolder.php";
            } elseif (isset($client_request->servermanager)) {
                include "includes/servermanager.php";
            }
        }
    }
    echo json_encode($client_response);
?>
