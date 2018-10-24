var hazards, campwindow, markerCluster;
var addmarker, formwindow, messagewindow;
var map;

function initMap() {

  map = new google.maps.Map(document.querySelector('#map'), {
    zoom: 14,
    center: window.mapCenter,
    styles:
    [
      {
        "elementType": "geometry",
        "stylers": [
          {
            "color": "#f5f5f5"
          }
        ]
      },
      {
        "elementType": "labels.icon",
        "stylers": [
          {
            "visibility": "on"
          }
        ]
      },
      {
        "elementType": "labels.text.fill",
        "stylers": [
          {
            "color": "#616161"
          }
        ]
      },
      {
        "elementType": "labels.text.stroke",
        "stylers": [
          {
            "color": "#f5f5f5"
          }
        ]
      },
      {
        "featureType": "administrative.land_parcel",
        "elementType": "labels.text.fill",
        "stylers": [
          {
            "color": "#bdbdbd"
          }
        ]
      },
      {
        "featureType": "poi",
        "elementType": "geometry",
        "stylers": [
          {
            "color": "#eeeeee"
          }
        ]
      },
      {
        "featureType": "poi",
        "elementType": "labels.text.fill",
        "stylers": [
          {
            "color": "#757575"
          }
        ]
      },
      {
        "featureType": "poi.park",
        "elementType": "geometry",
        "stylers": [
          {
            "color": "#e5e5e5"
          }
        ]
      },
      {
        "featureType": "poi.park",
        "elementType": "labels.text.fill",
        "stylers": [
          {
            "color": "#9e9e9e"
          }
        ]
      },
      {
        "featureType": "road",
        "elementType": "geometry",
        "stylers": [
          {
            "color": "#ffffff"
          }
        ]
      },
      {
        "featureType": "road.arterial",
        "elementType": "labels.text.fill",
        "stylers": [
          {
            "color": "#757575"
          }
        ]
      },
      {
        "featureType": "road.highway",
        "elementType": "geometry",
        "stylers": [
          {
            "color": "#dadada"
          }
        ]
      },
      {
        "featureType": "road.highway",
        "elementType": "labels.text.fill",
        "stylers": [
          {
            "color": "#616161"
          }
        ]
      },
      {
        "featureType": "road.local",
        "elementType": "labels.text.fill",
        "stylers": [
          {
            "color": "#9e9e9e"
          }
        ]
      },
      {
        "featureType": "transit.line",
        "elementType": "geometry",
        "stylers": [
          {
            "color": "#e5e5e5"
          }
        ]
      },
      {
        "featureType": "transit.station",
        "elementType": "geometry",
        "stylers": [
          {
            "color": "#eeeeee"
          }
        ]
      },
      {
        "featureType": "water",
        "elementType": "geometry",
        "stylers": [
          {
            "color": "#c9c9c9"
          }
        ]
      },
      {
        "featureType": "water",
        "elementType": "labels.text.fill",
        "stylers": [
          {
            "color": "#9e9e9e"
          }
        ]
      }
    ]
  });
  var infoWindow = new google.maps.InfoWindow;
  // Set a default origin for demonstration
  var origin = {
    lat: 37.782551,
    lng: -122.445368
  };

  // ///Try HTML5 geolocation.
  // if (navigator.geolocation) {
  //   navigator.geolocation.getCurrentPosition(function (position) {
  //     var pos = {
  //       lat: position.coords.latitude,
  //       lng: position.coords.longitude
  //     };

  //     infoWindow.setPosition(pos);
  //     infoWindow.setContent('Location found.');
  //     infoWindow.open(map);
  //     map.setCenter(pos);
  //   }, function () {
  //     handleLocationError(true, infoWindow, map.getCenter());
  //   });
  // } else {
  //   // Browser doesn't support Geolocation
  //   handleLocationError(false, infoWindow, map.getCenter());
  // }
  hazards = new google.maps.MVCArray();
  // getPoints(hazards);
  var heatmap = new google.maps.visualization.HeatmapLayer({
    data: hazards, //getPoints(),
    map: map
  });
  // Hide the markers rendered via map.data.loadGeoJson, since we'll add markers 
  // seperately with MarkerClusterer.
  map.data.setStyle({
    visible: false
  });

  // Info window will show a property's information when its marker is clicked.
  infoWindow = new google.maps.InfoWindow();
  infoWindow.setOptions({
    pixelOffset: new google.maps.Size(0, -30)
  });

  // We call map.data.loadGeoJson every time the bounds_changed event is triggered, 
  // which sometimes can occur multiple times very quickly in succession, so we 
  // only do this inside a function run via setTimeout, which is cancelled each 
  // time the event is triggered. timeoutHandler stores the handler for this.
  let timeoutHandler = 0;

  // MarkerClusterer instance which we store to allow us to call clearMarkers 
  // on it, each time the property data is received after map.data.loadGeoJson
  // being called.
  markerCluster = null;

  // Stores the bounds used for retrieving data, so that when the bounds_changed 
  // event is triggered, we don't request new data if the new bounds fall within 
  // dataBounds, for example when zooming in.
  let dataBounds = null;

  // Loads properties via map.data.loadGeoJson inside a setTimeout handler, which is 
  // cancelled each time loadProperties is called.
  function loadProperties() {

    clearTimeout(timeoutHandler);
    timeoutHandler = setTimeout(() => {

      // For retrieving data, use a larger (2x) bounds than the actual map bounds,
      // which will allow for some movement of the map, or one level of zooming 
      // out, without needed to load new data.
      const ne = map.getBounds().getNorthEast();
      const sw = map.getBounds().getSouthWest();
      const extendedLat = ne.lat() - sw.lat();
      const extendedLng = ne.lng() - sw.lng();
      dataBounds = new google.maps.LatLngBounds(
        new google.maps.LatLng(sw.lat() - extendedLat, sw.lng() - extendedLng),
        new google.maps.LatLng(ne.lat() + extendedLat, ne.lng() + extendedLng)
      );

      // Build the querystring of parameters to use in the URL given to 
      // map.data.loadGeoJson, which consists of the various form field 
      // values and the current bounding box.
      const params = {
        ne: dataBounds.getNorthEast().toUrlValue(),
        sw: dataBounds.getSouthWest().toUrlValue()
      };
    
      const camp_url = window.campsGeoJsonUrl + '?' + Object.keys(params).map((k) => k + '=' + params[k]).join('&');
      const people_url = window.peopleGeoJsonUrl + '?' + Object.keys(params).map((k) => k + '=' + params[k]).join('&');

      map.data.loadGeoJson(camp_url, null, (features) => {

        // Build an array of markers, one per property.
        const markers = features.map((feature) => {

          const marker = new google.maps.Marker({
            position: feature.getGeometry().get(0),
            label: 'C',
            title: 'Camp: ' + feature.getProperty('address')
          });
          // Show the property's details in the infowindow when 
          // the marker is clicked.
          var clickHandler = new ClickEventHandler(map, origin, marker, feature);
          marker.setMap(map);
          return marker;
        });
      });

      map.data.loadGeoJson(people_url, null, (features) => {

        // Clear the previous marker cluster.
        if (markerCluster !== null) {
          markerCluster.clearMarkers();
        }

        // Build an array of markers, one per property.
        const markers = features.map((feature) => {

          const marker = new google.maps.Marker({
            position: feature.getGeometry().get(0),
            label: 'P'
          });
          return marker;
        });

        // Add a marker clusterer to manage the markers.
        markerCluster = new MarkerClusterer(map, markers, {
          imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
        });
      });

      const hazard_url = window.hazardsGeoJsonUrl + '?' + Object.keys(params).map((k) => k + '=' + params[k]).join('&');

      map.data.loadGeoJson(hazard_url, null, (features) => {

        features.map((feature) => {
          hazards.push({location: feature.getGeometry().get(0), weight: feature.getProperty('weight')});
        });
      });
    }, 100);

    map.addListener('click', function (e) {
      placeMarkerAndPanTo(e.latLng, map, hazards);
    });
    var script = document.createElement('script');

    // This example uses a local copy of the GeoJSON stored at
    // http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojsonp
    script.src = 'https://developers.google.com/maps/documentation/javascript/examples/json/earthquake_GeoJSONP.js';
    document.getElementsByTagName('head')[0].appendChild(script);
    // Add a basic style.
    map.data.setStyle(function(feature) {
      var mag = Math.exp(parseFloat(feature.getProperty('mag'))) * 0.1;
      return /** @type {google.maps.Data.StyleOptions} */({
        icon: {
          path: google.maps.SymbolPath.CIRCLE,
          scale: mag,
          fillColor: '#f00',
          fillOpacity: 0.35,
          strokeWeight: 0
        }
      });
    });  
}

  // Refresh data each time the map bounds change, and fall outside the 
  // bounds of currently loaded data.
  google.maps.event.addListener(map, 'bounds_changed', () => {
    if (dataBounds === null ||
      !dataBounds.contains(map.getBounds().getNorthEast()) ||
      !dataBounds.contains(map.getBounds().getSouthWest())) {
      loadProperties();
    }
  });
}

