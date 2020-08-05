/*
 Spoiler JS for PhilleConnect Backend
 */
class spoiler {
    constructor(button, container) {
        this.button = button;
        this.container = container;
        this.status = false;
        this.button.onclick = this.toggle.bind(this);
    }
    toggle() {
        if (this.status) {
            this.status = false;
            this.container.classList.add('spoiler-invisible');
            this.button.classList.remove('spoiler-checkbox-out');
        } else {
            this.status = true;
            this.container.classList.remove('spoiler-invisible');
            this.button.classList.add('spoiler-checkbox-out');
        }
    }
}

export default spoiler;
