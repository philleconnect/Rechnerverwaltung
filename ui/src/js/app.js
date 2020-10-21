import $$ from 'dom7';
import Framework7 from 'framework7/framework7.esm.bundle.js';

// Import Icons and App Custom Styles
import '../css/app.css';
import '../css/diverse.css';
import '../css/icons.css';
import '../css/input.css';
import '../css/preloader.css';
import '../css/progress.css';
import '../css/responsivenav.css';
import '../css/spoiler.css';
import '../css/table.css';
import '../css/hamburgers.min.css';

// Import libraries
import Swal from 'sweetalert2';

// Import Routes
import routes from './routes.js';

// Import JS Modules
import api from './api.js';
import login from './login.js';
import menue from './menue.js';
import timeout from './timeout.js';
import mobilemenu from './mobile-menu.js';

import './mobile-menu-scrolling.js';

// Import main app component
import App from '../app.f7.html';

window.app = new Framework7({
  root: '#app', // App root element
  component: App, // App main component
  id: "org.schoolconnect.adminui",

  name: 'SchoolConnect Administration', // App name

  // App routes
  routes: routes,

  // Events
  on: {
    pageInit: function(page) {
      timeout.resetClock();
      menue.markActive(page.name);
    }
  }
});

let mainView = window.app.views.create(".view-main", {
  animate: false,
  preloadPreviousPage: false,
  pushState: true,
  pushStateAnimate: false,
  pushStateSeparator: "#page",
  removeElements: false
})

// Make the back button work
window.onpopstate = function(event) {
  if (event.state) {
    window.app.views.main.router.back();
  }
}

// Global login state
window.isLoggedIn = false;
window.currentUserPermissions = [];

// Start app
api.send("/api/setup/status", "GET", {}).then(function(response) {
  if (response == "SETUP_IPFIRE") {
    window.app.views.main.router.navigate("/setup/ipfire", {reloadAll: true});
  } else if (response == "SETUP_ADMIN") {
    window.app.views.main.router.navigate("/setup/admin", {reloadAll: true});
  } else {
    login.show();
  }
})

window.mobilemenu = mobilemenu;
