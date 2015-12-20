(function ($){
  $(function(){

    $('.button-collapse').sideNav();
    $('.parallax').parallax();



  }); // end of document ready
})(jQuery); // end of jQuery name space

var sendData;
var pressed = true;

/////////////debugging
//            $('#response-card').removeClass('hide').show()
//            .draggable()
//            .resizable();
//            $('#result-card').html("sssssssssssssssssssss" +
//                "sssss sss ssss ssssss ssss s s s s  s sss s s s s s s s s s s s s s s  sssssssssssss" +
//                "ssssssssss s s      sssss ssssssssssss s s s s ssssssssss ssssss sssss ssss ssss ss  ssss ss sss" +
//                "ssssssssss s s      sssss ssssssssssss s s s s ssssssssss ssssss sssss ssss ssss ss  ssss ss sss" +
//                "ssssssssss s s      sssss ssssssssssss s s s s ssssssssss ssssss sssss ssss ssss ss  ssss ss sss"
//            );

/////////////////////////////////////////


$('.exit').click(function(){
     $('#response-card').hide();
});


$("#tranalslateBtn").click(

function ()
{
    if(pressed) { //Translate button was pressed, show translation
        sendData = $('#input_text').val();
        $.ajax({
            url: '/gettranslation',
            type: "POST",
            data: sendData,
            contentType: 'text/html; charset=utf-8',
            dataType: "json ",
            statusCode: {
                400: function () {
                }
            },
            success: function (response, message, jq) {
                show_translation(response);

            }
        });
    }
    else //back button was pressed, go back to translation
    {
        $('.input-field').show();
        $('#input-card').hide();
        pressed = true;
         $("#tranalslateBtn").html("Translate");
        $('#response-card').hide();
    }

}
);

function show_translation(response)
{
    $('.input-field').hide();
    $('#input-card').removeClass('hide')
    .show();

    for(var i = 0; i< response.length; i++)
    {
       console.log(response[i].link);
    }
    $('#translation-card').html(sendData.toString())
    .lettering('words')
    .mouseover(function (event) {
        var word = event.target.innerHTML;

    for(var i = 0; i< response.length; i++)
    {
        if(word == response[i].keyword) {
            translation = response[i].translation;
            $('#response-card').removeClass('hide').show()
            .draggable()
            .resizable();
            $('#result-card').html(translation.toString());


        }
    }

    });

    $("#tranalslateBtn").html("Back");
    pressed = false;
}
