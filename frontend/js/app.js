/**
 * 
 * config & init
 * 
 * 
 * 
 * 
 * 
 */

appSettings = {
    "debbuging": true,
    "messageHideAfter": 2000, // ms
    "showSystemLoadingAfter": 100, //ms
    "ws1": {
        "url": "http://ec2-52-29-144-248.eu-central-1.compute.amazonaws.com/api"
    },
};

$(document).ready(function() {
    //login click function - login page
    $('body.login .login-btn').click(function(e) {
        login($('body.login #inputUname').val(), $('body.login #inputPassword').val());
        e.preventDefault();
    })

    //init cars page
    if($('body.cars').length && false) {
        insertAvailableCars(currency);

        userId = getUserId();
        if(userId == null) {
            log("getUserId: null");
            showError("Es trat ein Problem auf!");
        } else {
            insertRentedCars(userId);
        }
    }

    //change currency -> reload available cars
    $('#currency').change(function(e) {
        currency = $(this).val();
        insertAvailableCars(currency);
        e.preventDefault();
    })
});

/**
 * 
 * login functionality
 * 
 * 
 * 
 * 
 * 
 * 
 */

 /**
  * Login - store auth token and redirect to cars.html
  */
function login(uname, passw) {
    showAppLoading();

    log("login: "+uname, passw);

    ajaxRequest(
        appSettings.ws1.url + '/token',    // url
        'GET',  // method
        { // headers
            "Authorization": "Basic " + Base64.encode(uname + ':' + passw)
        },
        'json', // returnType
        {}  // para
    ).done(function(data) {
        log(['login:', data]);
        hideAppLoading();

        storeAuthToken(data.token, Date.now()/1000 + data.duration);

        window.open("/cars.html","_self");
    })
    .fail(function(jqXHR) {
        hideAppLoading();
        showErrorMessage(jqXHR, 'Anmeldung fehlgeschlagen!');
        handleError(jqXHR);
    });
}

/**
 * stores auth token locally
 */
function storeAuthToken(token, validTill) {
    // try to store it in localStorage otherwise use normal JS variable
    if(browserSupportLocalStorage()) {
        localStorage.setItem('ws1Token', token);
        localStorage.setItem('ws1TokenValidTill', validTill);
    } else {
        ws1Token = token;
        ws1TokenValidTill = validTill;
    }
}

/**
 * returns Auth Token - valid or invalid
 */
function getAuthToken() {
    if(browserSupportLocalStorage()) {
        return localStorage.getItem('ws1Token');
    } else {
        return ws1Token;
    }
}

/**
 * extract user id from jwt auth token (not encrypted)
 */
function getUserId(token) {
    // NOTE: jwt token is not verified
    var parts = token.split('.');
    try {
        json = Base64.decode(parts[1]);
        return parseInt(JSON.parse(json).id);
    } catch (error) {
        return null;
    }
}


/**
 * 
 * model section for app functionality
 * 
 * 
 * 
 * 
 * 
 * 
 */

/**
 * get all available cars (cars that are not rented during the submitted timeframe) - request
 */
function getAllAvailableCars(start, end, currency) {

    // TODO: type of start, end
    if(currency.length != 3) {
        showError("Bitte gültige Währung angeben!");
        return;
    }

    return ajaxRequest(
        appSettings.ws1.url + '/car/available?currency='+currency,    // url
        'PUT',  // method
        { // headers
            "Authorization": "Basic " + getAuthToken() + ':' 
        },
        'json', // returnType
        { // para
            "start" : start,
            "end": end
        }  
    )
}

function newUser(n, p) {

    // TODO: type of start, end

    return ajaxRequest(
        appSettings.ws1.url + '/users',    // url
        'POST',  // method
        { // headers
            // "Authorization": "Basic " + getAuthToken() + ':' 
        },
        'json', // returnType
        JSON.stringify({ // para
            "username" : n,
            "password": p
        })
    )
}

/**
 * get all cars - request
 */
function getAllCars() {

    // TODO: type of start, end

    return ajaxRequest(
        appSettings.ws1.url + '/car/all',    // url
        'GET',  // method
        { // headers
            "Authorization": "Basic " + getAuthToken() + ':' 
        },
        'json', // returnType
        {} // para  
    )
}

/**
 * get all cars rented by the user - request
 */
