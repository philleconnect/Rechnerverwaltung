/*
 API-Request-Engine
 © 2019 - 2020 Johannes Kreutz
 */

// Import libraries
import Swal from 'sweetalert2';

// Import modules
import login from './login.js';
import errormsg from './errormessages.js';
import preloader from './preloader.js';

// Module definition
let api = {
  send: function(url, type, data, disableErrorMessages) {
    return new Promise(function(resolve, reject) {
      let request = new XMLHttpRequest;
      request.addEventListener("load", function(event) {
        if (disableErrorMessages) {
          resolve(event.target);
        } else {
          if (event.target.status == 401) {
            if (window.isLoggedIn) {
              login.show();
            } else {
              Swal.showValidationMessage('Anmeldedaten falsch.');
              Swal.hideLoading();
            }
          } else if (event.target.status == 403) {
            if (window.isLoggedIn) {
              Swal.fire({
                title: "Zugriffsfehler",
                text: "Der Account verfügt nicht über die nötigen Berechtigungen für diesen Bereich.",
                icon: "warning"
              })
            } else {
              Swal.showValidationMessage('Anmeldedaten falsch.');
              Swal.hideLoading();
            }
          } else if (event.target.status == 502) {
            this.fireBackendConnectionError();
          } else if (event.target.status == 404) {
            preloader.hide();
            this.fire404Error();
          } else if (event.target.status >= 400) {
            preloader.hide();
            errormsg.fire(event.target.responseText);
            reject(event.target.responseText);
          } else if (event.target.status == 200 || event.target.status == 201) {
            resolve(event.target.responseText);
          }
        }
      }.bind(this))
      request.addEventListener("error", function(event) {
        if (!disableErrorMessages) {
          this.fireBackendConnectionError();
          reject(event);
        } else {
          resolve(event.target);
        }
      }.bind(this))
      let formData = new FormData();
      for (let key in data) {
        formData.append(key, data[key])
      }
      request.open(type, url, true);
      request.send(formData);
    }.bind(this))
  },
  fireBackendConnectionError: function() {
    Swal.fire({
      title: "Es konnte keine Verbindung zum Backend-Server hergestellt werden.",
      icon: "error",
      showConfirmButton: false,
      allowEscapeKey: false,
      allowOutsideClick: false
    });
  },
  fire404Error: function() {
    Swal.fire({
      title: "Der angeforderte API-Endpunkt konnte nicht gefunden werden.",
      icon: "error",
    });
  }
}

export default api;
