/**
 * Created by olesya on 12-Jun-16.
 */

//Get jquery functions ready
$(document).ready(function () {
    $('.button-collapse').sideNav();
    $('.parallax').parallax();
    $('.modal-trigger').leanModal();
    $('select').material_select();
});

//Define variables
var name = "";
var selected_option;
var options_list = ["class", "id"];
var counter = 1;
var THANKS_FOR_CONTRIBUTION = "Thank you for your contribution!";

// Add on click listener to all select-options
for(var i=1;i<4;i++) {
    $(document).on("change", "#select-option"+i, select_listener);
}
// Add on click listeners
$(document).on("click", "#add-other", addOther);
$(document).on("click", "#remove-other", removeOther);
$(document).on("click", "#addLanguageBtn",add_language);
$(document).on("click", ".mi", showInfo);

// Check if language in url present, if not redirect to /add-language page
if (document.location.href.indexOf("language=") != -1) {
    var language = document.location.href.split("language=")[1];
}
else {
    alert("Missing language parameter");
    document.location.href = "/add-language"
}

// This function shows information on information icon press
function showInfo() {
    $('#modal-header').html("How to add language: 'urls' fields");
    $('#modal-text').html("Please insert here the default urls the translation will be pulled from. <br>" +
    "Additionally, you need to add the best way to parse the html data from that url. " +
    "Use developer options on your browser to find the best way. " +
    "You can parse it by specific tag: id name or class name <br>" +
    "If there is no specific tag to parse from, you can use whole page with the tags or as plain text." +
    "<br> You can add maximum three urls and must add at least one");
    $('#modal1').openModal();
}

// This function preparing the data to be sent to server when "next" button pressed
function add_language(){
    var data = {};
    //finally structure {"urls" : [list of urls], url1 : {"name": name, "type": type}, url2 : {"name": name, "type": type} ...}
    var urls = [];
    var selected = [];
    // get all information from all urls inputs
    for(var i=1;i<4;i++)
    {
        var url = {};
        var j = $('#'+i);
        if(j.hasClass('hide')) // if the element is hidden, do not add the information
            break;
        var u = $('#'+ "input-url"+i); // take the url
        urls[i-1] = u.val();
        console.log(urls[i-1]);
        var c = document.getElementById("select-option"+i);
        selected[i-1] = c.options[c.selectedIndex ].value; // take the type of html parsing
        console.log(selected[i - 1]);
        if(options_list.indexOf(selected[i-1]) != -1) { // take the name if exist
            var name_obj = $("#name-insert" + i);
            name = name_obj.val();
        }
        else { // if name not needed, leave empty
            name = ""
        }
        // save all data in dictionary data
        url["type"] = selected[i-1];
        url["name"] = name;
        data[urls[i-1]] = url;

    }
    // Demand at least one url filled
    if (urls[0] == ""){
        alert("You must enter at least one url");
        return;
    }
    data["urls"] = urls;
    console.log(data);
    var all_data= {"all_data": data, "language": language};
    sendToServer(all_data); //send to server the data
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

    var json = JSON.stringify(data); // convert dictionary to json
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

// Treat response from server, if succeed show thank you message , if not - alert on error
function TreatResponse(response) {
    console.log(response["response"]);
    $('#info-form').addClass('hide');
    if (response["response"])
    {
        $('#header').html(THANKS_FOR_CONTRIBUTION);
        $('#greetings').hide();
        console.log("removing hide");
        $('#go-back').removeClass('hide');
    }
    else {
         $('#header').removeClass('hide').html("Something went wrong");
    }
}