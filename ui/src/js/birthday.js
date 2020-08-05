/*
 Birthday parser for PhilleConnect Admin Backend
 © 2019 Johannes Kreutz.
 */
var birthday = {
    parse: function(input, spacer1, spacer2, field1, field2, field3) {
        var day = "";
        var month = "";
        var year = "";
        let first = input.split(spacer1);
        if (spacer1 == spacer2) {
            if (field2 == "1") {
                day = first[1];
            } else if (field2 == "2") {
                month = first[1];
            } else if (field2 == "3") {
                year = first[1];
            }
            if (field3 == "1") {
                day = first[2];
            } else if (field3 == "2") {
                month = first[2];
            } else if (field3 == "3") {
                year = first[2];
            }
        } else {
            let second = first[1].split(spacer2);
            if (field2 == "1") {
                day = second[0];
            } else if (field2 == "2") {
                month = second[0];
            } else if (field2 == "3") {
                year = second[0];
            }
            if (field3 == "1") {
                day = second[1];
            } else if (field3 == "2") {
                month = second[1];
            } else if (field3 == "3") {
                year = second[1];
            }
        }
        if (field1 == "1") {
            day = first[0];
        } else if (field1 == "2") {
            month = first[0];
        } else if (field1 == "3") {
            year = first[0];
        }
        return this.zerofy(day) + "." + this.zerofy(month) + "." + year;
    },
    zerofy: function(input) {
        if (input.length <= 1) {
            return "0" + input;
        }
        return input;
    },
    convertToDBFormat: function(input) {
        if (input == null) return null;
        let parts = input.split(".");
        return parts[2] + "-" + parts[1] + "-" + parts[0];
    },
    convertToGermanFormat: function(input) {
        if (input == null) return null;
        let parts = input.split("-");
        return parts[2] + "." + parts[1] + "." + parts[0];
    }
}

export default birthday;
