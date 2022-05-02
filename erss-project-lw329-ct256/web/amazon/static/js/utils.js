function urlEncodedDataPairs(json) {
    return Object.keys(json).map(function (key) {
        return encodeURIComponent(key) + '=' + encodeURIComponent(json[key]);
    }).join('&');
}
function getCookie(name) {
    if (!document.cookie) {
        return null;
    }

    const xsrfCookies = document.cookie.split(';')
        .map(c => c.trim())
        .filter(c => c.startsWith(name + '='));

    if (xsrfCookies.length === 0) {
        return null;
    }
    return decodeURIComponent(xsrfCookies[0].split('=')[1]);
}
function addToChart(id) {
    csrftoken = getCookie('csrftoken');
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/addToChart", true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            alert("Added to cart successfully");
        } else if(this.readyState == 4) {
            alert("Failed to add to cart: " + this.status);
        } else if(this.readyState == 2) {
            alert("Send Cart Adding request")
        }
    };
    xhttp.send(urlEncodedDataPairs({
        'product_id': id
    }));
}

function purchase() {
    csrftoken = getCookie('csrftoken');
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/purchase", true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            alert("Purchase successful");
        } else if(this.readyState == 4 && this.status == 400) {
            alert("Failed to purchase");
        } else if(this.readyState == 2)
            alert("Send Purchase Request");
        }
    xhttp.send();
}

function cancelOrder(id) {
    console.log(id)
    csrftoken = getCookie('csrftoken');
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/cancelOrder", true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            alert("Cancelled order successfully");
        } else if(this.readyState == 4 && this.status == 400) {
            alert("Failed to cancel order");
        } else if(this.readyState == 2)
            alert("Send Cancel Request");
        }
    xhttp.send(urlEncodedDataPairs({'order_id': id}));
}

function subscribe() {
    csrftoken = getCookie('csrftoken');
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/subscribe", true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            alert("Subscribed successfully");
        } else if(this.readyState == 4 && this.status == 400) {
            alert("Failed to subscribe");
        } else if(this.readyState == 2)
            alert("Send Subscribe Request");
    }
    let email = document.getElementById('email').value;
    console.log(email)
    xhttp.send(urlEncodedDataPairs({'email': email}));
}