function getAllRentedCars(userId) {
    return ajaxRequest(
        appSettings.ws1.url + '/user/' + parseInt(userID) + "/rented",    // url
        'GET',  // method
        { // headers
            "Authorization": "Basic " + getAuthToken() + ':' 
        },
        'json', // returnType
        {} // para
    )
}

/**
 * rent a car - request
 */
function rentCarRequest(carId, start, end) {

    // TODO: type of start, end

    return ajaxRequest(
        appSettings.ws1.url + '/car/' + parseInt(carId) + "/rent",    // url
        'PUT',  // method
        { // headers
            "Authorization": "Basic " + getAuthToken() + ':' 
        },
        'json', // returnType
        { // para
            "start" : start,
            "end": end
        }
    )
}

/**
 * return a car - request
 */
function returnCarRequest(carId) {

    // TODO: type of start, end

    return ajaxRequest(
        appSettings.ws1.url + '/car/' + parseInt(carId) + "/return",    // url
        'PUT',  // method
        { // headers
            "Authorization": "Basic " + getAuthToken() + ':' 
        },
        'json', // returnType
        {} // para
    )
}


/**
 * 
 *  app functionality
 * 
 * 
 * 
 * 
 * 
 * 
 */


/**
 * insert cars in the available cars section
 */
function insertAvailableCars(currency){
    showAppLoading();

    if(currency.length != 3) {
        showError("Bitte gültige Währung auswählen!");
        return;
    }

    // remove all displayed cars
    $('.availabe-cars-container').html("");

    getAllAvailableCars("2018-03-12", "2018-03-15", currency)
    .done(function(data) {
        log(['getAllAvailableCars:', data]);
        hideAppLoading();

        // insert HTML
        for (let i = 0; i < data.available.length; i++) {
            outputAvailableCar(car, data.available[i]);
        }

        // click functions
        $('.available-cars-container car .car-rent-btn').unbind('click').click(function(){
            rentCarOptionsOpen($(this).closest('.car').attr('data-id'));
        })
    })
    .fail(function(jqXHR) {
        hideAppLoading();
        showErrorMessage(jqXHR, 'Es konnten keine Autos geladen werden!');
        handleError(jqXHR);
    });
}

/**
 * outputs the HTML of a available car
 */
function outputAvailableCar(car) {
//     var html = ''+
// '<div class="car" data-id="' + car.id + '">'+
//     '<div class="line-1">'+
//         '<div class="car-description car-img"><img src="img/sedan-car-model.svg"></div>'+
//         '<div class="car-description car-color" style="background-color: ' + car.color + '"></div>'+
//         '<div class="car-description car-label">' + car.company + '</div>'+
//         '<div class="car-description car-model">' + car.model + '</div>'+
//         '<div class="clearfix"></div>'+
//     '</div><div class="line-2">'+
//         '<div class="car-description car-price">' + car.price_per_day + '/Tag</div>'+
//         '<div class="car-description car-rent"><button type="button" class="btn btn-primary car-rent-btn">ausborgen</button></div>'+
//         '<div class="clearfix"></div>'+
//     '</div><div class="clearfix"></div>'+
// '</div>';

    var html = ''+
    '<div class="card car">'+
    '<img class="car-img" src=" http://flask-env.igdtepjkiu.eu-central-1.elasticbeanstalk.com/static/img/ferrari.jpg" alt="car image">'+
    '<div class="card-body">'+
        '<h5 class="card-title">'+
            '<span class="car-description car-label">' + car.company + '</span>&nbsp;'+
            '<span class="car-description car-model">' + car.model + '</span>'+
        '</h5>'+
        '<span class="car-description car-price">' + car.price_per_day + '/Tag</span>'+
        '<button type="button" class="btn btn-primary car-rent-btn">ausborgen</button>'+
        '<div class="clearfix"></div>'+
   ' </div>'+
'</div>';

    $('.available-cars-container').append(html);
}


/**
 * insert cars in the rented cars section
 */
