function initMap(allCars) {

    //limits the map to vienna
    var vienna = {lat: 48.205, lng: 16.376}; 
    var map = new google.maps.Map(document.getElementById('map'), { 
        zoom: 12, 
        center: vienna
    });  

    for (var i = 0; i < allCars.length; i++) {

        var pinColor = allCars[i].color;
        var pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor,
        new google.maps.Size(21, 34),
        new google.maps.Point(0,0),
        new google.maps.Point(10, 34));
        var pinShadow = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_shadow",
        new google.maps.Size(40, 37),
        new google.maps.Point(0, 0),
        new google.maps.Point(12, 35));

        var latLng = new google.maps.LatLng(allCars[i].gps_lat,allCars[i].gps_long);
        var marker = new google.maps.Marker({
            position: latLng,
            map: map,
            title: allCars[i].company+' '+allCars[i].model,
            icon: pinImage,
            shadow: pinShadow
        }); 
    }
}