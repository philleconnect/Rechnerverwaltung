/*
 ServerManager JavaScript Engine for PhilleConnect Admin Backend
 © 2019 Johannes Kreutz
 */
var servermanager = {
    services: null,
    plugins: null,
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
            var envStoreRequest = getAjaxRequest();
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
                                title: "Die Aktion wird jetzt durchgeführt.",
                                text: "Dies kann einige Minuten dauern. Bitte diese Seite nicht neu laden!",
                                allowOutsideClick: false,
                                allowEscapeKey: false,
                                onOpen: () => {
                                    swal.showLoading();
                                    servermanager.service.pendingChecker(name);
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
            var managerRequest = getAjaxRequest();
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
            swal({
                title: "ServerManager auf Version " + version + " aktualisieren?",
                text: "Durch die Aktualisierung ist der ServerManager für einige Zeit nicht verfügbar. Wir empfehlen dies zu zu Zeiten durchzuführen, zu denen keiner mit dem System arbeitet. Während der Aktualisierung bitte diese Seite nicht neu laden.",
                type: "question",
                showCancelButton: true,
                cancelButtonText: 'Abbrechen',
                confirmButtonText: 'Aktualisieren',
                showLoaderOnConfirm: true,
                allowOutsideClick: false,
                allowEscapeKey: false,
                preConfirm: function() {
                    return new Promise(function(resolve) {
                        var managerUpdateRequest = getAjaxRequest();
                        var url = "../api/api.php";
                        var params = "request=" + encodeURIComponent(JSON.stringify({
                            servermanager: {
                                url: "http://192.168.255.255:49100/executemanagerupdate",
                                data: {
                                    apikey: apikey,
                                    version: version
                                }
                            },
                        }));
                        managerUpdateRequest.onreadystatechange = stateChangedManagerUpdateCheck;
                        managerUpdateRequest.open("POST",url,true);
                        managerUpdateRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                        managerUpdateRequest.send(params);
                        function stateChangedManagerUpdateCheck() {
                            if (managerUpdateRequest.readyState == 4) {
                                var response = JSON.parse(JSON.parse(managerUpdateRequest.responseText).servermanager);
                                if (response.error) {
                                    swal({
                                        title: "Es ist ein interner Fehler aufgetreten.",
                                        text: "Bitte erneut versuchen. Der Fehlercode lautet '" + response.error + "'.",
                                        type: "error"
                                    })
                                } else if (response.result == "running") {
                                    servermanager.manager.pendingChecker(version);
                                } else {
                                    swal({
                                        title: "Es ist ein Fehler aufgetreten.",
                                        text: "Bitte erneut versuchen.",
                                        type: "error"
                                    })
                                }
                            }
                        }
                    })
                }
            })
        },
        pendingChecker: function(version) {
            var managerPendingCheckRequest = getAjaxRequest();
            var url = "../api/api.php";
            var params = "request=" + encodeURIComponent(JSON.stringify({
                servermanager: {
                    url: "http://192.168.255.255:49100/managerupdatecheck",
                    data: {
                        apikey: apikey,
                    }
                },
            }));
            managerPendingCheckRequest.onreadystatechange = stateChangedManagerPendingCheck;
            managerPendingCheckRequest.open("POST",url,true);
            managerPendingCheckRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            managerPendingCheckRequest.send(params);
            function stateChangedManagerPendingCheck() {
                if (managerPendingCheckRequest.readyState == 4) {
                    var responseContainer = JSON.parse(managerPendingCheckRequest.responseText);
                    if (!responseContainer.servermanager) {
                        setTimeout(function() {servermanager.manager.pendingChecker(version);}, 2000);
                    } else {
                        var response = JSON.parse(responseContainer.servermanager);
                        if (response.result == version) {
                            swal({
                                title: "ServerManager wurde erfolgreich aktualisiert.",
                                type: "success"
                            }).then(() => {
                                servermanager.manager.check();
                            })
                        } else if (response.error) {
                            swal({
                                title: "Es ist ein Fehler aufgetreten.",
                                text: "Bitte erneut versuchen. Der Fehlercode lautet '" + response.error + "'",
                                type: "error"
                            })
                        } else if (response.result) {
                            setTimeout(function() {servermanager.manager.pendingChecker(version);}, 2000);
                        } else {
                            swal({
                                title: "Es ist ein Fehler aufgetreten.",
                                text: "Bitte erneut versuchen.",
                                type: "error"
                            })
                        }
                    }
                }
            }
        }
    },
    service: {
        pending: null,
        get: function() {
            preloader.toggle("LADEN");
            var request = getAjaxRequest();
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
                document.getElementById("status_" + name).innerHTML = "<i class=\"f7-icons\" style=\"color: blue;\">arrow_up_round_fill</i>";
            } else {
                var action = "stop";
                document.getElementById("status_" + name).innerHTML = "<i class=\"f7-icons\" style=\"color: blue;\">arrow_down_round_fill</i>";
            }
            var runRequest = getAjaxRequest();
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
                    if (response.result == "running") {
                        document.getElementById("status_" + name).innerHTML = "<i class=\"f7-icons\" style=\"color: green;\">play_round_fill</i>";
                    } else if (response.result == "paused") {
                        document.getElementById("status_" + name).innerHTML = "<i class=\"f7-icons\" style=\"color: red;\">close_round_fill</i>";
                    } else if (response.error) {
                        swal({
                            title: "Die Aktion konnte nicht ausgeführt werden.",
                            text: "Bitte erneut versuchen. Der Fehlercode lautet '" + response.error + "'.",
                            type: "error"
                        })
                        if (mode) {
                            document.getElementById("status_" + name).innerHTML = "<i class=\"f7-icons\" style=\"color: red;\">close_round_fill</i>";
                        } else {
                            document.getElementById("status_" + name).innerHTML = "<i class=\"f7-icons\" style=\"color: green;\">play_round_fill</i>";
                        }
                    } else {
                        document.getElementById("status_" + name).innerHTML = "<i class=\"f7-icons\" style=\"color: red;\">alert_fill</i>";
                    }
                    servermanager.service.get();
                }
            }
        },
        check: function(name) {
            var updateRequest = getAjaxRequest();
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
                text: "Durch die Aktualisierung ist dieser Service für einige Zeit nicht verfügbar. Wir empfehlen dies zu zu Zeiten durchzuführen, zu denen keiner mit dem System arbeitet. Während der Aktualisierung bitte diese Seite nicht neu laden.",
                type: "question",
                showCancelButton: true,
                cancelButtonText: 'Abbrechen',
                confirmButtonText: 'Aktualisieren',
                showLoaderOnConfirm: true,
                allowOutsideClick: false,
                allowEscapeKey: false,
                preConfirm: function() {
                    return new Promise(function(resolve) {
                        var doUpdateRequest = getAjaxRequest();
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
                        doUpdateRequest.onreadystatechange = stateChangedDoUpdateCheck;
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
                                    servermanager.service.pending = "update";
                                    servermanager.service.pendingChecker(name);
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
                        var doRevertRequest = getAjaxRequest();
                        var url = "../api/api.php";
                        var params = "request=" + encodeURIComponent(JSON.stringify({
                            servermanager: {
                                url: "http://192.168.255.255:49100/executerevert",
                                data: {
                                    apikey: apikey,
                                    service: name
                                }
                            },
                        }));
                        doRevertRequest.onreadystatechange = stateChangedDoRevertCheck;
                        doRevertRequest.open("POST",url,true);
                        doRevertRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                        doRevertRequest.send(params);
                        function stateChangedDoRevertCheck() {
                            if (doRevertRequest.readyState == 4) {
                                var response = JSON.parse(JSON.parse(doRevertRequest.responseText).servermanager);
                                if (response.error) {
                                    swal({
                                        title: "Es ist ein interner Fehler aufgetreten.",
                                        text: "Bitte erneut versuchen. Der Fehlercode lautet '" + response.error + "'.",
                                        type: "error"
                                    })
                                } else if (response.result == "running") {
                                    servermanager.service.pending = "revert";
                                    servermanager.service.pendingChecker(name);
                                } else {
                                    swal({
                                        title: "Es ist ein unbekannter Fehler aufgetreten.",
                                        text: "Bitte erneut versuchen.",
                                        type: "error"
                                    })
                                }
                            }
                        }
                    })
                }
            })
        },
        pendingChecker: function(name) {
            var pendingCheckRequest = getAjaxRequest();
            var url = "../api/api.php";
            var params = "request=" + encodeURIComponent(JSON.stringify({
                servermanager: {
                    url: "http://192.168.255.255:49100/actionstatus",
                    data: {
                        apikey: apikey,
                        service: name
                    }
                },
            }));
            pendingCheckRequest.onreadystatechange = stateChangedPendingCheck;
            pendingCheckRequest.open("POST",url,true);
            pendingCheckRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            pendingCheckRequest.send(params);
            function stateChangedPendingCheck() {
                if (pendingCheckRequest.readyState == 4) {
                    if (pendingCheckRequest.status == 200) {
                        if (pendingCheckRequest.responseText.includes("Datenbankfehler")) {
                            setTimeout(function() {servermanager.service.pendingChecker(name);}, 2000);
                        } else {
                            var response = JSON.parse(JSON.parse(pendingCheckRequest.responseText).servermanager);
                            if (servermanager.service.pending == "update") {
                                if (response.error) {
                                    swal({
                                        title: "Es ist ein Fehler aufgetreten.",
                                        text: "Bitte versuchen Sie erneut, das Update durchzuführen.",
                                        type: "error"
                                    })
                                } else {
                                    if (response.result == "updating") {
                                        setTimeout(function() {servermanager.service.pendingChecker(name);}, 2000);
                                    } else if (response.result == "running") {
                                        swal({
                                            title: "Das Update wurde erfolgreich durchgeführt.",
                                            text: "Der Service '" + name + "' ist jetzt in der aktuellen Version installiert.",
                                            type: "success"
                                        }).then(() => {
                                            servermanager.service.get();
                                        })
                                    } else {
                                        swal({
                                            title: "Beim Updatevorgang ist ein Fehler aufgetreten.",
                                            text: "Die vorherige Version des Service wurde wiederhergestellt.",
                                            type: "error"
                                        })
                                    }
                                }
                            } else if (servermanager.service.pending == "revert") {
                                if (response.result == "reverting") {
                                    setTimeout(function() {servermanager.service.pendingChecker(name);}, 2000);
                                } else if (response.result == "running") {
                                    swal({
                                        title: "Die vorherige Version wurde erfolgreich wiederhergestellt.",
                                        type: "success"
                                    }).then(() => {
                                        servermanager.service.get();
                                    })
                                } else {
                                    swal({
                                        title: "Es ist ein Fehler aufgetreten.",
                                        text: "Die vorherige Version von '" + name  + "' konnte nicht wiederhergestellt werden.",
                                        type: "error"
                                    })
                                }
                            } else if (servermanager.service.pending == "install") {
                                if (response.result == "installing") {
                                    setTimeout(function() {servermanager.service.pendingChecker(name);}, 2000);
                                } else if (response.result == "running") {
                                    swal({
                                        title: "Service '" + name + "' wurde erfolgreich installiert.",
                                        type: "success"
                                    }).then(() => {
                                        servermanager.service.loadAvailable();
                                    })
                                } else {
                                    swal({
                                        title: "Es ist ein Fehler aufgetreten.",
                                        text: "'" + name  + "' konnte nicht installiert werden.",
                                        type: "error"
                                    })
                                }
                            } else if (servermanager.service.pending == "delete") {
                                if (response.result == "deleting") {
                                    setTimeout(function() {servermanager.service.pendingChecker(name);}, 2000);
                                } else if (response.result == "deleted") {
                                    swal({
                                        title: "Service '" + name + "' wurde deinstalliert.",
                                        type: "success"
                                    }).then(() => {
                                        servermanager.service.get();
                                    })
                                } else if (response.error) {
                                    swal({
                                        title: "Es ist ein Fehler aufgetreten.",
                                        text: "'" + name  + "' konnte nicht deinstalliert werden. Der Fehlercode lautet '" + response.error + "'.",
                                        type: "error"
                                    })
                                } else {
                                    swal({
                                        title: "Es ist ein Fehler aufgetreten.",
                                        text: "'" + name  + "' konnte nicht deinstalliert werden.",
                                        type: "error"
                                    })
                                }
                            }
                        }
                    } else {
                        setTimeout(function() {servermanager.service.pendingChecker(name);}, 2000);
                    }
                }
            }
        },
        install: function(name) {
            swal({
                title: "Service '" + name + "' wirklich installieren?",
                text: "Dies wird einen Moment dauern",
                type: "question",
                showCancelButton: true,
                cancelButtonText: 'Abbrechen',
                confirmButtonText: 'Löschen',
                showLoaderOnConfirm: true,
                allowOutsideClick: false,
                allowEscapeKey: false,
                preConfirm: function() {
                    return new Promise(function(resolve) {
                        var doInstallRequest = getAjaxRequest();
                        var url = "../api/api.php";
                        var params = "request=" + encodeURIComponent(JSON.stringify({
                            servermanager: {
                                url: "http://192.168.255.255:49100/install",
                                data: {
                                    apikey: apikey,
                                    service: name
                                }
                            },
                        }));
                        doInstallRequest.onreadystatechange = stateChangedDoInstallCheck;
                        doInstallRequest.open("POST",url,true);
                        doInstallRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                        doInstallRequest.send(params);
                        function stateChangedDoInstallCheck() {
                            if (doInstallRequest.readyState == 4) {
                                var response = JSON.parse(JSON.parse(doInstallRequest.responseText).servermanager);
                                if (response.error) {
                                    swal({
                                        title: "Es ist ein interner Fehler aufgetreten.",
                                        text: "Bitte erneut versuchen. Der Fehlercode lautet '" + response.error + "'.",
                                        type: "error"
                                    })
                                } else if (response.result == "installing") {
                                    servermanager.service.pending = "install";
                                    servermanager.service.pendingChecker(name);
                                } else {
                                    servermanager.environment.getEnvironmentVariables(response.result, name);
                                }
                            }
                        }
                    })
                }
            })
        },
        delete: function(name) {
            swal({
                title: "Service '" + name + "' wirklich deinstallieren?",
                text: "WARNUNG! WARNUNG! WARNUNG! Alle Einstellungen von '" + name + "' werden ebenfalls gelöscht. Alle auf '" + name + "' aufbauende Funktionen werden nicht mehr zur Verfügung stehen.",
                type: "warning",
                showCancelButton: true,
                cancelButtonText: 'Abbrechen',
                confirmButtonText: 'Löschen',
                showLoaderOnConfirm: true,
                allowOutsideClick: false,
                allowEscapeKey: false,
                preConfirm: function() {
                    return new Promise(function(resolve) {
                        swal({
                            title: "Ich frage nochmal zur Sicherheit.",
                            text: "WARNUNG! WARNUNG! WARNUNG! Alle Einstellungen von '" + name + "' werden ebenfalls gelöscht. Alle auf '" + name + "' aufbauende Funktionen werden nicht mehr zur Verfügung stehen.",
                            type: "warning",
                            showCancelButton: true,
                            cancelButtonText: 'Abbrechen',
                            confirmButtonText: 'Löschen',
                            showLoaderOnConfirm: true,
                            allowOutsideClick: false,
                            allowEscapeKey: false,
                            preConfirm: function() {
                                return new Promise(function(resolve) {
                                    var doDeleteRequest = getAjaxRequest();
                                    var url = "../api/api.php";
                                    var params = "request=" + encodeURIComponent(JSON.stringify({
                                        servermanager: {
                                            url: "http://192.168.255.255:49100/delete",
                                            data: {
                                                apikey: apikey,
                                                service: name
                                            }
                                        },
                                    }));
                                    doDeleteRequest.onreadystatechange = stateChangedDoDeleteCheck;
                                    doDeleteRequest.open("POST",url,true);
                                    doDeleteRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                                    doDeleteRequest.send(params);
                                    function stateChangedDoDeleteCheck() {
                                        if (doDeleteRequest.readyState == 4) {
                                            var response = JSON.parse(JSON.parse(doDeleteRequest.responseText).servermanager);
                                            if (response.error) {
                                                swal({
                                                    title: "Es ist ein interner Fehler aufgetreten.",
                                                    text: "Bitte erneut versuchen. Der Fehlercode lautet '" + response.error + "'.",
                                                    type: "error"
                                                })
                                            } else if (response.result == "running") {
                                                servermanager.service.pending = "delete";
                                                servermanager.service.pendingChecker(name);
                                            } else {
                                                swal({
                                                    title: "Es ist ein unbekannter Fehler aufgetreten.",
                                                    text: "Bitte erneut versuchen.",
                                                    type: "error"
                                                })
                                            }
                                        }
                                    }
                                })
                            }
                        })
                    })
                }
            })
        },
        loadAvailable: function() {
            preloader.toggle("LADEN");
            var repoRequest = getAjaxRequest();
            var url = "../api/api.php";
            var params = "request=" + encodeURIComponent(JSON.stringify({
                servermanager: {
                    url: "http://192.168.255.255:49100/repo",
                    data: {
                        apikey: apikey
                    }
                },
            }));
            repoRequest.onreadystatechange = stateChangedRepo;
            repoRequest.open("POST",url,true);
            repoRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            repoRequest.send(params);
            function stateChangedRepo() {
                if (repoRequest.readyState == 4) {
                    var response = JSON.parse(repoRequest.responseText);
                    servermanager.plugins = JSON.parse(response.servermanager);
                    servermanager.writePluginTable();
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
            } else if (this.services[i].status == "paused" || this.services[i].status == "installed") {
                var status = "<i class=\"f7-icons\">close_round_fill</i>";
                var runAction = "<a href=\"#\" onclick=\"servermanager.service.run('" + this.services[i].name + "', true)\">Aktivieren</a>";
            } else if (this.services[i].status == "installing" || this.services[i].status == "updating") {
                var status = "<i class=\"f7-icons\" style=\"color: blue;\">reload_round_fill</i>";
                var runAction = "";
            } else {
                var status = "<i class=\"f7-icons\" style=\"color: red;\">close_round_fill</i>";
                var runAction = "";
            }
            if (runAction != "") {
                runAction += "; "
            }
            runAction += "<a href=\"#\" onclick=\"servermanager.service.delete('" + this.services[i].name + "', true)\">Deinstallieren</a>";
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
            document.getElementById("tablecontent").innerHTML += style + "<td id=\"status_" + this.services[i].name + "\">" + status + "</td><td>" + this.services[i].name + "</td><td>" + this.services[i].version + previous + "</td><td>" + setting + "</td><td id=\"update_" + this.services[i].name + "\">Prüfung läuft...</td><td>" + actions + "</td></tr>";
            this.service.check(this.services[i].name);
        }
        renewTableSort();
        this.manager.check();
        preloader.toggle();
    },
    writePluginTable: function() {
        document.getElementById("plugincontent").innerHTML = "";
        for (var i = 0; i < this.plugins.length; i++) {
            if ((i % 2) == 0) {
                var style = "<tr>";
            } else {
                var style = "<tr class=\"alt\">";
            }
            if (this.plugins[i].installed) {
                var action = "Bereits installiert.";
            } else {
                var action = "<a href=\"#\" onclick=\"servermanager.service.install('" + this.plugins[i].name + "')\">Installieren</a>";
            }
            if (this.plugins[i].subscription) {
                var license = "Benötigt SchoolConnect Abbonement.";
            } else {
                var license = "Kostenlos (Open Source)";
            }
            document.getElementById("plugincontent").innerHTML += style + "<td>" + this.plugins[i].name + "</td><td>" + this.plugins[i].description + "</td><td>" + license + "</td><td>" + action + "</td></tr>";
        }
        preloader.toggle();
    }
}