function insertRentedCars(userId){
    showAppLoading();

    // remove all displayed cars
    $('.rented-cars-container').html("");

    // TODO: type of start, end
    $.when(
        getAllCars(),
        getAllRentedCars(userId)
    )
    .done(function(carsReturn, rentedReturn) {
        log(['getAllRentedCars:', data]);
        hideAppLoading();

        // insert HTML
        for (let i = 0; i < rentedReturn.rentals.length; i++) {
            var car_id = rentedReturn.rentals[i].car_id;
            var car = null;

            for (let j = 0; j < carsReturn.available.length; j++) {
                if(carsReturn.available[j].id == car_id)
                    car = carsReturn.available[j];                
            }
            if(car == null) {
                showError("Fehler: Auto konnte nicht gefunden werden!");
                log("insertRentedCars: car was not found");
                return;
            }

            outputRentedCar(car, rentedReturn.rentals[i]);
        }

        // update counter in nav
        updateRentedCarsCounter(rentedReturn.rentals.length);

        // click functions
        $('.rented-cars-container car .car-return-btn').unbind('click').click(function(){
            returnCar(
                parseInt($(this).closest('.car').attr('data-id'))
            );
        })
    })
    .fail(function(jqXHR) {
        hideAppLoading();
        showErrorMessage(jqXHR, 'Es konnten deine ausgeborgten Autos nicht geladen werden!');
        handleError(jqXHR);
    });
}

/**
 * outputs the HTML of a rented car
 */
function outputRentedCar(car, infos) {
    var html = ''+
'<div class="car" data-id="' + car.id + '">'+
    '<div class="line-1">'+
        '<div class="car-description car-img"><img src="img/sedan-car-model.svg"></div>'+
        '<div class="car-description car-color" style="background-color: ' + car.color + '"></div>'+
        '<div class="car-description car-label">' + car.company + '</div>'+
       ' <div class="car-description car-model">' + car.model + '</div>'+
       ' <div class="clearfix"></div>'+
    '</div><div class="line-2">'+
        '<div class="car-description car-price">' + car.price_per_day + '/Tag</div>'+
        '<div class="car-description car-rent-since">seit ' + infos.rented_from + '</div>'+
        '<div class="car-description car-costs">= ' + infos.total_price + '</div>'+
        '<div class="car-description car-return"><button type="button" class="btn btn-primary car-return-btn">retournieren</button></div>'+
        '<div class="clearfix"></div>'+
    '</div><div class="clearfix"></div>'+
'</div>';

    var html = ''+
    '<div class="card car">'+
    '<img class="car-img" src=" http://flask-env.igdtepjkiu.eu-central-1.elasticbeanstalk.com/static/img/ferrari.jpg" alt="car image">'+
    '<div class="card-body">'+
        '<h5 class="card-title">'+
            '<span class="car-description car-label">' + car.company + '</span>&nbsp;'+
            '<span class="car-description car-model">' + car.model + '</span>'+
        '</h5>'+
        '<div class="car-description car-price">' + car.price_per_day + '/Tag</div>'+
        '<div class="car-description car-rent-since">seit 18.8.2016</div>'+
        '<span class="car-description car-costs">= 240,-€</span>'+
        '<button type="button" class="btn btn-primary car-return-btn">retournieren</button>'+
        '<div class="clearfix"></div>'+
    ' </div>'+
    '</div>';

    $('.rented-cars-container').append(html);
}

/**
 * return a car
 */
function returnCar(carId) {
    showAppLoading();

    returnCarRequest(carId)
    .done(function(data) {
        log(['returnCar:', data]);
        hideAppLoading();

        //remove rented car
        $('.rented-cars-container').find('car[data-id="' + carId + '"]').remove();

        //update view
        insertAvailableCars(currency);


        showMessage("Danke fürs zurück bringen!");
    })
    .fail(function(jqXHR) {
        hideAppLoading();
        showErrorMessage(jqXHR, 'Das Auto konnte nicht retoniert werden!');
        handleError(jqXHR);
    });
}

/**
 * open rent car options-popup
 */
function rentCarOptionsOpen(carId) {
    $('#carId').val(parseInt(carId));

    $('#rentCarOptions .rentCar-btn').unbind('click').click(function(){
        var startDate = getDateFromForm($('#startDate'));
        var endDate = getDateFromForm($('#startDate'));
        if(startDate != null && endDate != null) {
            rentCar(
                parseInt(carId),
                startDate,
                endDate
            );
        } else {
            showError("Bitte Start und End Datum im Format YYYY-MM-DD angeben.")
        }
    });
    $('#rentCarOptions').modal('show');
}

/**
 * rent a car
 */
function rentCar(carId, start, end) {
    showAppLoading();

    rentCarRequest(carId, start, end)
    .done(function(data) {
        log(['rentCar:', data]);
        hideAppLoading();

        //remove available car
        $('.availabe-cars-container').find('car[data-id="' + carId + '"]').remove();

        //update view
        insertRentedCars(userId);

        showMessage("Viel Spaß mit deinem Auto!");
    })
    .fail(function(jqXHR) {
        hideAppLoading();
        showErrorMessage(jqXHR, 'Das Auto konnte nicht ausgeborgt werden!');
        handleError(jqXHR);
    });
}

