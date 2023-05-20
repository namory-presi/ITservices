var updateBtns = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('action:', action,'article:', productId)
        console.log('Client', user)

        if (user === "AnonymousUser") {
            console.log("Vous n'etes pas connecté")
        } else {
            console.log("Envoi des données")
            updateUserOrder(productId, action)
        }

    })
    
}


function updateUserOrder(productId, action) {

    
    var url = '/cart/update/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body: JSON.stringify({"productId": productId, "action": action})
    })


    .then((response) =>{
        return response.json()
    })

    .then( (data) =>{
        // location.reload();
        // window.location.reload();
        console.log(data)
    })
    .then(response => console.log(JSON.stringify(response)))
}