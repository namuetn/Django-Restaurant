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


// Using Jquery
$(document).ready(function() {
    $('.add-to-cart').on('click', function(e) {
        e.preventDefault()
        food_id = $(this).attr('data-id')
        url = $(this).attr('data-url')

        $.ajax({
            type: "GET",
            url: url,
            success: function (response) {
                console.log(response);
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info').then(function() {
                        window.location = '/login'
                    })
                } else if (response.status == 'Failed') {
                    swal(response.message, '', 'error')
                } else {
                    $('#cart-counter').html(response.cart_counter['cart_count']);
                    $('#qty-' + food_id).html(response.quantity);

                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )
                }
            }
        });
    })

    // Place the cart item quantity on load
    $('.cart-qty').each(function () {
        var id = $(this).attr('id');
        var quantity = $(this).attr('data-qty');
        $('#' + id).html(quantity);
    });

    $('.decrease-cart').on('click', function(e) {
        e.preventDefault()
        food_id = $(this).attr('data-id')
        url = $(this).attr('data-url')
        cart_id = $(this).attr('id')

        $.ajax({
            type: "GET",
            url: url,
            success: function (response) {
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info').then(function() {
                        window.location = '/login'
                    })
                } else if (response.status == 'Failed') {
                    swal(response.message, '', 'error')
                } else {
                    $('#cart-counter').html(response.cart_counter['cart_count']);
                    $('#qty-' + food_id).html(response.quantity);

                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )

                    if (window.location.pathname == '/cart/') {
                        if (response.quantity == 0) {
                            $('#cart-item-' + cart_id).remove();
                        }
                        checkEmptyCart()
                    }
                }
            }
        });
    })

    $('.delete-cart').on('click', function(e) {
        e.preventDefault()
        cart_id = $(this).attr('data-id')
        url = $(this).attr('data-url')

        $.ajax({
            type: "GET",
            url: url,
            success: function (response) {
                if (response.status == 'Failed') {
                    swal(response.message, '', 'error')
                } else {
                    $('#cart-counter').html(response.cart_counter['cart_count']);
                    swal(response.status, response.message, 'success')

                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )

                    if (window.location.pathname == '/cart/') {
                        $('#cart-item-' + cart_id).remove();
                        checkEmptyCart()
                    }
                }
            }
        });
    })

    function checkEmptyCart() {
        var cart_counter = $('#cart-counter').html();
        if (cart_counter == 0) {
            $('#empty-cart').removeClass('d-none');
        } else {
            $('#empty-cart').addClass('d-none');
        }
    }

    function applyCartAmounts(subtotal, tax, grand_total) {
        if (window.location.pathname == '/cart/') {
            $('#subtotal').html(subtotal);
            $('#tax').html(tax);
            $('#total').html(grand_total);
        }
    }
})
