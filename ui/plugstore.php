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
                <tbody id="plugincontent"></tbody>
            </table>
        </div>
    </div>
    <script>
        var apikey = "<?php echo trim(file_get_contents('../config/apikey.txt')); ?>";
        function getAjaxRequest() {
            var ajax = null;
            ajax = new XMLHttpRequest;
            return ajax;
        }
    </script>
    <script src="ressources/js/servermanager.js" type="text/javascript"></script>
    <script>
        var navigation = responsiveNav("foo", {customToggle: ".nav-toggle"});
        servermanager.service.loadAvailable();
    </script>
</body>
</html>
