    // For button under track analysis
    $("#button_track").click(function() {
        var value_track = $("#text_track").val();
        // Showing error message if no input entered
        if (value_track.length == 0) {
            $("#replacethis").replaceWith('<div class="row" id="replacethis"><div data-alert class="alert-box" class="large-12 columns">Please enter a track name<\/div>');
	    $("#replacethis2").remove();
            $("#replacethis3").remove();
        } else {
            var requesturl = "http://ec2-54-211-198-60.compute-1.amazonaws.com/1K?traname=" + value_track;
            //Starting Ajax request
            $.ajax({
                url: requesturl,
                type: 'GET',
                success: function(data) {
                    var status = data["status"]
                    // Handling condition where there are no results
                    if (status == "NORESULTS") {
                        $("#replacethis").replaceWith('<div class="row" id="replacethis"><div data-alert class="alert-box" class="large-12 columns">Sorry, we do not have information on this track<\/div>')
                    } else {
                        var genderDict = data["gender"];
                        var males = genderDict["m"];
                        var females = genderDict["f"];
                        var ageDict = data["age"];
                        var ageArray = [];
                        for (var each in ageDict) {
                            ageArray.push({
                                label: each,
                                y: ageDict[each]
                            });
                        }
                        var hourDict = data["hour"];
                        var hourArray = [];
                        for (var each in hourDict) {
                            hourArray.push({
                                label: each,
                                y: hourDict[each]
                            });
                        }
                        var weekdayDict = data["weekday"];
                        var weekdayArray = [];
                        for (var each in weekdayDict) {
                            weekdayArray.push({
                                label: each,
                                y: weekdayDict[each]
                            });
                        }
                        var countryDict = data["country"]
                        var countryArray = []
                        for (var each in countryDict) {
                            countryArray.push(countryDict[each]);
                        }
                        $("#replacethis").replaceWith('<div class="row" id="replacethis"><div id="trackgenderchart" class="large-6 columns" style="height:250px"><\/div><\/div>');
                        var chart = new CanvasJS.Chart("trackgenderchart", {
                            theme: "theme2",
                            title: {
                                text: "Gender",
                                fontFamily: "Calibri"
                            },
                            data: [{
                                type: "doughnut",
                                dataPoints: [{
                                    label: "Males",
                                    y: males
                                }, {
                                    label: "Females",
                                    y: females
                                }, ]
                            }]
                        });
                        chart.render();
                        $("#replacethis").append('<div id="trackagechart" class="large-6 columns" style="height:250px"><\/div>');
                        var chart = new CanvasJS.Chart("trackagechart", {
                            theme: "theme2",
                            title: {
                                text: "Age",
                                fontFamily: "Calibri"
                            },
                            data: [{
                                type: "spline",
                                dataPoints: ageArray
                            }]
                        });
                        chart.render();
                        $("#replacethis").after('<div class="row" id="replacethis2"><hr> <div id="trackhourchart" class="large-6 columns" style="height:250px"><\/div><\/div>');
                        var chart = new CanvasJS.Chart("trackhourchart", {
                            theme: "theme2",
                            title: {
                                text: "Hour",
                                fontFamily: "Calibri"
                            },
                            data: [{
                                type: "spline",
                                dataPoints: hourArray
                            }]
                        });
                        chart.render();
                        $("#replacethis2").append('<div id="trackweekdaychart" class="large-6 columns" style="height:250px"><\/div>');
                        var chart = new CanvasJS.Chart("trackweekdaychart", {
                            theme: "theme2",
                            title: {
                                text: "Weekday",
                                fontFamily: "Calibri"
                            },
                            data: [{
                                type: "spline",
                                dataPoints: weekdayArray
                            }]
                        });
                        chart.render();
                        $("#replacethis2").after('<div class="row" id="replacethis3"><hr> <div id="trackcountrymap" class="large-12 columns" style="height:500px;padding-bottom:100px;"><p style="text-align:center;font-size:120%;font-family:Calibri">Country Heat Map<\/p><\/div><\/div>');
                        // HERE Maps Code:
                        nokia.Settings.set("app_id", "VMBvOMpdSfn6wMbt1Anz");
                        nokia.Settings.set("app_code", "1kTcwkTf0RJKCzbXSv1YZQ");
                        // Get the DOM node to which we will append the map
                        var mapContainer = document.getElementById("trackcountrymap");
                        // Create a map inside the map container DOM node
                        var map = new nokia.maps.map.Display(mapContainer, {
                            components: [
                            // Add the behavior component to allow panning / zooming of the map
                            new nokia.maps.map.component.Behavior()],
                            zoomLevel: 2,
                            center: [32.51, 13.4]
                        });
                        var mapData = countryArray;
                        var heatmapProvider;
                        try {
                            // Creating Heatmap overlay
                            heatmapProvider = new nokia.maps.heatmap.Overlay({
                                // This is the greatest zoom level for which the overlay will provide tiles
                                max: 20,
                                // This is the overall opacity applied to this overlay
                                opacity: 0.6,
                                // Defines if our heatmap is value or density based
                                type: "value",
                                // Coarseness defines the resolution with which the heat map is created.
                                coarseness: 2
                            });
                        } catch (e) {
                            // The heat map overlay constructor throws an exception if there
                            // is no canvas support in the browser
                            alert(typeof e == "string" ? e : e.message);
                        }
                        // Only start loading data if the heat map overlay was successfully created
                        if (heatmapProvider) {
                            // Trigger the load of data, after the map emmits the "displayready" event
                            map.addListener("displayready", function() {
                                heatmapProvider.addData(mapData);
                                map.overlays.add(heatmapProvider);
                                // Rendering the heat map overlay onto the map
                                heatmapProvider.addData(mapData);
                                map.overlays.add(heatmapProvider);
                            });
                        } //End of HERE maps code
                    } //End of else construct from within the success part of ajax
                } // End of success part of Ajax call
            }) // End of Ajax Call 
        } //end of else construct from the no input entered condition
    }); // End of click function


    // For button under artist analysis
    $("#button_artist").click(function() {
        var value_artist = $("#text_artist").val();
        // Showing error message if no input entered
        if (value_artist.length == 0) {
            $("#replacethis").replaceWith('<div class="row" id="replacethis"><div data-alert class="alert-box" class="large-12 columns">Please enter an artist name<\/div>');
	    $("#replacethis2").remove();
        } else {
            var requesturl = "http://ec2-54-211-198-60.compute-1.amazonaws.com/360K?artname=" + value_artist;
            //Starting Ajax request
	    $.ajax({
                url: requesturl,
                type: 'GET',
                success: function(data) {
                    var status = data["status"]
                    // Handling condition where there are no results
                    if (status == "NORESULTS") {
                        $("#replacethis").replaceWith('<div class="row" id="replacethis"><div data-alert class="alert-box" class="large-12 columns">Sorry, we do not have information on this artist<\/div>')
                    } else {
                        var genderDict = data["gender"];
                        var males = genderDict["m"];
                        var females = genderDict["f"];
                        var ageDict = data["age"];
                        var ageArray = [];
                        for (var each in ageDict) {
                            ageArray.push({
                                label: each,
                                y: ageDict[each]
                            });
                        }
                        var countryDict = data["country"]
                        var countryArray = []
                        for (var each in countryDict) {
                            countryArray.push(countryDict[each]);
                        }
                        $("#replacethis").replaceWith('<div class="row" id="replacethis"><div id="artistgenderchart" class="large-6 columns" style="height:250px"><\/div><\/div>');
                        var chart = new CanvasJS.Chart("artistgenderchart", {
                            theme: "theme2",
                            title: {
                                text: "Gender",
                                fontFamily: "Calibri"
                            },
                            data: [{
                                type: "doughnut",
                                dataPoints: [{
                                    label: "Males",
                                    y: males
                                }, {
                                    label: "Females",
                                    y: females
                                }, ]
                            }]
                        });
                        chart.render();
                        $("#replacethis").append('<div id="artistagechart" class="large-6 columns" style="height:250px"><\/div>');
                        var chart = new CanvasJS.Chart("artistagechart", {
                            theme: "theme2",
                            title: {
                                text: "Age",
                                fontFamily: "Calibri"
                            },
                            data: [{
                                type: "spline",
                                dataPoints: ageArray
                            }]
                        });
                        chart.render();
                        $("#replacethis").after('<div class="row" id="replacethis2"><hr> <div id="artistcountrymap" class="large-12 columns" style="height:500px;padding-bottom:100px;"><p style="text-align:center;font-size:120%;font-family:Calibri">Country Heat Map<\/p><\/div><\/div>');
                        // HERE Maps Code:
                        nokia.Settings.set("app_id", "VMBvOMpdSfn6wMbt1Anz");
                        nokia.Settings.set("app_code", "1kTcwkTf0RJKCzbXSv1YZQ");
                        // Get the DOM node to which we will append the map
                        var mapContainer = document.getElementById("artistcountrymap");
                        // Create a map inside the map container DOM node
                        var map = new nokia.maps.map.Display(mapContainer, {
                            components: [
                            // Add the behavior component to allow panning / zooming of the map
                            new nokia.maps.map.component.Behavior()],
                            zoomLevel: 2,
                            center: [32.51, 13.4]
                        });
                        var mapData = countryArray;
                        var heatmapProvider;
                        try {
                            // Creating Heatmap overlay
                            heatmapProvider = new nokia.maps.heatmap.Overlay({
                                // This is the greatest zoom level for which the overlay will provide tiles
                                max: 20,
                                // This is the overall opacity applied to this overlay
                                opacity: 0.6,
                                // Defines if our heatmap is value or density based
                                type: "value",
                                // Coarseness defines the resolution with which the heat map is created.
                                coarseness: 2
                            });
                        } catch (e) {
                            // The heat map overlay constructor throws an exception if there
                            // is no canvas support in the browser
                            alert(typeof e == "string" ? e : e.message);
                        }
                        // Only start loading data if the heat map overlay was successfully created
                        if (heatmapProvider) {
                            // Trigger the load of data, after the map emmits the "displayready" event
                            map.addListener("displayready", function() {
                                heatmapProvider.addData(mapData);
                                map.overlays.add(heatmapProvider);
                                // Rendering the heat map overlay onto the map
                                heatmapProvider.addData(mapData);
                                map.overlays.add(heatmapProvider);
                            });
                        } //End of HERE maps code
                    } //End of else construct from within the success part of ajax
                } // End of success part of Ajax call
            }) // End of Ajax Call 
        } //end of else construct from the no input entered condition
    }); // End of click function

    // For button under user similarity
    $("#button_usersimilarity").click(function() {
        var value_usersimilarity1 = $("#text_usersimilarity1").val();
        var value_usersimilarity2 = $("#text_usersimilarity2").val();
        // Showing error message if no input entered
        if (value_usersimilarity1.length == 0 || value_usersimilarity2.length == 0) {
            $("#replacethis").replaceWith('<div class="row" id="replacethis"><div data-alert class="alert-box" class="large-12 columns">Please enter values in both username fields<\/div>');
        } else {
	if (value_usersimilarity1 == value_usersimilarity2) {
$("#replacethis").replaceWith('<div class="row" id="replacethis"><div data-alert class="alert-box" class="large-12 columns">Please enter two different usernames<\/div>');
} else{
            var requesturl = "http://ec2-54-211-198-60.compute-1.amazonaws.com/usersimilarity?user1=" + value_usersimilarity1 + "&user2=" + value_usersimilarity2;
            //Starting Ajax request
	    $.ajax({
                url: requesturl,
                type: 'GET',
                success: function(data) {
                    var status = data["status"]
                    // Handling condition where wrong username(s) are entered
                    if (status == "WRONG USER1" || status == "WRONG USER2") {
                        $("#replacethis").replaceWith('<div class="row" id="replacethis"><div data-alert class="alert-box" class="large-12 columns">Please enter a valid username in both fields<\/div>')
                    } else {
			var similarity = data["similarity"];
			var common = data["common"]
                        var gender1 = data["gender1"]
			var gender2 = data["gender2"]
                        var age1 = data["age1"]
			var age2 = data["age2"]
			var country1 = data["country1"]
			var country2 = data["country2"]
                        var registered1 = data["registered1"]
			var registered2 = data["registered2"]
                        $("#replacethis").replaceWith('<div class="row" id="replacethis"><ul class="vcard small-2 large-4 columns"><li class="fn">User 1</li><li class="state">Gender: ' + gender1 +'</li><li class="state">Age: ' + age1 + '</li><li class="state">Country: ' + country1 + '</li><li>Registered: ' + registered1 + '</li></ul><ul class="vcard small-2 large-4 columns" style="text-align:center"><li class="fn">Music Compatibility: ' + similarity + '</li><li class="state">Common Artists: ' + common + '</li></ul><ul class="vcard small-2 large-4 columns" style="text-align:right"><li class="fn">User 2</li><li class="state">Gender: ' + gender2 +'</li><li class="state">Age: ' + age2 + '</li><li class="state">Country: ' + country2 + '</li><li>Registered: ' + registered2 + '</li></ul><\/div>');
                 
			} //End of else construct from within the success part of ajax
                } // End of success part of Ajax call
            }) // End of Ajax Call 
	} //End of else from the same usernames in both fields
        } //end of else construct from the no input entered condition
    }); // End of click function

