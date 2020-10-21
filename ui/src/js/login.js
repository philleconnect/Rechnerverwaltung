/*
 Login-Engine
 © 2020 Johannes Kreutz
 */

// Import libraries
import Swal from 'sweetalert2'

// Import modules
import api from './api.js';
import errormsg from './errormessages.js';
import menue from './menue.js';
import preloader from './preloader.js';

// Module definition
let login = {
  show: function() {
    document.getElementById("app").classList.add("login-shown");
    Swal.fire({
      title: 'Bitte Nutzerdaten eingeben.',
      html: '<input type="text" id="swal-input1" placeholder="Nutzername" class="swal2-input"/><input type="password" id="swal-input2" placeholder="Passwort" class="swal2-input"/>',
      showCancelButton: false,
      confirmButtonText: 'Anmelden',
      showLoaderOnConfirm: true,
      allowOutsideClick: false,
      allowEscapeKey: false,
      preConfirm: function() {
        return new Promise(function(resolve) {
          if (document.getElementById("swal-input1").value == "" || document.getElementById("swal-input2").value == "") {
            Swal.showValidationMessage('Bitte geben Sie Nutzername und Passwort ein.');
            Swal.hideLoading();
          } else {
            login.login();
          }
        })
      }
    });
  },
  login: function() {
    window.isLoggedIn = false;
    api.send("/api/login", "POST", {uname: document.getElementById("swal-input1").value, passwd: document.getElementById("swal-input2").value}).then(function(response) {
      window.isLoggedIn = true;
      document.getElementById("app").classList.remove("login-shown");
      window.currentUserPermissions = JSON.parse(response);
      Swal.close();
      preloader.hide();
      menue.rebuild();
      window.app.views.main.router.navigate("/welcome", {reloadAll: true});
    }, function(error) {
      errormsg.fire(error);
    });
  }
}

export default login;
