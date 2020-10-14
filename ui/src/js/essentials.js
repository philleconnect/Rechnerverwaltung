/*
 Essential functions for SchoolConnect Admin Backend
 © 2019 Johannes Kreutz
 */
let essentials = {
    // Create a new ajax request
    getAjaxRequest: function() {
        var ajax = null;
        ajax = new XMLHttpRequest;
        return ajax;
    },
    minusIfNull: function(input) {
        return (input == null || input == "") ? "-" : input;
    },
    getDayName: function(number) {
        switch(number) {
            case 0:
                return "Sonntag";
            case 1:
                return "Montag";
            case 2:
                return "Dienstag";
            case 3:
                return "Mittwoch";
            case 4:
                return "Donnerstag";
            case 5:
                return "Freitag";
            case 6:
                return "Samstag";
        }
    },
    getMonthName: function(number) {
        switch(number) {
            case 0:
                return "Januar";
            case 1:
                return "Februar";
            case 2:
                return "März";
            case 3:
                return "April";
            case 4:
                return "Mai";
            case 5:
                return "Juni";
            case 6:
                return "Juli";
            case 7:
                return "August";
            case 8:
                return "September";
            case 9:
                return "Oktober";
            case 10:
                return "November";
            case 11:
                return "Dezember";
        }
    },
    isInteger: function(input) {
        var regex = /^-?[0-9]*[1-9][0-9]*$/;
        return regex.test(input);
    },
    niceifyTimestamp: function(input) {
        let date = new Date(input);
        return date.getDate() + "." + (date.getMonth() + 1) + "." + date.getFullYear() + " " + date.getHours() + ":" + this.addLeadingZeroIfNeeded(date.getMinutes()) + ":" + this.addLeadingZeroIfNeeded(date.getSeconds());
    },
    addLeadingZeroIfNeeded: function(input) {
        let value = "0" + input;
        return value.substr(-2);
    },
    getLogText: function(type, info, target = null) {
        switch(type) {
            case 0:
                switch(info) {
                    case "0":
                        return "Erfolgreich angemeldet.";
                    case "10":
                        return "Zugangsdaten fehlerhaft.";
                    case "11":
                        return "Berechtigungen fehlerhaft.";
                }
            case 1:
                switch(info) {
                    case "0":
                        return "Passwort erfolgreich geändert.";
                    case "1":
                        return "Passwort ändern fehlgeschlagen: Datenbankfehler.";
                    case "2":
                        return "Passwort ändern fehlgeschlagen: LDAP-Fehler.";
                    case "10":
                        return "Passwort ändern fehlgeschlagen: Altes Passwort falsch.";
                    case "11":
                        return "Passwort ändern fehlgeschlagen: Neue Passwörter stimmen nicht überein.";
                }
            case 2:
                let targetString = "";
                if (target != null) {
                  targetString = " (" + target + ")";
                }
                switch(info) {
                    case "0":
                        return "Passwort erfolgreich zurückgesetzt." + targetString;
                    case "1":
                        return "Passwort zurücksetzen fehlgeschlagen: Datenbankfehler." + targetString;
                    case "2":
                        return "Passwort zurücksetzen fehlgeschlagen: LDAP-Fehler." + targetString;
                    case "10":
                        return "Passwort zurücksetzen fehlgeschlagen: Authentifizierung abgelehnt." + targetString;
                    case "11":
                        return "Passwort zurücksetzen fehlgeschlagen: Neue Passwörter stimmen nicht überein." + targetString;
                    case "12":
                        return "Passwort zurücksetzen fehlgeschlagen: Berechtigung fehlt." + targetString;
                    case "13":
                        return "Passwort zurücksetzen fehlgeschlagen: Passwort des Ziels kann nicht zurückgesetzt werden." + targetString;
                    case "14":
                        return "Passwort zurücksetzen fehlgeschlagen: Kein Lehrer-PC." + targetString;
                }
        }
        return "";
    }
}

export default essentials;
