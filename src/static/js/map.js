	
	// control that shows state info on hover
	var info = L.control();

	info.onAdd = function (map) {
		this._div = L.DomUtil.create('div', 'info');
		this.update();
		return this._div;
	};

	info.update = function (props) {
		this._div.innerHTML = (props ?
			'<b>' + props.name + '</b><br />' + props.density +' accidents'
			: 'Hover over a state');
	};

	info.addTo(map);

	function getColor(d) {
		return d > 500 ? '#800026' :
				d > 300   ? '#FEB24C' :
				d > 20   ? '#3BCA25' :
						   '#23b70c';
	}

	function style(feature) {
		return {
			weight: 2,
			opacity: 0.2,
			color: 'white',
			dashArray: '3',
			fillOpacity: 0.7,
			fillColor: getColor(feature.properties.density)
		};
	}
	
	function highlightFeature(e) {
		var layer = e.target;

		layer.setStyle({
			weight: 5,
			color: '#666',
			dashArray: '',
			fillOpacity: 0.7
		});

		if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
			layer.bringToFront();
		}
        
		info.update(layer.feature.properties);

	}
	
	var geojson;

	function resetHighlight(e) {
		geojson.resetStyle(e.target);
		info.update();
	}

	function getcountydata(e) {
		//map.fitBounds(e.target.getBounds());
		console.log(e);
		//alert(e.target.feature.id)
		window.location.href = '/searchbycounty?county='+e.target.feature.id;
		
	}

	function onEachFeature(feature, layer) {
		layer.on({
			mouseover: highlightFeature, 
			mouseout: resetHighlight,
			click: getcountydata
		});
	}

	geojson = L.geoJson(statesData, {
		style: style,
		onEachFeature: onEachFeature
	}).addTo(map);
	
	var legend = L.control({position: 'bottomleft'});

	legend.onAdd = function (map) {

		var div = L.DomUtil.create('div', 'info legend'),
			grades = [0, 20, 300, 500],
			labels = [];

		// loop through our density intervals and generate a label with a colored square for each interval
		for (var i = 0; i < grades.length; i++) {
			div.innerHTML +=
				'<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
				grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
		}

		return div;
	};

	legend.addTo(map);