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
        <p id="servermanager_version">Servermanager-Version: Laden...</p>
        <p>Installierte Services:</p>
        <div class="datagrid">
            <table id="services">
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
        function renewTableSort() { //TODO: Fix creation of two selection controls
            /*setFilterGrid("services", {
                col_0: "none",
                col_3: "select",
                col_4: "none",
                col_5: "none",
                display_all_text: "Alle anzeigen",
                sort_select: true
            });*/
        }
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
                    url: "http://192.168.255.255:49100/status"
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
            for (var i = 0; i < services.length; i++) {
                if ((i % 2) == 0) {
                    var style = "<tr>";
                } else {
                    var style = "<tr class=\"alt\">";
                }
                if (services[i].status == "running") {
                    var status = "<i class=\"f7-icons\" style=\"color: green;\">play_round_fill</i>";
                    var runAction = "<a href=\"#\" onclick=\"runService(\"" + services[i].name + "\", false)\">Deaktivieren</a>";
                } else if (services[i].status == "paused") {
                    var status = "<i class=\"f7-icons\">close_round_fill</i>";
                    var runAction = "<a href=\"#\" onclick=\"runService(\"" + services[i].name + "\", true)\">Aktivieren</a>";
                } else if (services[i].status == "installing" || services[i].status == "updating") {
                    var status = "<i class=\"f7-icons\" style=\"color: blue;\">reload_round_fill</i>";
                    var runAction = "";
                } else {
                    var status = "<i class=\"f7-icons\" style=\"color: red;\">close_round_fill</i>";
                    var runAction = "";
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
                document.getElementById("tablecontent").innerHTML += style + "<td>" + status + "</td><td>" + services[i].name + "</td><td>" + services[i].version + "</td><td>" + setting + "</td><td id=\"update_" + services[i].name + "\">Prüfung läuft...</td><td>" + actions + "</td></tr>";
                checkIfUpdateAvailable(services[i].name);
            }
            renewTableSort();
            checkManagerVersion();
            preloader.toggle();
        }
        function runService(name, mode) {
            if (mode) {
                var action = "start";
            } else {
                var action = "stop";
            }
            request = getAjaxRequest();
            var url = "../api/api.php";
            var params = "request=" + encodeURIComponent(JSON.stringify({
                servermanager: {
                    url: "http://192.168.255.255:49100/control",
                    data: {
                        container: name,
                        action: action
                    }
                },
            }));
            request.onreadystatechange=stateChangedRun;
            request.open("POST",url,true);
            request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            request.send(params);
            function stateChangedRun() {
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
        function checkIfUpdateAvailable(name) {
            request = getAjaxRequest();
            var url = "../api/api.php";
            var params = "request=" + encodeURIComponent(JSON.stringify({
                servermanager: {
                    url: "http://192.168.255.255:49100/updatecheck",
                    data: {
                        container: name
                    }
                },
            }));
            request.onreadystatechange=stateChangedUpdateCheck;
            request.open("POST",url,true);
            request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            request.send(params);
            function stateChangedUpdateCheck() {
                if (request.readyState == 4) {
                    var response = JSON.parse(JSON.parse(request.responseText).servermanager);
                    if (response.error) {
                        document.getElementById("update_" + name).innerHTML = "Fehler.";
                    } else if (response.actualVersion == response.latestPossible) {
                        document.getElementById("update_" + name).innerHTML = "Aktuell: " + response.actualVersion;
                    } else {
                        document.getElementById("update_" + name).innerHTML = "<a href=\"#\" onclick=\"updateService(\"" + name + "\", \"" + response.latestPossible + "\")\">Auf " + response.latestPossible + " aktualisieren.</a>";
                    }
                }
            }
        }
        function updateService(name, version) {

        }
        function checkManagerVersion() {
            request = getAjaxRequest();
            var url = "../api/api.php";
            var params = "request=" + encodeURIComponent(JSON.stringify({
                servermanager: {
                    url: "http://192.168.255.255:49100/manager",
                },
            }));
            request.onreadystatechange=stateChangedManagerCheck;
            request.open("POST",url,true);
            request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            request.send(params);
            function stateChangedManagerCheck() {
                if (request.readyState == 4) {
                    var response = JSON.parse(JSON.parse(request.responseText).servermanager);
                    if (response.available) {
                        document.getElementById("servermanager_version").innerHTML = "Servermanager-Version: " + response.actual + ". <a href=\"#\" onclick=\"updateManager(\"" + response.available + "\")\">Auf Version " + response.available + " aktualisieren.</a>";
                    } else {
                        document.getElementById("servermanager_version").innerHTML = "Servermanager-Version: " + response.actual + ".";
                    }
                }
            }
        }
        function updateManager() {

        }
        renewTableSort();
        getServices();
    </script>
</body>
</html>
