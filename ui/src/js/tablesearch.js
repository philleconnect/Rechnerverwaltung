/*
 Table search module for PhilleConnect Admin Backend
 © 2019 Johannes Kreutz.
 */
import TableFilter from 'tablefilter';

class tableSearch {
    constructor(id, properties) {
        this.element = document.getElementById(id);
        this.properties = properties;
        this.enable();
    }
    enable() {
        this.tf = new TableFilter(this.element, this.properties);
        this.tf.init();
    }
    disable() {
        this.tf.destroy();
    }
    reload() {
        this.disable();
        this.enable();
    }
}

export default tableSearch;
