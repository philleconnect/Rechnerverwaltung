<?php
    $config = unserialize(file_get_contents('../config/config.txt'));
    if ($config['database']['finish'] == 'true') {
        header('Location: ldap.php');
    }
    if ($_POST['isReady'] == 'true') {
        $mysqli = mysqli_connect($_POST['url'], $_POST['user'], $_POST['password'], $_POST['name']);
        $trycount = 0;
        $sleeptime = 1;
        while ($trycount < 10) {
            if (mysqli_connect_errno()) {
                set_time_limit(60);
                sleep($sleeptime);
                $trycount++;
                $sleeptime++;
                $mysqli = mysqli_connect($_POST['url'], $_POST['user'], $_POST['password'], $_POST['name']);
            } else {
                include "../api/accessConfig.php";
                changeConfigValue('database', 'url', $_POST['url']);
                changeConfigValue('database', 'user', $_POST['user']);
                changeConfigValue('database', 'password', $_POST['password']);
                changeConfigValue('database', 'name', $_POST['name']);
                $configTableRequest = "CREATE TABLE IF NOT EXISTS configs (id int(11) NOT NULL, name text COLLATE utf8_bin NOT NULL, os text COLLATE utf8_bin NOT NULL, smbserver text COLLATE utf8_bin NOT NULL, driveone text COLLATE utf8_bin NOT NULL, drivetwo text COLLATE utf8_bin NOT NULL, drivethree text COLLATE utf8_bin NOT NULL, pathone text COLLATE utf8_bin NOT NULL, pathtwo text COLLATE utf8_bin NOT NULL, paththree text COLLATE utf8_bin NOT NULL, shutdown int(11) NOT NULL, dologin text COLLATE utf8_bin NOT NULL, loginpending text COLLATE utf8_bin NOT NULL, loginfailed text COLLATE utf8_bin NOT NULL, wrongcredentials text COLLATE utf8_bin NOT NULL, networkfailed text COLLATE utf8_bin NOT NULL, success text COLLATE utf8_bin NOT NULL, groupfolders text COLLATE utf8_bin NOT NULL, infotext text COLLATE utf8_bin NOT NULL, servicemode int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;";
                $machinesTableRequest = "CREATE TABLE IF NOT EXISTS machines (id int(11) NOT NULL, room text COLLATE utf8_bin NOT NULL, machine text COLLATE utf8_bin NOT NULL, hardwareid text COLLATE utf8_bin NOT NULL, config_win text COLLATE utf8_bin NOT NULL, config_linux text COLLATE utf8_bin NOT NULL, inet int(11) NOT NULL, ip text COLLATE utf8_bin NOT NULL, ipfire int(11) NOT NULL, teacher int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;";
                $userdataTableRequest = "CREATE TABLE IF NOT EXISTS userdata (id int(11) NOT NULL, username text COLLATE utf8_bin NOT NULL, password text COLLATE utf8_bin NOT NULL, type int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;";
                $logTableRequest = "CREATE TABLE IF NOT EXISTS log (id int(11) NOT NULL, action int(11) NOT NULL, user text COLLATE utf8_bin NOT NULL, machine text COLLATE utf8_bin NOT NULL, timestamp int(11) NOT NULL, target text COLLATE utf8_bin NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;";
                $groupfoldersTableRequest = "CREATE TABLE IF NOT EXISTS groupfolders (id int(11) NOT NULL, name text COLLATE utf8_bin NOT NULL, students int(11) NOT NULL, teachers int(11) NOT NULL, roomexchange int(11) NOT NULL, writeable int(11) NOT NULL, path text COLLATE utf8_bin NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;";
                $configTableQuery = mysqli_query($mysqli, $configTableRequest);
                $machinesTableQuery = mysqli_query($mysqli, $machinesTableRequest);
                $userdataTableQuery = mysqli_query($mysqli, $userdataTableRequest);
                $logTableQuery = mysqli_query($mysqli, $logTableRequest);
                $groupfoldersTableQuery = mysqli_query($mysqli, $groupfoldersTableRequest);
                $alterRequest1 = "ALTER TABLE configs ADD PRIMARY KEY (id);";
                $alterRequest2 = "ALTER TABLE machines ADD PRIMARY KEY (id);";
                $alterRequest3 = "ALTER TABLE userdata ADD PRIMARY KEY (id);";
                $alterRequest4 = "ALTER TABLE log ADD PRIMARY KEY (id);";
                $alterRequest5 = "ALTER TABLE groupfolders ADD PRIMARY KEY (id);";
                $alterRequest6 = "ALTER TABLE configs MODIFY id int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=1;";
                $alterRequest7 = "ALTER TABLE machines MODIFY id int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=1;";
                $alterRequest8 = "ALTER TABLE userdata MODIFY id int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=1;";
                $alterRequest9 = "ALTER TABLE log MODIFY id int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=1;";
                $alterRequest10 = "ALTER TABLE groupfolders MODIFY id int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=1;";
                $alterQuery1 = mysqli_query($mysqli, $alterRequest1);
                $alterQuery2 = mysqli_query($mysqli, $alterRequest2);
                $alterQuery3 = mysqli_query($mysqli, $alterRequest3);
                $alterQuery4 = mysqli_query($mysqli, $alterRequest4);
                $alterQuery5 = mysqli_query($mysqli, $alterRequest5);
                $alterQuery6 = mysqli_query($mysqli, $alterRequest6);
                $alterQuery7 = mysqli_query($mysqli, $alterRequest7);
                $alterQuery8 = mysqli_query($mysqli, $alterRequest8);
                $alterQuery9 = mysqli_query($mysqli, $alterRequest9);
                $alterQuery10 = mysqli_query($mysqli, $alterRequest10);
                $fillConfigRequest = "INSERT INTO configs (name, os, smbserver, driveone, drivetwo, drivethree, pathone, pathtwo, paththree, shutdown, dologin, loginpending, loginfailed, wrongcredentials, networkfailed, success, groupfolders, infotext, servicemode) VALUES ('beispiel_windows', 'win', '".mysqli_real_escape_string($mysqli, file_get_contents('../../host.txt'))."', 'X:', 'Y:', 'Z:', 'Laufwerk X', 'Laufwerk Y', 'Laufwerk Z', 540, 'Bitte melde dich mit deinen Zugangsdaten an.', 'Anmeldung läuft, bitte warten...', 'Anmeldung fehlgeschlagen. Bitte frage deinen Lehrer.', 'Nutzername oder Passwort falsch.', 'Nutzername falsch oder Netzwerkfehler.', 'Anmeldung erfolgreich!', '[[\"J:\",1],[\"K:\",3]]', 'Glückwunsch!%Sie haben PhilleConnect erfolgreich eingerichtet.%Diesen Hinweis und weitere Einstellungen können Sie in der Administrationsoberfläche ändern.', 0), ('beispiel_linux', 'linux', '".mysqli_real_escape_string($mysqli, file_get_contents('../../host.txt'))."', '/media/', '/media/', '/media/', '/media/', '/media/', '/media/', 540, 'Bitte melde dich mit deinen Zugangsdaten an.', 'Anmeldung läuft, bitte warten...', 'Anmeldung fehlgeschlagen. Bitte frage deinen Lehrer.', 'Nutzername oder Passwort falsch.', 'Nutzername falsch oder Netzwerkfehler.', 'Anmeldung erfolgreich!', '[[\"/media/\",1],[\"/media/\",3]]', 'Glückwunsch!%Sie haben PhilleConnect erfolgreich eingerichtet.%Diesen Hinweis und weitere Einstellungen können Sie in der Administrationsoberfläche ändern.', 0);";
                $fillConfigQuery = mysqli_query($mysqli, $fillConfigRequest);
                $fillGroupfoldersRequest = "INSERT INTO groupfolders (name, students, teachers, roomexchange, writeable, path) VALUES ('SchulTausch', 1, 1, 0, 1, '/home/schoolExchange'), ('SchulVorlagen', 0, 1, 0, 1, '/home/schoolTemplate'), ('SchulVorlagenSchueler', 1, 1, 0, 0, '/home/schoolTemplate'), ('LehrerTausch', 0, 1, 0, 1, '/home/teacherExchange'), ('LehrerVorlagen', 0, 1, 0, 0, '/home/teacherTemplate');";
                $fillGroupfoldersQuery = mysqli_query($mysqli, $fillGroupfoldersRequest);
                if ($configTableQuery && $machinesTableQuery && $userdataTableQuery && $logTableQuery && $groupfoldersTableQuery && $fillConfigQuery && $fillGroupfoldersQuery && $alterQuery1 && $alterQuery2 && $alterQuery3 && $alterQuery4 && $alterQuery5 && $alterQuery6 && $alterQuery7 && $alterQuery8 && $alterQuery9 && $alterQuery10) {
                    $data = array(
                        (object) array(
                            'name' => 'SchulTausch',
                            'path' => '/home/schoolExchange',
                            'students' => true,
                            'teachers' => true,
                            'writeable' => true,
                        ),
                        (object) array(
                            'name' => 'SchulVorlagen',
                            'path' => '/home/schoolTemplate',
                            'students' => false,
                            'teachers' => true,
                            'writeable' => true,
                        ),
                        (object) array(
                            'name' => 'SchulVorlagenSchueler',
                            'path' => '/home/schoolTemplate',
                            'students' => true,
                            'teachers' => true,
                            'writeable' => false,
                        ),
                        (object) array(
                            'name' => 'LehrerTausch',
                            'path' => '/home/teacherExchange',
                            'students' => false,
                            'teachers' => true,
                            'writeable' => true,
                        ),
                        (object) array(
                            'name' => 'LehrerVorlagen',
                            'path' => '/home/teacherTemplate',
                            'students' => false,
                            'teachers' => true,
                            'writeable' => false,
                        ),
                    );
                    $options = array(
                        'http' => array(
                            'header' => "Content-type: application/x-www-form-urlencoded\r\n",
                            'method' => 'POST',
                            'content' => json_encode($data)
                        )
                    );
                    $context = stream_context_create($options);
                    $result = file_get_contents('http://samba:8000', false, $context);
                    if ($result === false) {
                        $case = 3;
                    } elseif (strpos($result, 'Thanks, it worked') !== false) {
                        changeConfigValue('database', 'finish', 'true');
                        header("Location: ldap.php");
                    } else {
                        $case = 3;
                    }
                } else {
                    $case = 2;
                }
                break;
            }
        }
        if (mysqli_connect_errno()) {
            $case = 1;
        }
    }