/**
 * update the rented car counter in Header
 */
function updateRentedCarsCounter(amount) {
    $('nav .rented-cars-counter').text(parseInt(amount));
}

/**
 * get date from input type date - returns timestamp in s
 */
function getDateFromForm(element) {
    var value = element.val();
    var date = Date.parse(value); // timestamp in ms
    if(date > 0)
        return null;
    return date/1000;
}


/**
 * 
 * Ajax functionality
 * 
 * 
 * 
 * 
 * 
 */

/**
* Ajax call,  returns a promise - jQuery based
*/
function ajaxRequest(url, method, headers, returnType, data) {
    /**
     * Description:
     * ----------- 
     * use following promise callbacks:
          .done(function() {
            alert( "success" );
          })
          .fail(function() {
            alert( "error" );
          })
          .always(function() {
            alert( "success or error" );
          });
    */
    log('ajax Request: ', data);

    return $.ajax({
        url: url,
        method: method,
        headers: headers,
        dataType: returnType,
        contentType: "application/json",
        data: data
    })
}






/**
 * 
 * Error Handling functionality
 * 
 * 
 * 
 * 
 * 
 * 
 */

/**
* show message in console - only in debug mode
* obj: Object/Sting/Array
*/
function log(obj){
    // returns all arguments in an array
    if(appSettings.debugging)
        console.debug(obj);
}

function logError(obj){
    // returns all arguments in an array
    console.error(obj);
}

/**
* how to handle a error
* obj: Object/Sting/Array
*/
function handleError(obj)
{
    // console log in debugging mode
    logError('error:',obj);
}

/**
* show error message
*/
function showErrorMessage(jqXHR, customMessage) {
    if(jqXHR.status == 400)
        showError('API Anbindungsfehler!');
    else if(jqXHR.status == 401)
        showError('Nicht Berechtigt!');
    else if(jqXHR.status == 404)
        showError('Ressource konnte nicht gefunden werden!');
    else if(jqXHR.status == 409)
        showError('Die Ressource scheint nicht mehr verfügbar zu sein!');
    else if(jqXHR.status == 500)
        showError('Es ist etwas schiefgelaufen!');
    else if(customMessage)
        showError(customMessage);
    else
        showError("Es trat ein unerwarteter Fehler auf!");
}


/**
 * 
 * User Feedback functionality
 * 
 * 
 * 
 * 
 * 
 * 
 */


/**
* show a message to a user - bootstrap based
*/
function showMessage(message)
{
    $('#showMessage .modal-body').text(message);
    $('#showMessage').modal('show');
}

/**
* show a error to a user - bootstrap based
*/
function showError(message)
{
    $('#showError .modal-body').text(message);
    $('#showError').modal('show');
}

/**
* show the application loading animation
*/
function showAppLoading()
{
    // if variable not defined - error
    if(typeof appLoading == "undefined") {
        appLoading = {'counter':0, 'id':null};
    }

    // if HTML not already created
    if(!$('#app-loading').length)
        $('body').append('<div id="app-loading" class="hide"><div class="loading-animation"></div></div>');


    if(appLoading.counter == 0)
    {
        var random=Math.floor(Math.random()*1000001);
        appLoading.id=random;
        setTimeout("displayAppLoading("+random+");",appSettings.showSystemLoadingAfter);
    }
    appLoading.counter++;
}

/**
* hide the application loading animation
*/
function hideAppLoading()
{
    appLoading.counter--;

	if(appLoading.counter <= 0)
	{
		if(!$('#app-loading').hasClass('hide'))
            $('#app-loading').addClass('hide');

		appLoading.counter = 0;
        appLoading.id = 0;
	}
}

/**
* display the application loaing animation
*/
function displayAppLoading(randomId) {
    if(appLoading.counter > 0 && randomId == appLoading.id)
	   $('#app-loading').removeClass('hide');
}


/**
 * 
 * Other functionality
 * 
 * 
 * 
 * 
 */

/**
 * check Browser support for localStorage
 */
function browserSupportLocalStorage() {
    return typeof(Storage) !== "undefined" ? true : false;
}






/**
 * 
 * TESTS
 * 
 */

function openModal(){
    $('#exampleModal').modal('show');
}