function eqfeed_callback(data) {
  map.data.addGeoJson(data);
}


var ClickEventHandler = function (map, origin, marker, feature) {
  this.origin = origin;
  this.map = map;
  this.marker = marker;
  this.feature = feature;
  this.directionsService = new google.maps.DirectionsService;
  this.directionsDisplay = new google.maps.DirectionsRenderer({
    draggable: true,
    map: map,
    panel: document.getElementById('right-panel')
  });
  this.directionsDisplay.addListener('directions_changed', function() {
    document.getElementById('right-panel').style.flexBasis = '25%';
    document.getElementById('map').style.flexBasis = '74%';
  });
  this.placesService = new google.maps.places.PlacesService(map);
  campwindow = new google.maps.InfoWindow;
  this.infowindowContent = document.getElementById('infowindow-content');
  campwindow.setContent(this.infowindowContent);

  // Listen for clicks on the map.
  this.marker.addListener('click', this.handleClick.bind(this));
};

ClickEventHandler.prototype.handleClick = function (event) {
  console.log('You clicked on: ' + event.latLng);
  // If the event has a placeId, use it.
  // if (event.placeId) {
  // console.log('You clicked on place:' + event.placeId);

  // Calling e.stop() on the event prevents the default info window from
  // showing.
  // If you call stop here when there is no placeId you will prevent some
  // other map click event handlers from receiving the event.
  event.stop();
  this.calculateAndDisplayRoute(event.latLng);
  this.getPlaceInformation();

};

