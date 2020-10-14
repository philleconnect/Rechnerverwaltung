/*
 Timeout
 © 2020 Johannes Kreutz
 */

// Import modules
import api from './api.js';

// Module definition
let timeout = {
  timeinterval: null,
  endtime: null,
  clock: null,
  getTimeRemaining: function(endtime) {
    var t = Date.parse(endtime) - Date.parse(new Date());
    var seconds = ('0' + (Math.floor((t / 1000) % 60))).substr(-2);
    var minutes = Math.floor((t / 1000 / 60) % 60);
    var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
    var days = Math.floor(t / (1000 * 60 * 60 * 24));
    return {
      'total': t,
      'days': days,
      'hours': hours,
      'minutes': minutes,
      'seconds': seconds
    };
  },
  updateClock: function() {
    var t = this.getTimeRemaining(this.endtime);
    this.clock.innerHTML = 'Auto-Logout in '+t.minutes+':'+t.seconds;
    if (t.total <= 0) {
      clearInterval(this.timeinterval);
      api.send("/api/logout", "POST", {}).then(function(response) {
        window.location.reload();
      }.bind(this))
    }
  },
  initializeClock: function(id) {
    this.clock = document.getElementById(id);
    this.updateClock();
    this.timeinterval = setInterval(this.updateClock.bind(this), 1000);
  },
  resetClock: function() {
    clearInterval(this.timeinterval);
    this.endtime = new Date((Date.parse(new Date) + 1200000));
    this.initializeClock('timeout');
  },
  pauseClock: function() {
    clearInterval(this.timeinterval);
    document.getElementById('timeout').innerHTML = 'Auto-Logout ausgesetzt';
  }
}

export default timeout;
