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

    // $(document).ready(function () {

    //     document.querySelectorAll('.add').forEach(button => {
    //         button.onclick = () => {
    //             const menuitemid = button.dataset.menuitemid;
    //             createOrder(menuitemid, csrftoken);
    //         }

    //     });
    // });

    //### Control total topping selection for specific order
    const toppingCount = document.querySelector('#toppingCount');
    const limit = Number(toppingCount.dataset.count);
    const updateURL = window.location.origin + '/update';
    $(`.this`).on('change', function() {
        if ($(`.this:checked`).length > limit) {
            this.checked = false;
            alert('Max toppings for order selected')
        }
        // if ($(`.this:checked`) && $(this).is(':checked')) {
        //     update(updateURL)
        // } else {
        //     console.log(this)
        // }
    });
    //### END Control total topping selection for specific order

    
});
// onchange i will fetch a post to either add or delete.
//

//#########


// function createOrder(menuitemid, csrftoken) {

//     const request = new XMLHttpRequest();
    
//     request.open('POST','/create/');

//     const data = new FormData();

//     var csrftoken = Cookies.get("csrftoken");
//     request.setRequestHeader("X-CSRFToken", csrftoken);

//     request.send(data);
// }
  

   
         
 







// function checkedTopping() {
//     const toppingCount = document.querySelector('#toppingCount');
//     const limit = Number(toppingCount.dataset.count);
//     document.querySelectorAll('.single-checkbox').forEach(check => {

//         if (check.checked == true > limit) {
//             console.log('jaaa')
//         }

//     })
//     //const limit = document.querySelector('#toppingCount').value;

// }