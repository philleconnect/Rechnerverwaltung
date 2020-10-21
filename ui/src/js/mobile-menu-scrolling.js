/*
 * Add a background to the mobile menu toggle if the page is scrolled (blurry if supported)
 * © 2018 - 2020 Johannes Kreutz. All rights reserved.
 */
window.onload = function() {
  window.onscroll = function() {
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;
    if (scrollTop <= 0) {
      Array.prototype.forEach.call(document.getElementsByClassName('mobile-menu-toggle'), function(element) {
        element.classList.remove('scrolled');
      });
    } else {
      Array.prototype.forEach.call(document.getElementsByClassName('mobile-menu-toggle'), function(element) {
        element.classList.add('scrolled');
      });
    }
  }
}
