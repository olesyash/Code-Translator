/**
 * Created by olesya on 12-Jun-16.
 */

$(document).ready(function () {
    $('.button-collapse').sideNav();
    $('.parallax').parallax();
    $('.modal-trigger').leanModal();
    $('select').material_select();
});
var name = "";
var selected_option;
var options_list = ["class", "id"];
var counter = 1;
var THANKS_FOR_CONTRIBUTION = "Thank you for your contribution!";

for(var i=1;i<4;i++) {
    $(document).on("change", "#select-option"+i, select_listener);
}
$(document).on("click", "#add-other", addOther);
$(document).on("click", "#remove-other", removeOther);
$(document).on("click", "#addLanguageBtn",add_language);
$(document).on("click", ".mi", showInfo);


if (document.location.href.indexOf("language=") != -1) {
    var language = document.location.href.split("language=")[1];
}
else {
    alert("Missing language parameter");
    document.location.href = "/add-language"
}

function showInfo() {
    $('#modal-header').html("header info about urls");
    $('#modal-text').html("info about urls");
    $('#modal1').openModal();
}

function add_language(){
    var data = {};
    var urls = [];
    var selected = [];
    for(var i=1;i<4;i++)
    {
        var url = {};
        var j = $('#'+i);
        if(j.hasClass('hide'))
            break;
        var u = $('#'+ "input-url"+i);
        urls[i-1] = u.val();
        console.log(urls[i-1]);
        var c = document.getElementById("select-option"+i);
        selected[i-1] = c.options[c.selectedIndex ].value;
        console.log(selected[i - 1]);
        if(options_list.indexOf(selected[i-1]) != -1) {
            var name_obj = $("#name-insert" + i);
            name = name_obj.val();
        }
        else {
            name = ""
        }
        url["type"] = selected[i-1];
        url["name"] = name;
        data[urls[i-1]] = url;

    }
    data["urls"] = urls;
    console.log(data);
    var all_data= {"all_data": data, "language": language};
    sendToServer(all_data);
}


//Select option listener
function select_listener(e) {
    var id = e.target.id;
    console.log("select pressed " + id);
    var hidden;
    var e2 = document.getElementById(id);
    selected_option = e2.options[e2.selectedIndex ].value;


    var j = id.split('select-option')[1];
    if (options_list.indexOf(selected_option) != -1) {
        console.log("in if");
        hidden = "name" + j;
        console.log(hidden);
        var name_obj = $("#"+hidden);
        name_obj.removeClass("hide").show();
    }
    else {
        name = "";
        hidden = "name" + j;
        $("#" + hidden).addClass('hide');
    }

}

function addOther(){
    if (counter <3)
        counter++;
    $("#" + counter).removeClass('hide');

}

function removeOther(){
    console.log("in remove");
    $("#" + counter).addClass('hide');
    if(counter > 1)
        counter--;
}

//Send data to server to add language urls to DB
function sendToServer(data) {

    var json = JSON.stringify(data);
    //Show loader (spinner) while waiting for server response
    $(".darken").removeClass("hide").show();
    $.ajax({
        url: '/add-language-urls',
        type: "POST",
        data: json,
        contentType: "json",
        dataType: "json",
        statusCode: {
            404: function () {
               $(".darken").hide(); //stop spinner
            },
            400: function () {
                $(".darken").hide(); //stop spinner
            },
            500: function () {
                $(".darken").hide(); //stop spinner
                alert("Sorry, there is some error in the server side =(")
            }
        },
        success: function (response, message, jq) {
            console.log(response);
            $(".darken").hide(); //stop spinner
            TreatResponse(response)
        }
    });
}

function TreatResponse(response) {
    console.log(response["response"]);
    $('#info-form').addClass('hide');
    if (response["response"])
    {
        $('#header').html(THANKS_FOR_CONTRIBUTION);
        $('#greetings').hide();
    }
    else {
         $('#header').removeClass('hide').html("Something went wrong");
    }
}