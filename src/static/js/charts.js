google.charts.load("current", {packages:["corechart"]});
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() 
		{
			var data = google.visualization.arrayToDataTable([
			['Cause', 'Accident Number'],
			  ['Unknown Cause', 7],
			  ['Swinging too wide while making right turn',     11],
			  ['Failure to Signal Turn',      4],
			  ['Driving or Bicycling Under the Influence of Alcohol or Drug',  2],
			  ['Unsafe Speed', 2]
			]);

			var options = {
			  title: 'Collision Percentage by Primary Collision Factor',
			  is3D: true,
			};

			var chart = new google.visualization.PieChart(document.getElementById('piechart_3d'));
			chart.draw(data, options);
		}
	  function ontabClick(sel_tab)
		{
			
		}
	  function openPage(pageName,elmnt,color)
		{
			var i, tabcontent, tablinks;
			tabcontent = document.getElementsByClassName("tabcontent");
			for (i = 0; i < tabcontent.length; i++)
			{
				tabcontent[i].style.display = "none";
			}
			tablinks = document.getElementsByClassName("tablink");
			for (i = 0; i < tablinks.length; i++) 
			{
				tablinks[i].style.backgroundColor = "";
			}
			document.getElementById(pageName).style.display = "block";
			elmnt.style.backgroundColor = color;
		}
		// Get the element with id="defaultOpen" and click on it
		document.getElementById("defaultOpen").click();