ClickEventHandler.prototype.calculateAndDisplayRoute = function (latLng) {
  var me = this;
  this.directionsService.route({
    origin: this.origin,
    destination: latLng,
    travelMode: 'DRIVING'
  }, function (response, status) {
    if (status === 'OK') {
      me.directionsDisplay.setDirections(response);
    } else {
      window.alert('Directions request failed due to ' + status);
    }
  });
};

ClickEventHandler.prototype.getPlaceInformation = function () {
  var me = this;
  var feature = this.feature;
  const position = feature.getGeometry().get();
  campwindow.close();
  campwindow.setPosition(position);
  me.infowindowContent.children['place-img'].src = "https://maps.googleapis.com/maps/api/streetview?size=200x200&location=" +
    position.lat() + ',' + position.lng() + '&key=' + window.apiKey;
  me.infowindowContent.children['place-address'].textContent = feature.getProperty('address');
  me.infowindowContent.children['place-description'].textContent = feature.getProperty('description');
  me.infowindowContent.children['place-capacity'].textContent = "Capacity: " + feature.getProperty('capacity');
  me.infowindowContent.children['place-water'].textContent = "Water: " + feature.getProperty('water');
  me.infowindowContent.children['place-food'].textContent = "Food: " + feature.getProperty('food');
  me.infowindowContent.children['place-medicine'].textContent = "Medicine: " + feature.getProperty('medicine');
  campwindow.open(me.map);
};

