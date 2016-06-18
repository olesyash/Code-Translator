/**
 * Created by olesya on 30-Apr-16.
 */

// ---- Contribution treatment -----------

//Global variables
var keyword;
var selected_type;
var selected_option;
var url;
var name = "";
var GET = "Please insert contribution details: ";
var NO_THANKS = "Thank you, but the keyword already translated";
var options_list = ["class", "id"];

$(document).ready(function () {
    $('select').material_select();
});

console.log("start");

document.getElementById("select-option").addEventListener("change", select_listener, false);

//Select option listener
function select_listener() {
    console.log("select pressed");
    var e2 = document.getElementById("select-option");
    selected_option = e2.options[e2.selectedIndex ].value;

    if (options_list.indexOf(selected_option) != -1) {
        $("#name").removeClass("hide").show();
    }
    else {
        name = "";
        $("#name").addClass('hide');
    }
}

//Check keyword button listener
$("#keywordBtn").click(
    function () {
        console.log("button pressed");
        check_keyword();
    }
);

//Submit button listener
$("#submit").click(
    function () {
        console.log("submit pressed");
        submit_contribution();
    }
);

//Yes button listener
$("#yes").click(
    function () {
        $("#temp-translation-card").hide();
        hideAll();
        send_contribution(selected_type, url, selected_option, name, "True");
    }
);

//No button listener
$("#no").click(
    function () {
        init();
        $("#temp-translation-card").hide();
        hideAll();
        showGetTranslation();
    }
);

//Agree button listener
$("#agree").click(
    function () {
        approve();
    }
);

//Disagree button listener
$("#disagree").click(
    function () {
        $("#translation-card").addClass("hide");
        $("#header").html(GET);
        showGetTranslation();
    }
);

//Init
function init() {
    console.log("in init");
    selected_type = "";
    selected_option = "";
    url = "";
    name = "";

    $('#select-keyword-type').val("").material_select();
    $("#select-option").val("").material_select();

    $('#url-insert').val("");
    $('#name-insert').val("");
    $("#header").html(GET).removeClass("red-text text-accent-4");
}

//Submit contribution getting all info from user and sending to server using send_contribution function
function submit_contribution() {
    //Keyword type
    var e = document.getElementById("select-keyword-type");
    selected_type = e.options[e.selectedIndex].value;
    console.log(selected_type);
    if (selected_type == "") {
        alert("Please choose keyword type");
        return;
    }


    //Option
    var e2 = document.getElementById("select-option");
    //Because of the disabled option there is shift of one (+1)
    selected_option = e2.options[e2.selectedIndex].value;
    console.log("selected option " + selected_option);
    if (selected_option == "") {
        alert("Please choose an option");
        return;
    }


    //Url
    url = $('#url-insert').val();
    if (url == "") {
        alert("Please insert url");
        return;
    }
    console.log(url);

    //id/class Name
    name = $('#name-insert').val();
    console.log("name" + name);
    if (!($('#name').hasClass('hide')) && name == "") {
        alert("Please insert name");
        return;
    }

    send_contribution(selected_type, url, selected_option, name, "False");
}

//Send contribution details to server, and get response
function send_contribution(selected_type, url, selected_option, name, save) {
    var dict = {
        "keyword": keyword, "language": languages_response[selected], "word_type": selected_type,
        "url": url, "option": selected_option, "save": save, "name": name
    };
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
                $(".loader2").hide(); //stop spinner
                alert("Sorry, there is some error in the server side =(")
            }
        },
        success: function (response, message, jq) {
            console.log(response);
            $(".loader2").hide(); //stop spinner
            if (save == "False") {
                treatTranslation(response);
            }
            else {
                showThankYou(response);
            }
        }
    });
}

//Show translation to user and make sure this is what he meant
function treatTranslation(response) {
    var text = response.response;
    if (response.rc == 0) {
        hideAll();
        $("#header").html("Is it your suggested translation?").removeClass("hide").removeClass("red-text text-accent-4").show();
        $("#temp-translation-card").removeClass("hide").show();
        console.log(text);
        $("#content-of-card").html(text);
    }
    else
    {
        $("#header").html(text).removeClass("hide").addClass("red-text text-accent-4").show();
    }
}

//Show thank you message to user
function showThankYou(response) {
    var text = response.response;
    $("#header").html(text).removeClass("hide").show();
}

//Send request to server to check if keyword already exist/approved
function check_keyword() {
    keyword = $('#keyword').val();
    if (keyword == "") {
        alert("Please insert keyword");
        return
    }
    var dict = {"keyword": keyword, "language": languages_response[selected]};
    var json = JSON.stringify(dict);

    //Show loader (spinner) while waiting for server response
    $(".loader2").removeClass("hide").show();
    $.ajax({
        url: '/check-keyword',
        type: "POST",
        data: json,
        contentType: "json",
        dataType: "json",
        statusCode: {
            400: function () {
            },
            500: function () {
                $(".loader2").hide(); //stop spinner
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

//This function treat the response of keyword check
function TreatResponse(response) {
    console.log(response);
    var text = response.response;
    if (text == GET) {
        showGetTranslation();
    }
    else if (text == NO_THANKS) {
        $("#header").html(NO_THANKS).removeClass("hide").show();
    }
    else {
        $("#header").html("This is the current translation. Do you approve?").removeClass("hide").show();
        $("#translation-card").removeClass("hide").show();
        console.log(text);
        $("#content").html(text);
    }
}

function approve()
{
     var dict = {"keyword": keyword, "language": languages_response[selected]};
    var json = JSON.stringify(dict);

    //Show loader (spinner) while waiting for server response
    $(".loader2").removeClass("hide").show();
    $.ajax({
        url: '/approve',
        type: "POST",
        data: json,
        contentType: "json",
        dataType: "json",
        statusCode: {
            400: function () {
            },
            500: function () {
                $(".loader2").hide(); //stop spinner
                alert("Sorry, there is some error in the server side =(")
            }
        },
        success: function (response, message, jq) {
            console.log(response);
            $(".loader2").hide(); //stop spinner
            $("#translation-card").addClass("hide");
            showThankYou(response);
        }
    });
}

//Show all elements needed to get contribution information from user
function showGetTranslation() {
    $("#header").html(GET).removeClass("hide").show();
    $("#keyword-type").removeClass("hide").show();
    $("#url").removeClass("hide").show();
    $("#option-choose").removeClass("hide").show();
    $("#submit").removeClass("hide").show();
}

//Hide all elements needed to get contribution information from user
function hideAll() {
    $("#header").hide();
    $("#keyword-type").hide();
    $("#url").hide();
    $("#option-choose").hide();
    $("#submit").hide();
    $("#name").addClass('hide');
}


function changePage(i) {
    selected = i;
    hideAll();
    addPagination();
}