?>
<!DOCTYPE html>
<html>
<head>
    <title>Setup - Datenbank - PhilleConnect Admin</title>
    <?php include "includes.php"; ?>
</head>
<body>
    <div role="navigation" id="foo" class="nav-collapse">
        <div class="top">
            <img src="../ui/ressources/img/logo.png">
            <li><b>PHILLE</b>CONNECT</li>
        </div>
        <ul>
            <li>
                <a href="#">Willkommen</a>
            </li>
            <li class="active">
                <a href="#">Datenbank</a>
            </li>
            <li>
                <a href="#">LDAP-Server</a>
            </li>
            <li>
                <a href="#">IPFire</a>
            </li>
            <li>
                <a href="#">Administratorkonto</a>
            </li>
            <li>
                <a href="#">Fertigstellen</a>
            </li>
        </ul>
    </div>
    <div role="main" class="main">
        <a href="#nav" class="nav-toggle">Menu</a>
        <noscript>
            <p>Dein Browser unterstützt kein JavaScript oder JavaScript ist ausgeschaltet. Du musst JavaScript aktivieren, um diese Seite zu verwenden!</p>
        </noscript>
        <p style="font-family: Arial, sans-serif; font-size: 45px;"><b>SQL</b>DATENBANK</p>
        <?php
            if ($_POST['isReady'] == 'true' && !$mysqli && $case == 1) {
                ?>
                <p style="color: red;">Fehler beim Verbinden mit dem MySQl-Server:</p>
                <br />
                <p style="color: red;"><?php echo mysqli_connect_error(); ?></p>
                <br />
                <p style="color: red;">Bitte korrigiere deine Eingaben und probiere es erneut.</p>
                <?php
            } elseif ($_POST['isReady'] == 'true' && $case == 2) {
                ?>
                <p style="color: red;">Fehler beim Erstellen der Tabellen.</p>
                <?php
            } elseif ($_POST['isReady'] == 'true' && $case == 3) {
                ?>
                <p style="color: red;">Fehler beim Einrichten des Samba-Servers.</p>
                <br />
                <p style="color: red;"><?php echo $result; ?></p>
                <?php
            }
        ?>
        <form action="database.php" method="post">
            <div class="datagrid">
                <table>
                    <thead>
                        <tr>
                            <th>Datenbank-Zugangsdaten:</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>URL:</td>
                            <td><input type="text" value="localhost" name="url"/></td>
                        </tr>
                        <tr class="alt">
                            <td>Datenbank-Benutzer:</td>
                            <td><input type="text" value="sql_user" name="user"/></td>
                        </tr>
                        <tr>
                            <td>Passwort:</td>
                            <td><input type="text" value="sql_password" name="password"/></td>
                        </tr>
                        <tr class="alt">
                            <td>Datenbank-Name:</td>
                            <td><input type="text" value="sql_database" name="name"/></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <input type="submit" value=">> Weiter"/>
            <input type="hidden" value="true" name="isReady"/>
        </form>
        <button onclick="window.location.href = 'ldap.php'">Überspringen</button>
    </div>
    <script>
        var navigation = responsiveNav("foo", {customToggle: ".nav-toggle"});
    </script>
</body>
</html>
