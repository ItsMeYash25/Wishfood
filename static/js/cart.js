var updatebtn = document.getElementsByClassName('update-cart')

for (var i = 0; i < updatebtn.length; i++) {
    updatebtn[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productid:',productId, 'Action:',action)

        console.log('User:',user)

        if (user == "AnonymousUser") {
            console.log('Not Logged in')
        } else {
            updateUserOrder(productId, action)
        }
    }) 
}

function updateUserOrder(productId, action) {
    console.log('Logged in')
    var url = 'update_item'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({
            'productId':productId , 'action':action
        })
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}
