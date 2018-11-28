$(document).ready(function(){

 fetchNumberKilled("LOS ANGELES",1);
 fetchNumberInjured("LOS ANGELES",1);

document.getElementById("1year").addEventListener("click",function(){
	var county = document.getElementById("county").value;
	fetchNumberKilled(county,1);
	fetchNumberInjured(county,1);
});
document.getElementById("2year").addEventListener("click",function(){
	var county = document.getElementById("county").value;
	fetchNumberKilled(county,2);
	fetchNumberInjured(county,2);
});
document.getElementById("5year").addEventListener("click",function(){
	var county = document.getElementById("county").value;
	fetchNumberKilled(county,5);
	fetchNumberInjured(county,5);
});

document.getElementById("county").addEventListener('change',function(){
	var county = document.getElementById("county").value;
	fetchNumberKilled(county,5);
	fetchNumberInjured(county,5);
});

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
				$("#injured-prediction").html("No Injuries");
			}else{
				$("#injured-prediction").html("");
				loadInjuredChart(years, data.y_observed, data.y_prediction, county, zerosArray);
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
	    		text :"Number of People Injured"
	    	}
	    },
	    series: [{
	    	name : 'No of People Injured',
	        data : i_observed,
	        color:'#579BDD'
	    }, {
	    	name : 'No of Injured Predictions',
	    	data : zerosArray.concat(i_predicted),
	    	color:'#69CD4B'
	    }],
			    
	});
}

})