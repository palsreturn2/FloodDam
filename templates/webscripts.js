function initMap() 
{
	var myLatLng = {lat: 23.2324, lng: 87.0786};
	var mapDiv = document.getElementById('map');
	var map = new google.maps.Map(mapDiv, {center: {lat: 23.2324, lng: 87.0786},zoom: 15});
	var marker = new google.maps.Marker({position: myLatLng, map: map,title: 'Hello World!'});        
}
