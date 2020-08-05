/*
 * Preloader JS by Johannes Kreutz for PhilleConnect Backend
 * © 2019 Johannes Kreutz.
 */
let preloader = {
    isVisible: false,
    toggle: function(text) {
        if (this.isVisible) {
            this.isVisible = false;
            document.getElementById('loader-background').classList.add('loader-invisible');
            setTimeout(function() {
                if (!preloader.isVisible) {
                    document.getElementById('loader-background').style.display = 'none';
                }
            }, 550);
        } else if (text != "") {
            this.isVisible = true;
            document.getElementById('loader-background').style.display = 'flex';
            if (text != '') {
                document.getElementById('loader-text').innerHTML = text;
            } else {
                document.getElementById('loader-text').innerHTML = 'SPEICHERN';
            }
            setTimeout(function() {
                if (preloader.isVisible) {
                    document.getElementById('loader-background').classList.remove('loader-invisible');
                }
            }, 10);
        }
    },
    hide: function() {
        if (this.isVisible) {
            this.toggle();
        }
    }
}

export default preloader;
