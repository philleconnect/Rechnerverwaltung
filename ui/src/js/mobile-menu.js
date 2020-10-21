/*
 * Mobile menu open and close
 * © 2020 Johannes Kreutz. All rights reserved.
 */
let mobilemenu = {
  status: false,
  toggle: function() {
    if (!this.status) {
      this.status = true;
      document.documentElement.classList.add("js-nav-active");
      document.getElementById("menu").classList.add("opened");
      document.getElementById("menu").classList.remove("closed");
      document.getElementById("hamburger").classList.add("active");
    } else {
      this.close();
    }
  },
  close: function() {
    if (this.status) {
      this.status = false;
      document.documentElement.classList.remove("js-nav-active");
      document.getElementById("menu").classList.remove("opened");
      document.getElementById("menu").classList.add("closed");
      document.getElementById("hamburger").classList.remove("active");
    }
  }
}

export default mobilemenu;
