<!DOCTYPE html>
<?php
    $page = 'Servermanagement';
    include "../api/dbconnect.php";
    session_start();
    if ($_SESSION['user'] == null || $_SESSION['user'] == '' || ($_SESSION['timeout'] + 1200) < time()) {
        header("Location: nologin.php");
    } elseif ($_SESSION['type'] != '1' && $_SESSION['type'] != '3') {
        header("Location: restricted.php");
    } else {
        $_SESSION['timeout'] = time();
        include "menue.php";
        include "../api/accessConfig.php";
    }
?>
<html lang="de">
<head>
    <title>Servermanagement - PhilleConnect Admin</title>
    <?php include "includes.php"; ?>
</head>
<body>
    <?php include "assets/preloader.php"; ?>
    <div role="navigation" id="foo" class="nav-collapse">
        <div class="top">
            <img src="ressources/img/logo.png">
            <li><b>PHILLE</b>CONNECT</li>
        </div>
        <ul>
            <?php
                echo $menu;
            ?>
        </ul>
        <?php include "assets/timeout.php"; ?>
    </div>
    <div role="main" class="main">
        <a href="#nav" class="nav-toggle">Menu</a>
        <noscript>
            <p>Dein Browser unterstützt kein JavaScript oder JavaScript ist ausgeschaltet. Du musst JavaScript aktivieren, um diese Seite zu verwenden!</p>
        </noscript>
        <p style="font-family: Arial, sans-serif; font-size: 45px; text-transform: uppercase;"><b>SERVER</b>MANAGEMENT</p>
        <p>Installierte Services:</p>
        <div class="datagrid">
            <table>
                <thead>
                    <tr>
                        <th>Status:</th>
                        <th>Name:</th>
                        <th>Version:</th>
                        <th>Einstellung:</th>
                        <th>Aktualisierung:</th>
                        <th>Aktionen:</th>
                    </tr>
                </thead>
                <tbody id="tablecontent">

                </tbody>
            </table>
        </div>
    </div>
    <script>
        var navigation = responsiveNav("foo", {customToggle: ".nav-toggle"});
        var services = null;
        function getAjaxRequest() {
            var ajax = null;
            ajax = new XMLHttpRequest;
            return ajax;
        }
        function getServices() {
            request = getAjaxRequest();
            var url = "../api/api.php";
            var params = "request=" + encodeURIComponent(JSON.stringify({
                servermanager: {
                    url: "http://192.168.255.255:49100/status",
                    data: []
                },
            }));
            request.onreadystatechange=stateChangedServices;
            request.open("POST",url,true);
            request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            request.send(params);
            function stateChangedServices() {
                if (request.readyState == 4) {
                    var response = JSON.parse(request.responseText);
                    services = response.servermanager;
                }
            }
        }
        function writeTable() {

        }
    </script>
</body>
</html>