// function handleLocationError(browserHasGeolocation, infoWindow, pos) {
//   infoWindow.setPosition(pos);
//   infoWindow.setContent(browserHasGeolocation ?
//     'Error: The Geolocation service failed.' :
//     'Error: Your browser doesn\'t support geolocation.');
//   infoWindow.open(map);
// }

function placeMarkerAndPanTo(latLng, map, hazards) {
  if (addmarker != null) addmarker.setMap(null);
  addmarker = new google.maps.Marker({
    position: latLng,
    map: map
  });
  map.panTo(latLng);

  // if (formwindow != null) formwindow.close();
  addmarker.infowindow = new google.maps.InfoWindow({
    content: document.getElementById('select-form-type')
  });

  messagewindow = new google.maps.InfoWindow({
    content: document.getElementById('message')
  });

  google.maps.event.addListener(addmarker.infowindow, 'domready', function () {
    document.getElementById("form-button").addEventListener("click", function (e) {
      whichForm();
      // saveData();
    });
  });
  addmarker.infowindow.open(map, addmarker);
}

function whichForm() {
  var type = document.getElementById('type').value;
  if (type == 'hazard') {
    addmarker.infowindow.close();     
    addmarker.infowindow = new google.maps.InfoWindow({
      content: document.getElementById('hazard-form')
    });
    google.maps.event.addListener(addmarker.infowindow, 'domready', function () {
      document.getElementById("form-button").addEventListener("click", function (e) {
        saveData('hazard');
      });
    });
    addmarker.infowindow.open(map, addmarker);
  } else if (type == "need-rescue") {
    addmarker.infowindow.close();     
    addmarker.infowindow = new google.maps.InfoWindow({
      content: document.getElementById('rescue-form')
    });
    google.maps.event.addListener(addmarker.infowindow, 'domready', function () {
      document.getElementById("form-button").addEventListener("click", function (e) {
        saveData('need-rescue');
      });
    });
    addmarker.infowindow.open(map, addmarker);
  }
}

function saveData(type) {
  var latLng = addmarker.getPosition();
  if (type == "hazard") {
    var description = escape(document.getElementById('description').value);
    var param = {
      headers: {
        "content-type": "application/json; charset=UTF-8"
      },
      body: JSON.stringify({
        "data": {
          "description": description,
        },
        "latlng": latLng.toJSON(),
      }),
      method: "POST"
    };
    fetch(window.addHazardUrl, param)
      .then(res => res.json())
      .then(response => {
        if (response['status'] == 200) {
          addmarker.infowindow.close();
          addmarker.setMap(null);
          messagewindow.open(map, addmarker);
          console.log('Success:', JSON.stringify(response))
        }
        else {
          console.log('Failure:', JSON.stringify(response))
        }
      })
      .catch(error => console.error('Error:', error));

    hazards.push(latLng);

  } else if (type == "need-rescue") {
    var name = escape(document.getElementById('name').value);
    var phone = escape(document.getElementById('phone').value);
    var friendName = escape(document.getElementById('friend-name').value);
    var friendPhone = escape(document.getElementById('friend-phone').value);
    var param = {
      headers: {
        "content-type": "application/json; charset=UTF-8"
      },
      body: JSON.stringify({
        "data": {
          "name" : name,
          "phone" : phone,
          "emergencyName" : friendName,
          "emergencyPhone" : friendPhone,
        },
        "latlng" : latLng.toJSON(),
      }),
      method: "POST"
    };
    fetch(window.addPersonUrl, param)
      .then(res => res.json())
      .then(response => {
        if (response['status'] == '200') {
          addmarker.infowindow.close();
          markerCluster.addMarker(new google.maps.Marker({
            position: addmarker.getPosition(),
            map: map,
            label: 'P', 
          }));
          addmarker.setMap(null);
          messagewindow.open(map, addmarker);
          console.log('Success:', JSON.stringify(response))
        }
        else {
          console.log('Failure:', JSON.stringify(response))
        }
      })
      .catch(error => console.error('Error:', error));
  }
}