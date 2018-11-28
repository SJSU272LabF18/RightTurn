function loadFatalitiesChart(years, f_observed, f_predicted, county, zerosArray){

	Highcharts.chart('forecast-killed', {
	    chart: {
	        type: 'column'
	    },
	    title : {
	    	text : 'Fatalities - '
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
	    	data:zerosArray.concat(f_predicted),
	    	color:'#69CD4B'

	    }],
			    
	}).setTitle({text : 'New Title'});	
}


function loadInjuredChart(years, i_observed, i_predicted, county, zerosArray){
	alert(county);
	Highcharts.chart('forecast-injured', {
	    chart: {
	        type: 'column'
	    },
	    title : {
	    	text : 'No of People Injured - '
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
			    
	}).setTitle({text : 'New'});
}

function fetchNumberKilled(county, year){
	$.ajax({
		url:'/forecast/killed',
		data: {
			county : county,
			years : year
		},
		type:'POST',
		success:function(data){
			console.log(data);
			var years = data.x_observed.concat(data.x_prediction);
			var zerosArray  = new Array(years.length()).fill(0);
			loadFatalitiesChart(years, data.y_observed, data.y_prediction, county,zerosArray);
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
		success:function(data){
			console.log(data);
			var years = data.x_observed.concat(data.x_prediction);
			var zerosArray  = new Array(years.length()).fill(0);
			loadInjuredChart(years, data.y_observed, data.y_prediction, county,zerosArray);
		}
	});
}


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
