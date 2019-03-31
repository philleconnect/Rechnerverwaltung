/*
 ServerManager JavaScript Engine for PhilleConnect Admin Backend
 © 2019 Johannes Kreutz
 */
var servermanager = {
    services: null,
    environment: {
        getEnvironmentVariables: function(data, name) {
            var steps = [];
            var questions = [];
            for (var i = 1; i <= data.length; i++) {
                steps.push(i.toString());
                questions.push({title:"Einstellung setzen: " + data[(i-1)].name,text:data[(i-1)].description});
            }
            swal.mixin({
                input: "text",
                confirmButtonText: "Weiter &rarr;",
                showCancelButton: false,
                allowOutsideClick: false,
                allowEscapeKey: false,
                progressSteps: steps,
            }).queue(questions).then((result) => {
                if (result.value) {
                    var output = [];
                    for (var i = 0; i < data.length; i++) {
                        output.push({key:data[i].name,value:result.value[i]});
                    }
                    servermanager.environment.storeEnvironmentVariables(output, name);
                }
            })
        },
        storeEnvironmentVariables: function(data, name) {
            envStoreRequest = getAjaxRequest();
            var url = "../api/api.php";
            var params = "request=" + encodeURIComponent(JSON.stringify({
                servermanager: {
                    url: "http://192.168.255.255:49100/storeenv",
                    data: {
                        apikey: apikey,
                        key: data[0].key,
                        value: data[0].value
                    }
                },
            }));
            envStoreRequest.onreadystatechange = stateChangedEnvStore;
            envStoreRequest.open("POST",url,true);
            envStoreRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            envStoreRequest.send(params);
            function stateChangedEnvStore() {
                if (envStoreRequest.readyState == 4) {
                    var response = JSON.parse(JSON.parse(envStoreRequest.responseText).servermanager);
                    if (response.result == "SUCCESS") {
                        if (data.length <= 1) {
                            swal({
                                title: "Das Update wird jetzt durchgeführt.",
                                text: "Dies kann einige Minuten dauern. Bitte diese Seite nicht neu laden!",
                                allowOutsideClick: false,
                                allowEscapeKey: false,
                                onOpen: () => {
                                    swal.showLoading();
                                    servermanager.service.updatePending(name);
                                }
                            })
                        } else {
                            data.shift()
                            servermanager.environment.storeEnvironmentVariables(data, name);
                        }
                    } else {
                        swal({
                            title: "Es ist ein interner Fehler aufgetreten.",
                            text: "Bitte erneut versuchen.",
                            type: "error"
                        })
                    }
                }
            }
        }
    },
    manager: {
        check: function() {
            managerRequest = getAjaxRequest();
            var url = "../api/api.php";
            var params = "request=" + encodeURIComponent(JSON.stringify({
                servermanager: {
                    url: "http://192.168.255.255:49100/manager",
                    data: {
                        apikey: apikey
                    }
                },
            }));
            managerRequest.onreadystatechange = stateChangedManagerCheck;
            managerRequest.open("POST",url,true);
            managerRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            managerRequest.send(params);
            function stateChangedManagerCheck() {
                if (managerRequest.readyState == 4) {
                    var response = JSON.parse(JSON.parse(managerRequest.responseText).servermanager);
                    if (response.available) {
                        document.getElementById("servermanager_version").innerHTML = "ServerManager-Version: " + response.actual + ". <a href=\"#\" onclick=\"servermanager.manager.update('" + response.available + "')\">Auf Version " + response.available + " aktualisieren.</a>";
                    } else {
                        document.getElementById("servermanager_version").innerHTML = "ServerManager-Version: " + response.actual + ".";
                    }
                }
            }
        },
        update: function(version) {

        }
    },
    service: {
        get: function() {
            preloader.toggle("LADEN");
            request = getAjaxRequest();
            var url = "../api/api.php";
            var params = "request=" + encodeURIComponent(JSON.stringify({
                servermanager: {
                    url: "http://192.168.255.255:49100/status",
                    data: {
                        apikey: apikey
                    }
                },
            }));
            request.onreadystatechange = stateChangedServices;
            request.open("POST",url,true);
            request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            request.send(params);
            function stateChangedServices() {
                if (request.readyState == 4) {
                    var response = JSON.parse(request.responseText);
                    servermanager.services = JSON.parse(response.servermanager);
                    servermanager.writeTable();
                }
            }
        },
        run: function(name, mode) {
            if (mode) {
                var action = "start";
            } else {
                var action = "stop";
            }
            runRequest = getAjaxRequest();
            var url = "../api/api.php";
            var params = "request=" + encodeURIComponent(JSON.stringify({
                servermanager: {
                    url: "http://192.168.255.255:49100/control",
                    data: {
                        apikey: apikey,
                        service: name,
                        action: action
                    }
                },
            }));
            runRequest.onreadystatechange = stateChangedRun;
            runRequest.open("POST",url,true);
            runRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            runRequest.send(params);
            function stateChangedRun() {
                if (runRequest.readyState == 4) {
                    var response = JSON.parse(JSON.parse(runRequest.responseText).servermanager);
                    if (response.status == "SUCCESS") {
                        swal({
                            title: "Aktion erfolgreich ausgeführt.",
                            type: "success"
                        });
                    } else {
                        swal({
                            title: "Es ist ein Fehler aufgetreten.",
                            text: "Bitte erneut versuchen.",
                            type: "error"
                        });
                    }
                    servermanager.service.get();
                }
            }
        },
        check: function(name) {
            updateRequest = getAjaxRequest();
            var url = "../api/api.php";
            var params = "request=" + encodeURIComponent(JSON.stringify({
                servermanager: {
                    url: "http://192.168.255.255:49100/updatecheck",
                    data: {
                        apikey: apikey,
                        service: name
                    }
                },
            }));
            updateRequest.onreadystatechange = stateChangedUpdateCheck;
            updateRequest.open("POST",url,true);
            updateRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            updateRequest.send(params);
            function stateChangedUpdateCheck() {
                if (updateRequest.readyState == 4) {
                    var response = JSON.parse(JSON.parse(updateRequest.responseText).servermanager);
                    if (response.error) {
                        document.getElementById("update_" + name).innerHTML = "Fehler.";
                    } else if (response.actualVersion == response.latestPossible) {
                        document.getElementById("update_" + name).innerHTML = "Aktuell: " + response.actualVersion;
                    } else {
                        document.getElementById("update_" + name).innerHTML = "<a href=\"#\" onclick=\"servermanager.service.update('" + name + "', '" + response.latestPossible + "')\">Auf " + response.latestPossible + " aktualisieren.</a>";
                    }
                }
            }
        },
        update: function(name, version) {
            swal({
                title: "'" + name + "' auf Version " + version + " aktualisieren?",
                text: "Durch die Aktualisierung ist dieser Service für einige Zeit nicht verfügbar. Wir empfehlen dies nur zu Zeiten durchzuführen, zu denen keiner mit dem System arbeitet. Die Aktualisierung kann einige Zeit in Anspruch nehmen. Bitte diese Seite nicht neu laden.",
                type: "question",
                showCancelButton: true,
                cancelButtonText: 'Abbrechen',
                confirmButtonText: 'Aktualisieren',
                showLoaderOnConfirm: true,
                allowOutsideClick: false,
                allowEscapeKey: false,
                preConfirm: function() {
                    return new Promise(function(resolve) {
                        doUpdateRequest = getAjaxRequest();
                        var url = "../api/api.php";
                        var params = "request=" + encodeURIComponent(JSON.stringify({
                            servermanager: {
                                url: "http://192.168.255.255:49100/executeupdate",
                                data: {
                                    apikey: apikey,
                                    service: name,
                                    version: version
                                }
                            },
                        }));
                        doUpdateRequest.onreadystatechange=stateChangedDoUpdateCheck;
                        doUpdateRequest.open("POST",url,true);
                        doUpdateRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                        doUpdateRequest.send(params);
                        function stateChangedDoUpdateCheck() {
                            if (doUpdateRequest.readyState == 4) {
                                var response = JSON.parse(JSON.parse(doUpdateRequest.responseText).servermanager);
                                if (response.error) {
                                    swal({
                                        title: "Es ist ein interner Fehler aufgetreten.",
                                        text: "Bitte erneut versuchen. Der Fehlercode lautet '" + response.error + "'.",
                                        type: "error"
                                    })
                                } else if (response.result == "running") {
                                    servermanager.service.updatePending(name);
                                } else {
                                    servermanager.environment.getEnvironmentVariables(response.result, name);
                                }
                            }
                        }
                    })
                }
            })
        },
        revert: function(name) {
            swal({
                title: "WARNUNG! Service wirklich auf vorherige Version zurücksetzen?",
                text: "Durch das Zurücksetzen auf die vorherige Version kann es zu Inkompatibilitäten mit bereits erzeugten Daten kommen. Wir empfehlen, diese Funktion ausschließlich direkt nach fehlgeschlagenen Aktualisierungen zu nutzen!",
                type: "warning",
                showCancelButton: true,
                cancelButtonText: 'Abbrechen',
                confirmButtonText: 'Zurücksetzen',
                showLoaderOnConfirm: true,
                allowOutsideClick: false,
                allowEscapeKey: false,
                preConfirm: function() {
                    return new Promise(function(resolve) {

                    })
                }
            })
        },
        updatePending: function(name) {
            updatePendingRequest = getAjaxRequest();
            var url = "../api/api.php";
            var params = "request=" + encodeURIComponent(JSON.stringify({
                servermanager: {
                    url: "http://192.168.255.255:49100/updatestatus",
                    data: {
                        apikey: apikey,
                        service: name
                    }
                },
            }));
            updatePendingRequest.onreadystatechange=stateChangedUpdatePendingCheck;
            updatePendingRequest.open("POST",url,true);
            updatePendingRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            updatePendingRequest.send(params);
            function stateChangedUpdatePendingCheck() {
                if (updatePendingRequest.readyState == 4) {
                    var response = JSON.parse(JSON.parse(updatePendingRequest.responseText).servermanager);
                    if (response.error) {
                        swal({
                            title: "Es ist ein Fehler aufgetreten.",
                            text: "Bitte versuchen Sie erneut, das Update durchzuführen.",
                            type: "error"
                        })
                    } else {
                        if (response.result == "updating") {
                            setTimeout(function() {servermanager.service.updatePending(name);}, 2000);
                        } else if (response.result == "finished") {
                            swal({
                                title: "Das Update wurde erfolgreich durchgeführt.",
                                text: "Der Service " + name + " ist jetzt in der aktuellen Version installiert.",
                                type: "success"
                            }).then({
                                window.reload();
                            })
                        } else {
                            swal({
                                title: "Beim Updatevorgang ist ein Fehler aufgetreten.",
                                text: "Die vorherige Version des Service wurde wiederhergestellt.",
                                type: "error"
                            })
                        }
                    }
                }
            }
        }
    },
    writeTable: function() {
        document.getElementById("tablecontent").innerHTML = "";
        for (var i = 0; i < this.services.length; i++) {
            if ((i % 2) == 0) {
                var style = "<tr>";
            } else {
                var style = "<tr class=\"alt\">";
            }
            if (this.services[i].status == "running") {
                var status = "<i class=\"f7-icons\" style=\"color: green;\">play_round_fill</i>";
                var runAction = "<a href=\"#\" onclick=\"servermanager.service.run('" + this.services[i].name + "', false)\">Deaktivieren</a>";
            } else if (this.services[i].status == "paused") {
                var status = "<i class=\"f7-icons\">close_round_fill</i>";
                var runAction = "<a href=\"#\" onclick=\"servermanager.service.run('" + this.services[i].name + "', true)\">Aktivieren</a>";
            } else if (this.services[i].status == "installing" || this.services[i].status == "updating") {
                var status = "<i class=\"f7-icons\" style=\"color: blue;\">reload_round_fill</i>";
                var runAction = "";
            } else {
                var status = "<i class=\"f7-icons\" style=\"color: red;\">close_round_fill</i>";
                var runAction = "";
            }
            if (this.services[i].wanted) {
                var setting = "Aktiviert";
            } else {
                var setting = "Deaktiviert";
            }
            if (this.services[i].name == "core") {
                var actions = "Keine Aktionen für Core.";
            } else {
                var actions = runAction;
            }
            if (this.services[i].previous != "") {
                var previous = "<br /><a href=\"#\" onclick=\"servermanager.service.revert('" + this.services[i].name + "')\">Zurück zu " + this.services[i].previous + "</a>";
            } else {
                var previous = "";
            }
            document.getElementById("tablecontent").innerHTML += style + "<td>" + status + "</td><td>" + this.services[i].name + "</td><td>" + this.services[i].version + previous + "</td><td>" + setting + "</td><td id=\"update_" + this.services[i].name + "\">Prüfung läuft...</td><td>" + actions + "</td></tr>";
            this.service.check(this.services[i].name);
        }
        renewTableSort();
        this.manager.check();
        preloader.toggle();
    }
}
