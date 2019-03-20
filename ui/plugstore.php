<!DOCTYPE html>
<?php
    $page = 'Plugin-Store';
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
    <title>Plugin-Store - PhilleConnect Admin</title>
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
        <p style="font-family: Arial, sans-serif; font-size: 45px; text-transform: uppercase;"><b>PLUGIN</b>STORE</p>
        <p>Verfügbare PhilleConnect-Plugins:</p>
        <div class="datagrid">
            <table id="plugins">
                <thead>
                    <tr>
                        <th>Plugin:</th>
                        <th>Beschreibung:</th>
                        <th>Lizenz:</th>
                        <th>Aktion:</th>
                    </tr>
                </thead>
                <tbody id="tablecontent"></tbody>
            </table>
        </div>
    </div>
    <script>
        var navigation = responsiveNav("foo", {customToggle: ".nav-toggle"});
        function getAjaxRequest() {
            var ajax = null;
            ajax = new XMLHttpRequest;
            return ajax;
        }
        var plugins;
        function loadPlugins() {
            preloader.toggle("LADEN");
            request = getAjaxRequest();
            var url = "../api/api.php";
            var params = "request=" + encodeURIComponent(JSON.stringify({
                servermanager: {
                    url: "http://192.168.255.255:49100/repo"
                },
            }));
            request.onreadystatechange=stateChangedRepo;
            request.open("POST",url,true);
            request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            request.send(params);
            function stateChangedRepo() {
                if (request.readyState == 4) {
                    var response = JSON.parse(request.responseText);
                    plugins = JSON.parse(response.servermanager);
                    writeTable();
                }
            }
        }
        function writeTable() {
            document.getElementById().innerHTML = "";
            for (var i = 0; i < plugins.length; i++) {
                if (plugins[i].installed) {
                    var action = "Bereits installiert.";
                } else {
                    var action = "<a href=\"#\" onclick=\"installService(\"" + plugins[i].name + "\")\">Installieren</a>";
                }
                if (plugins[i].subscription) {
                    var license = "Benötigt SchoolConnect Abbonement.";
                } else {
                    var license = "Kostenlos (Open Source)";
                }
                document.getElementById().innerHTML += "<td>" + plugins[i].name + "</td><td>" + plugins[i].description + "</td><td>" + license + "</td><td>" + action + "</td>";
            }
            preloader.toggle();
        }
        function installService(name) {

        }
        loadPlugins();
    </script>
</body>
</html>
