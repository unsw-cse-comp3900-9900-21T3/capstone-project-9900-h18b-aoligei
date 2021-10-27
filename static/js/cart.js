console.log("Let's go cart");

if (localStorage.getItem('cart') == null) {
    var cart = {};
} else {
    cart = JSON.parse(localStorage.getItem('cart'));
}

$(document).on("click", ".atc", function () {
    console.log("Adding to cart button is clicked;");
    var item_id = this.id.toString();
    console.log(item_id);

    if (cart[item_id] != undefined) {
        cart[item_id] = cart[item_id] + 1;
    } else {
        cart[item_id] = 1;
    }
    console.log(cart);
    localStorage.setItem('cart', JSON.stringify(cart));

    document.getElementById("cart").innerHTML = "Cart(" + Object.keys(cart).length + ")";

    // console.log(Object.keys(cart).length);

});
//display cart function


// var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
// document.getElementById('cart_function').setAttribute('data-bs-content', cartString)
// var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
//     return new bootstrap.Popover(popoverTriggerEl);
// });
// $(function () {
//     $('[data-toggle="popover"]').popover();
//     document.getElementById("cart").setAttribute('data-content', "<h2>this is your cart</h2>h2>");
// });

displayCart(cart);

function displayCart(cart) {
    var cartString = "";
    cartString += "<h5>This is your cart</h5>";

    var cartIndex = 1;

    for (var x in cart) {
        cartString += cartIndex;
        cartString += document.getElementById("nm" + x).innerHTML + " | " + "Qty:" + cart[x] + "</br>";
        cartIndex += 1;
    }
    // document.getElementById("cart").setAttribute("data-content", cartString);

    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    document.getElementById("cart").setAttribute("data-bs-content", cartString);

    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });


}



