let autocomplete;

function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            //default in this app is "IN" - add your country code
            componentRestrictions: {'country': ['vn', 'us']},
        })
    // function to specify what should happen when the prediction is clicked
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged () {
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry) {
        document.getElementById('id_address').placeholder = "Start typing...";
    } else {
        console.log('place name=>', place.name)
    }

    // get the address components and assign them to the fields
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value

    geocoder.geocode({'address': address}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat()
            var longitude = results[0].geometry.location.lng()

            document.getElementById('id_latitude').value = latitude
            document.getElementById('id_longitude').value = longitude
            document.getElementById('id_address').value = address
        }
    })

    // loop through the address components and assign other address data
    for (let i = 0; i < place.address_components.length; i++) {
        for (let j = 0; j < place.address_components[i].types.length; j++) {
            if (place.address_components[i].types[j] == 'country') {
                document.getElementById('id_country').value = place.address_components[i].long_name
            }

            if (place.address_components[i].types[j] == 'administrative_area_level_1') {
                document.getElementById('id_state').value = place.address_components[i].long_name
            }

            if (place.address_components[i].types[j] == 'locality') {
                document.getElementById('id_city').value = place.address_components[i].long_name
            }

            if (place.address_components[i].types[j] == 'postal_code') {
                document.getElementById('id_pin_code').value = place.address_components[i].long_name
            } else {
                document.getElementById('id_pin_code').value = ''
            }
        }
        
    }
}