// Fetching and displaying network analysis data
$("#switch_nwanalysis").click(function() {
	var requesturl = 'http://ec2-54-211-198-60.compute-1.amazonaws.com/networkanalysis';
	$.ajax({
                url: requesturl,
                type: 'GET',
                success: function(data) {
		var topartists_1k = data["topartists_1k"];
		var topartists_1k_text = '';
		for (var each in topartists_1k) {
                            topartists_1k_text = topartists_1k_text + '<tr><td>' + topartists_1k[each] + '</td></tr>'
                        }
		var topartists_1k2005 = data["topartists_1k2005"];
		var topartists_1k2005_text = '';
		for (var each in topartists_1k2005) {
                            topartists_1k2005_text = topartists_1k2005_text + '<tr><td>' + topartists_1k2005[each] + '</td></tr>'
                        }
		var topartists_1k2006 = data["topartists_1k2006"];
		var topartists_1k2006_text = '';
		for (var each in topartists_1k2006) {
                            topartists_1k2006_text = topartists_1k2006_text + '<tr><td>' + topartists_1k2006[each] + '</td></tr>'
                        }
		var topartists_1k2007 = data["topartists_1k2007"];
		var topartists_1k2007_text = '';
		for (var each in topartists_1k2007) {
                            topartists_1k2007_text = topartists_1k2007_text + '<tr><td>' + topartists_1k2007[each] + '</td></tr>'
                        }
		var topartists_1k2008 = data["topartists_1k2008"];
		var topartists_1k2008_text = '';
		for (var each in topartists_1k2008) {
                            topartists_1k2008_text = topartists_1k2008_text + '<tr><td>' + topartists_1k2008[each] + '</td></tr>'
                        }
		var topartists_1k2009 = data["topartists_1k2009"];
		var topartists_1k2009_text = '';
		for (var each in topartists_1k2009) {
                            topartists_1k2009_text = topartists_1k2009_text + '<tr><td>' + topartists_1k2009[each] + '</td></tr>'
                        }

		$("#replacethis").replaceWith('<div class="row" id="replacethis"><div class="large-12 columns"><div class="panel">Charts from 1K data set</div></div></div><div class="row" id="replacethis2"><div class="large-3 columns" style="text-align:center"><table><thead><tr><th style="text-align:center" width="200">Top Artists(Overall)</th></tr></thead><tbody>' + topartists_1k_text + '</tbody></table></div><div class="large-3 columns" style="text-align:center"><table><thead><tr><th width="200" style="text-align:center">Top Artists in 2005</th></tr></thead><tbody>' + topartists_1k2005_text + '</tbody></table></div>'+ '<div class="large-3 columns" style="text-align:center"><table><thead><tr><th width="200" style="text-align:center">Top Artists in 2006</th></tr></thead><tbody>' + topartists_1k2006_text + '</tbody></table></div>' + '<div class="large-3 columns" style="text-align:center"><table><thead><tr><th width="200" style="text-align:center">Top Artists in 2007</th></tr></thead><tbody>' + topartists_1k2007_text + '</tbody></table></div></div>' + '<div class="row" id="replacethis3"><div class="large-6 columns" style="text-align:center"><table><thead><tr><th width="400" style="text-align:center">Top Artists in 2008</th></tr></thead><tbody>' + topartists_1k2008_text + '</tbody></table></div><div class="large-6 columns" style="text-align:center"><table><thead><tr><th width="400" style="text-align:center">Top Artists in 2009</th></tr></thead><tbody>' + topartists_1k2009_text + '</tbody></table></div></div>');

		var month_1k = data["month_1k"];
		var month_1karray = []		
		for (var each in month_1k) {
                            month_1karray.push({
                                label: parseInt(each),
                                y: parseInt(month_1k[each])
                            });
                        }
		$("#replacethis3").after('<div class="row" id="replacethis4"><hr><div class="large-12 columns" id="month_1kchart" style="height:250px"></div></div>')
		var chart = new CanvasJS.Chart("month_1kchart", {
                            theme: "theme2",
                            title: {
                                text: "Month",
                                fontFamily: "Calibri"
                            },
                            data: [{
                                type: "spline",
                                dataPoints: month_1karray
                            }]
                        });
                        chart.render();

		var day_1k = data["day_1k"];
		var day_1karray = []		
		for (var each in day_1k) {
                            day_1karray.push({
                                label: parseInt(each),
                                y: parseInt(day_1k[each])
                            });
                        }
		$("#replacethis4").after('<div class="row" id="replacethis5"><hr><div class="large-6 columns" id="day_1kchart" style="height:250px"></div></div>')
		var chart = new CanvasJS.Chart("day_1kchart", {
                            theme: "theme2",
                            title: {
                                text: "Day of Month",
                                fontFamily: "Calibri"
                            },
                            data: [{
                                type: "spline",
                                dataPoints: day_1karray
                            }]
                        });
                        chart.render();

		var hour_1k = data["hour_1k"];
		var hour_1karray = []				
		for (var each in hour_1k) {
                            hour_1karray.push({
                                label: parseInt(each),
                                y: parseInt(hour_1k[each])
                            });
                        }
		$("#replacethis5").append('<div class="large-6 columns" id="hour_1kchart" style="height:250px"></div><hr></div>')
		var chart = new CanvasJS.Chart("hour_1kchart", {
                            theme: "theme2",
                            title: {
                                text: "Hour",
                                fontFamily: "Calibri"
                            },
                            data: [{
                                type: "spline",
                                dataPoints: hour_1karray
                            }]
                        });
                        chart.render();


		var topartistcount_360k = data["topartistcount_360k"];
		var topartistcount_360k_text = '';
		for (var each in topartistcount_360k) {
                            topartistcount_360k_text = topartistcount_360k_text + '<tr style="text-align:center"><td>' + topartistcount_360k[each] + '</td></tr>'
                        }

		var topartistplays_360k = data["topartistplays_360k"];
		var topartistplays_360k_text = '';
		for (var each in topartistplays_360k) {
                            topartistplays_360k_text = topartistplays_360k_text + '<tr><td>' + topartistplays_360k[each] + '</td></tr>'
                        }

		$("#replacethis5").after('<div class="row" id="replacethis6"><div class="panel">Charts from 360K data set</div></div><div class="row" id="replacethis7"><div class="large-6 columns"><table><thead><tr><th width="400" style="text-align:center">Top Artists by listener count</th></tr></thead><tbody>' + topartistcount_360k_text + '</tbody></table></div><div class="large-6 columns" style="text-align:center"><table><thead><tr><th width="400" style="text-align:center">Top Artists by number of plays</th></tr></thead><tbody>' + topartistplays_360k_text + '</tbody></table></div></div>')



	} //End of success function
	}); //End of ajax call
	}); //End of click function


    // Clearing the charts below on clicking the panels
    $("a[id$='panel']").click(function() {
        $("div[id*='replacethis']").replaceWith('<div id="replacethis"><\/div>');
    });
    // Clearing the charts when any button (which initiate the ajax request) is clicked. Also showing LOADING gif.
    $(document).ajaxStart(function() {
        $("div[id*='replacethis']").replaceWith('<div id="replacethis"><\/div>');
        $("#replacethis").append('<div class="row"><div class="large-12 columns"><img src="img/ajax-loader.gif"><\/div><\/div>')
    });
