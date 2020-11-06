/*
 Error message alert generator
 © 2020 Johannes Kreutz
 */

// Import libraries
import Swal from 'sweetalert2'

// Module definition
let errormsg = {
  codes: {
    ERR_DATABASE_ERROR: {
      title: "Es ist ein Datenbankfehler aufgetreten.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_LDAP_ERROR: {
      title: "Es ist ein LDAP-Fehler aufgetreten.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_CREATE_HOMEFOLDER: {
      title: "Der Nutzerdatenordner konnte nicht angelegt werden.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_NOT_IMPLEMENTED: {
      title: "Diese Funktion ist noch nicht implementiert.",
      text: "",
      showWarningSign: true
    },
    ERR_DELETE_PREVIOUS_FOLDER: {
      title: "Der Nutzerdatenordner eines vorherigen Nutzers konnte nicht verschoben werden.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_MOVE_DATA_FOLDER: {
      title: "Der Nutzerdatenordner konnte nicht verschoben werden.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_FOLDER_PLACE_INVALID: {
      title: "Der angegebene Pfad ist nicht korrekt.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_FOLDER_EXISTS: {
      title: "Fehler: Es existiert bereits ein solcher Ordner.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_PASSWORDS_DIFFERENT: {
      title: "Die Passwörter stimmen nicht überein.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_ACTUAL_ACCOUNT: {
      title: "Löschen fehlgeschlagen",
      text: "Der aktuell angemeldete Account kann nicht gelöscht werden.",
      showWarningSign: true
    },
    ERR_USER_NOT_FOUND: {
      title: "Account konnte nicht gefunden werden.",
      text: "",
      showWarningSign: true
    },
    ERR_AUTH_PASSWORD: {
      title: "Authentifizierung fehlgeschlagen",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_UPDATE_SAMBA: {
      title: "Die neuen Einstellungen konnten nicht auf den Samba-Server übertragen werden.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_PROFILE_IN_USE: {
      title: "Profil in Verwendung.",
      text: "Dieses Konfigurationsprofil ist derzeit in Verwendung und kann daher nicht gelöscht werden.",
      showWarningSign: true
    },
    ERR_CONNECTION_ERROR: {
      title: "Verbindungsfehler.",
      text: "Es konnte keine Vebindung zum ServerManager aufgebaut werden.",
      showWarningSign: true
    },
    ERR_ROOT_PASSWORD_WRONG: {
      title: "Das Root-Passwort ist falsch.",
      text: "Die Root-Anmeldung auf der IPFire ist fehlgeschlagen. Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_PORT_NOT_A_NUMBER: {
      title: "Der eingegebene Port ist keine ganze Zahl.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_IPFIRE_SETUP_USERADD: {
      title: "Es konnte kein Nutzer auf der IPFire angelegt werden.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_IPFIRE_SETUP_SETPASS: {
      title: "Für den neuen IPFire-Benutzer konnte kein Passwort festgelegt werden.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_IPFIRE_SETUP_PERMISSIONS: {
      title: "Die IPFire-Berechtigungen konnten nicht korrekt gesetzt werden.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_IPFIRE_SETUP_HOMEFOLDER: {
      title: "Für den neuen IPFire-Benutzer konnte kein Homefolder angelegt werden.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_IPFIRE_SETUP_SSHFILES: {
      title: "Für den neuen IPFire-Benutzer konnte kein SSH-Ordner angelegt werden.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_IPFIRE_SETUP_RULES: {
      title: "Die Firewallregeln konnten nicht auf die IPFire kopiert werden.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_SETUP_ERROR: {
      title: "Der IPFire-Benutzer konnte nicht korrekt angelegt werden.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_IPFIRE_SETUP_SSHKEY: {
      title: "Der SSH-Schlüssel konnte nicht auf die IPFire kopiert werden.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_IPFIRE_SETUP_RELOAD: {
      title: "Die geädetern IPFire-Einstellungen konnten nicht übernommen werden.",
      text: "Bitte erneut versuchen.",
      showWarningSign: true
    },
    ERR_ACTUAL_ACCOUNT: {
      title: "Der aktuell angemeldete Account kann nicht gelöscht werden.",
      text: "",
      showWarningSign: false
    },
    ERR_INPUT_ERROR: {
      title: "Fehelrhafte Eingaben.",
      text: "",
      showWarningSign: false
    }
  },
  fire: function(message) {
    if (message in this.codes) {
      let icon = this.codes[message].showWarningSign ? "warning" : "error";
      Swal.fire({
        title: this.codes[message].title,
        text: this.codes[message].text,
        icon: icon
      });
    } else {
      Swal.fire({
        title: "Es ist ein Fehler aufgetreten",
        text: message,
        icon: "error"
      });
    }
  }
}

export default errormsg;
