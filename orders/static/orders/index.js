//var declarations are globally scoped or function scoped. 
//var variables can be updated and re-declared within its scope.
//let and const are block scoped. 
//let variables can be updated but not re-declared.
//const variables can neither be updated nor re-declared.

// XMLHttpRequest is just an object in javascript that will allow you to make an ajax request, thats going to allow me to make an HTTP request to some other web server in order to get some information 
// //connect to websocket 
// var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);



document.addEventListener('DOMContentLoaded', () => {

    // DJANGO CSRF FOR AJAX REQUESTS
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // END DJANGO CSRF FOR AJAX REQUESTS




    document.querySelectorAll('.add').forEach(button => {
        button.onclick = () => {
            const request = new XMLHttpRequest()
           
            request.onreadystatechange = function () {
                if (request.readyState === 4) {
                    if (request.status === 200) {
                        const response = JSON.parse(request.responseText);
                        document.querySelector('#ordersToPlace').innerHTML += response['result'];
                    } else if (request.status === 404) {
                        //file not found
                    }
            }
              
        };

    // request.onload = () => {
    //     const response = JSON.parse(request.responseText); 
    //     document.querySelector('#ordersToPlace').innerHTML = response['result'];


    // };
    request.open('POST', '/createOrder')
    request.send();
};
    })
    
    // JS promise
    const order = false;
    const orderReady = new Promise((resolve, reject) => {
        setTimeout(() => {
            if (order) {
                resolve('Order is complete');
            }   else {
                reject(Error('Order cannot be complete at this time'));
            }
           
        }, 5000)
        
    })
    console.log(orderReady);
    orderReady.then(val => console.log(val)).catch(err => console.log(err));

    function addFive(n) {
        return n + 5;
    };
    function double(n) {
        return n * 2;
    };

    function finalValue(nextValue) {
        console.log(`The final value is ${nextValue}`)
    }

    const mathPromise = new Promise( (resolve, reject) => {
        setTimeout(() => {
            if (typeof value === 'number') {
                resolve(value);
            } else {
                reject(Error('you must specify a number'));
            }
        }, 1000);
    });

    const value = 5;
    mathPromise.then(addFive).then(double).then(finalValue).catch(err => console.log(err) );


});


function clicked(e) {
    var cart = document.querySelector('#ordersToPlace');
    localStorage.setItem('data', e)
    data = localStorage.getItem('data')
    cart.append(data);
};



//     const ordersSocket = new WebSocket('ws://' + window.location.host + window.location.pathname);

//     ordersSocket.onmessage = function(e) {
//         const data = JSON.parse(e.data);
//         document.getElementById('orders').value += (data.order + '\n')
//     };

//    ordersSocket.onclose = function(e) {
//         console.error('Chat socket closed unexpectedly');
//     };

//     document.querySelectorAll('.add').forEach(button => {
//         button.onclick = () => {
//             var data = button.dataset.item;
//             ordersSocket.send(JSON.stringify({
//                 'order': data
//             }))
//         };
//     })