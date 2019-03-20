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
                <tbody id="tablecontent"></tbody>
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
            preloader.toggle("LADEN");
            request = getAjaxRequest();
            var url = "../api/api.php";
            var params = "request=" + encodeURIComponent(JSON.stringify({
                servermanager: {
                    url: "http://192.168.255.255:49100/status",
                    data: {}
                },
            }));
            request.onreadystatechange=stateChangedServices;
            request.open("POST",url,true);
            request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            request.send(params);
            function stateChangedServices() {
                if (request.readyState == 4) {
                    var response = JSON.parse(request.responseText);
                    services = JSON.parse(response.servermanager);
                    writeTable();
                }
            }
        }
        function writeTable() {
            document.getElementById("tablecontent").innerHTML = "";
            for (var i = 0; i < services.length, i++) {
                if (services[i].status) {
                    var status = "<i class=\"f7-icons\" style=\"color: green;\">play_round_fill</i>";
                    var runAction = "<a href=\"#\" onclick=\"runService(\"" + services[i].name + "\", false)\">Deaktivieren</a>";
                } else {
                    var status = "<i class=\"f7-icons\" style=\"color: red;\">close_round_fill</i>";
                    var runAction = "<a href=\"#\" onclick=\"runService(\"" + services[i].name + "\", true)\">Aktivieren</a>";
                }
                if (services[i].wanted) {
                    var setting = "Aktiviert";
                } else {
                    var setting = "Deaktiviert";
                }
                if (services[i].name == "core") {
                    var actions = "Keine Aktionen für Core.";
                } else {
                    var actions = runAction + "<br /><a href=\"#\" onclick=\"runService(\"" + services[i].name + "\", false)\">Deaktivieren</a>";
                }
                document.getElementById("tablecontent").innerHTML += "<td>" + status + "</td><td>" + services[i].name + "</td><td>" + services[i].version + "</td><td>" + setting + "</td><td></td><td>" + runAction + "</td>";
            }
            preloader.toggle();
        }
        function runService(name, mode) {
            request = getAjaxRequest();
            var url = "../api/api.php";
            var params = "request=" + encodeURIComponent(JSON.stringify({
                servermanager: {
                    url: "http://192.168.255.255:49100/control",
                    data: {
                        container: name
                    }
                },
            }));
            request.onreadystatechange=stateChangedServices;
            request.open("POST",url,true);
            request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            request.send(params);
            function stateChangedServices() {
                if (request.readyState == 4) {
                    var response = JSON.parse(request.responseText);
                    if (response.servermanager == "SUCCESS") {
                        swal({
                            title: "Aktion erfolgreich ausgeführt.",
                            type: "success"
                        });
                    } else {
                        swal({
                            title: "Es ist ein Fehler aufgetreten.",
                            text: "Bitte erneut versuchen.",
                            type: "error"
                        });
                    }
                    getServices();
                }
            }
        }
    </script>
</body>
</html>
