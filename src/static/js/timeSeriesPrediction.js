$(document).ready(function(){
 showLoader();
 fetchNumberKilled("LOS ANGELES",5);
 fetchNumberInjured("LOS ANGELES",5);
 fetchPedestrianInjured('LOS ANGELES',5);
 fetchBicyclistInjured('LOS ANGELES',5);

document.getElementById("1year").addEventListener("click",function(){
	showLoader();
	var county = document.getElementById("county").value;
	$(".nav-link").removeClass("active");
	$("#1year").addClass("active");
	fetchNumberKilled(county,1);
	fetchNumberInjured(county,1);
	fetchPedestrianInjured(county,1);
	fetchBicyclistInjured(county,1);
});
document.getElementById("2year").addEventListener("click",function(){
	showLoader();
	var county = document.getElementById("county").value;
	$(".nav-link").removeClass("active");
	$("#2year").addClass("active");
	fetchNumberKilled(county,2);
	fetchNumberInjured(county,2);
	fetchPedestrianInjured(county,2);
	fetchBicyclistInjured(county,2);
});
document.getElementById("5year").addEventListener("click",function(){
	showLoader();
	var county = document.getElementById("county").value;
	$(".nav-link").removeClass("active");
	$("#5year").addClass("active");
	fetchNumberKilled(county,5);
	fetchNumberInjured(county,5);
	fetchPedestrianInjured(county,5);
	fetchBicyclistInjured(county,5);
});

document.getElementById("county").addEventListener('change',function(){
	showLoader();
	var county = document.getElementById("county").value;
	$(".nav-link").removeClass("active");
	$("#5year").addClass("active");
	fetchNumberKilled(county,5);
	fetchNumberInjured(county,5);
	fetchPedestrianInjured(county,5);
	fetchBicyclistInjured(county,5);
});

function showLoader(){
	$(".chart-row").addClass("hide");
	$(".spinner").removeClass("hide");
}
function hideLoader(){
	$(".spinner").addClass("hide");
	$(".chart-row").removeClass("hide");
}
function fetchNumberKilled(county, year){
	$.ajax({
		url:'/forecast/killed',
		data: {
			county : county,
			years : year
		},
		type:'POST',
		async: true,
		success:function(data){
			hideLoader();
			console.log(data);
			var years = data.x_observed.concat(data.x_prediction);
			var len = data.x_observed.length;
			var zerosArray  = new Array(len).fill(0);
			console.log(zerosArray);
			if(data.y_observed.every(element => element == 0)){
				$("#fatalities-prediction").html("No Fatalities");
			}else{
				$("#fatalities-prediction").html("");
				loadFatalitiesChart(years, data.y_observed, data.y_prediction, county, zerosArray);
			}
		}
	});
}
function fetchNumberInjured(county, year){
	$.ajax({
		url:'/forecast/injured',
		data: {
			county : county,
			years : year
		},
		type:'POST',
		async: true,
		success:function(data){
			console.log(data);
			var years = data.x_observed.concat(data.x_prediction);
			var len = data.x_observed.length;
			var zerosArray  = new Array(len).fill(0);
			console.log(zerosArray);
			if(data.y_observed.every(element => element == 0)){
				$("#injured-prediction").html("None Injured");
			}else{
				$("#injured-prediction").html("");
				loadInjuredChart(years, data.y_observed, data.y_prediction, county, zerosArray);
			}
		}
	});
}

function fetchPedestrianInjured(county, year){
	$.ajax({
		url:'/forecast/pedestrian/injured',
		data: {
			county : county,
			years : year
		},
		type:'POST',
		async: true,
		success:function(data){
			hideLoader();
			console.log(data);
			var years = data.x_observed.concat(data.x_prediction);
			var len = data.x_observed.length;
			var zerosArray  = new Array(len).fill(0);
			console.log(zerosArray);
			if(data.y_observed.every(element => element == 0)){
				$("#pedestrian-injured-prediction").html("No Pedestrian Injured");
			}else{
				$("#pedestrian-injured-prediction").html("");
				loadPedestrianInjuredChart(years, data.y_observed, data.y_prediction, county, zerosArray);
			}
		}
	});

}
function fetchBicyclistInjured(county, year){
	$.ajax({
		url:'/forecast/bicyclist/injured',
		data: {
			county : county,
			years : year
		},
		type:'POST',
		async: true,
		success:function(data){
			console.log(data);
			var years = data.x_observed.concat(data.x_prediction);
			var len = data.x_observed.length;
			var zerosArray  = new Array(len).fill(0);
			console.log(zerosArray);
			if(data.y_observed.every(element => element == 0)){
				$("#bicyclist-injured-prediction").html("No Bicyclist Injured");
			}else{
				$("#bicyclist-injured-prediction").html("");
				loadBicyclistInjuredChart(years, data.y_observed, data.y_prediction, county, zerosArray);
			}
		}
	});
}
function loadFatalitiesChart(years, f_observed, f_predicted, county,zerosArray){
	Highcharts.chart('fatalities-prediction', {
	    chart: {
	        type: 'column'
	    },
	    title : {
	    	text : (function() {
						if (county != "") {
						  return 'Fatalities - ' + county.toLowerCase() + ' county' ;
						} else {
						  return 'Fatalities - All Counties';
						}
					})()
	    },
	    xAxis : {
	       categories: years
	    },
	    yAxis :{
	    	min : 0,
	    	title : {
	    		text :"Number of Fatalities"
	    	}
	    },
	    series: [{
	    	name : 'No of Fatalities',
	        data: f_observed,
	        color:'#579BDD'
	    }, {
	    	name : 'No of Fatalities Predictions',
	    	data: zerosArray.concat(f_predicted),
	    	color:'#69CD4B'

	    }],
			    
	});	
}


function loadInjuredChart(years, i_observed, i_predicted, county,zerosArray){
	Highcharts.chart('injured-prediction', {
	    chart: {
	        type: 'column'
	    },
	    title : {
	    	text : (function() {
						if (county != "") {
						  return 'Number of People Injured - ' + county.toLowerCase() + ' county';
						} else {
						  return 'Number of People Injured - All Counties';
						}
			})()
 	    },
	    xAxis : {
	       categories: years
	    },
	    yAxis :{
	    	min : 0,
	    	title : {
	    		text :"Number of Total People Injured"
	    	}
	    },
	    series: [{
	    	name : 'Number of Total People Injured',
	        data : i_observed,
	        color:'#579BDD'
	    }, {
	    	name : 'Number of Total People Injured Predictions',
	    	data : zerosArray.concat(i_predicted),
	    	color:'#69CD4B'
	    }],
			    
	});
}

function loadPedestrianInjuredChart(years, p_observed, p_predicted, county, zerosArray){
	Highcharts.chart('pedestrian-injured-prediction', {
	    chart: {
	        type: 'column'
	    },
	    title : {
	    	text : (function() {
						if (county != "") {
						  return 'Number of Pedestrian Injured - ' + county.toLowerCase() + ' county';
						} else {
						  return 'Number of Pedestrian Injured - All Counties';
						}
			})()
 	    },
	    xAxis : {
	       categories: years
	    },
	    yAxis :{
	    	min : 0,
	    	title : {
	    		text :"Number of Pedestrian Injured"
	    	}
	    },
	    series: [{
	    	name : 'Number of Pedestrian Injured',
	        data : p_observed,
	        color:'#579BDD'
	    }, {
	    	name : 'Number of Pedestrian Injured Predictions',
	    	data : zerosArray.concat(p_predicted),
	    	color:'#69CD4B'
	    }],
			    
	});
}
function loadBicyclistInjuredChart(years, b_observed, b_predicted, county, zerosArray){
	Highcharts.chart('bicyclist-injured-prediction', {
	    chart: {
	        type: 'column'
	    },
	    title : {
	    	text : (function() {
						if (county != "") {
						  return 'Number of Bicyclist Injured - ' + county.toLowerCase() + ' county';
						} else {
						  return 'Number of Bicyclist Injured - All Counties';
						}
			})()
 	    },
	    xAxis : {
	       categories: years
	    },
	    yAxis :{
	    	min : 0,
	    	title : {
	    		text :"Number of Bicyclist Injured"
	    	}
	    },
	    series: [{
	    	name : 'Number of Bicyclist Injured',
	        data : b_observed,
	        color:'#579BDD'
	    }, {
	    	name : 'Number of Bicyclist Injured Predictions',
	    	data : zerosArray.concat(b_predicted),
	    	color:'#69CD4B'
	    }],
			    
	});
}

})