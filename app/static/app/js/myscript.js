$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items:5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

  

/*$('.plus-cart').click(function(){
    console.log("Plus Clicked")
    var id = $(this).attr("pid").toString();
   // console.log(id)
    $.ajax({
        type:'GET',
        url: "/pluscart",
        data:{
             prod_id : id
        },
        success: function(data)
        {
            console.log(data)
            console.log("Success")
        }
    });
})*/

// Wrap your jQuery code inside $(document).ready() to ensure it runs after the DOM is fully loaded
$(document).ready(function () {
    $('.plus-cart').click(function () {
        console.log("Plus Clicked");
        var id = $(this).attr("pid").toString();
        var eml = this.parentNode.children[2]

        // Make sure the 'id' variable contains the expected value
        console.log("Product ID: " + id);

        // Use $.ajax() to send a GET request to the server
        $.ajax({
             
            type: 'GET',
            url: "/pluscart",
            
            data: {
                prod_id: id
                
            },
           
            success: function (data) {
                // Handle the successful response from the server
                console.log("work")
                console.log(data);
                console.log("Success");
                eml.innerText = data.quantity
            },
            
            error: function (error) {
                // Handle any errors that occur during the AJAX request
                console.error("Error:", error);
            }
        });
    });
});
