/*
 * Progress JS by Johannes Kreutz for PhilleConnect Backend
 * © 2019 Johannes Kreutz.
 */
let progress = {
    steps: [],
    actualIndex: 1,
    setup: function() {
        this.steps = [];
        this.actualIndex = 1;
        if (!!document.getElementById("progress")) {
            setTimeout(function() {
                for (const step of document.getElementsByClassName("step")) {
                    this.steps.push(step);
                }
            }.bind(this), 100);
            return true;
        } else {
            return false;
        }
    },
    isActive: function(step) {
        return step.classList.contains("current");
    },
    next: function() {
        this.animations.disable(this.actualIndex);
        this.animations.nextStep();
        this.actualIndex++;
        setTimeout(function() {
            this.animations.enable(this.actualIndex);
        }.bind(this), 400);
    },
    prev: function() {
        this.animations.disable(this.actualIndex);
        this.animations.prevStep();
        this.actualIndex--;
        setTimeout(function() {
            this.animations.enable(this.actualIndex);
        }.bind(this), 400);
    },
    animations: {
        disable: function(nr) {
            document.getElementById("step-" + nr).classList.remove("current");
            setTimeout(function() {
                document.getElementById("step-" + nr).classList.add("disabled");
            }, 350);
        },
        enable: function(nr) {
            document.getElementById("step-" + nr).classList.remove("disabled");
            setTimeout(function() {
                document.getElementById("step-" + nr).classList.add("current");
            }, 10);
        },
        nextStep: function() {
            for (var i = 0; i < (progress.steps.length - 1); i++) {
                if (progress.steps[i].classList.contains("current")) {
                    progress.steps[i].classList.remove("current");
                    progress.steps[i].classList.add("done");
                    progress.steps[i + 1].classList.add("current");
                    break;
                }
            }
        },
        prevStep: function() {
            for (var i = 1; i < progress.steps.length; i++) {
                if (progress.steps[i].classList.contains("current")) {
                    progress.steps[i].classList.remove("current");
                    progress.steps[i - 1].classList.remove("done");
                    progress.steps[i - 1].classList.add("current");
                }
            }
        },
    }
}

export default progress;
