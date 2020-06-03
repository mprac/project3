document.addEventListener('DOMContentLoaded', () => {

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

    // Add menu item to cart
    document.querySelectorAll('.add').forEach(button => {
        button.onclick = async () => {
            const request = new XMLHttpRequest();

            request.open("POST", "/add/")

            //server response
            request.onload = () => {
                const info = JSON.parse(request.responseText);
                // loadOrders(info);
                // console.log(info.menuitem, info.hasTopping);
                console.log(info);
            }

            var csrftoken = getCookie('csrftoken');
            request.setRequestHeader("X-CSRFToken", csrftoken);

            const itemid = Number(button.dataset.item);
            const count = Number(document.querySelector(`.c${itemid}`).value);
            const data = new FormData();
            data.append('itemid', itemid);
            data.append('count', count);
            request.send(data);

        }


    });

    //End DOMContentLoaded
});
//End DOMContentLoaded

//Edit address

//end edit address

function loadOrders(info) {
    jQuery('#orders').html("");
    document.querySelector('#orders').innerHTML = `<h1>${info.menuitem}</h1>`
}