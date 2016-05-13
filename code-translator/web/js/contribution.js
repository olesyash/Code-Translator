/**
 * Created by olesya on 30-Apr-16.
 */

// ---- Contribution treatment -----------

var language = "Java";
console.log("start");
var GET = "Please insert contribution details: ";

//Translate button listener
$("#keywordBtn").click(
    function () {
        console.log("button pressed");
        check_keyword();
    }
);

function check_keyword() {
    var keyword = $('#keyword').val();
    if (keyword == "")
    {
        alert("Please insert keyword");
        return
    }
    var dict = {"keyword": keyword, "language": language};
    var json = JSON.stringify(dict);

    //Show loader (spinner) while waiting for server response
    $(".loader2").removeClass("hide").show();
    $.ajax({
        url: '/contribute',
        type: "POST",
        data: json,
        contentType: "json",
        dataType: "json",
        statusCode: {
            400: function () {
            },
            500: function () {
                $(".darken").hide(); // Stop spinner
                alert("Sorry, there is some error in the server side =(")
            }
        },
        success: function (response, message, jq) {
            console.log(response);
            $(".loader2").hide(); //stop spinner
            TreatResponse(response)
        }
    });
}


function TreatResponse(response){
    console.log(response);
     var text = response.response;
    if (text == GET) {
        getTranslation();
    }
    else {
        $("#translation-card").removeClass("hide").show();
        console.log(text);
        $("#content").html(text);
    }
}

function getTranslation()
{

}