function getCSRFToken() {
    return document.querySelector("#csrf_token").value;
}

async function postJSONData(url, data) {
    return await fetch(url, {
        "method": "POST",
        headers: {
            "content-type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify(data)
    })
}


function capitalizeFirstLetter(val) {
    return String(val).charAt(0).toUpperCase() + String(val).slice(1);
}


function showMessage(message) {
    const msg = document.querySelector('.message2');
    msg.classList.remove('show');
    msg.textContent = message;
    msg.classList.add('show');
}