var sendData;
var pressed = true;
var response = [];


//Translate button listener
$("#tranalslateBtn").click(
    function () {
        if (pressed) { //Translate button was pressed, show translation
            pressed = false;

            $("#tranalslateBtn").html("Back"); //Replace button to ->  "Back"
            var btn = document.getElementById("tranalslateBtn"); //disable button
            btn.className += " disabled";

            //Show loader (spinner) while waiting for translation
            $('#spinner-text').html("Please wait while we translating the code for you...");
            $(".darken").removeClass("hide").show();

            sendData = $('#input_text').val();
            var dict = {"text": sendData, "language": languages_response[selected]};
            console.log("dict before sending");
            console.log(dict);
            var json = JSON.stringify(dict);
            $.ajax({
                url: '/gettranslation',
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
                    showTranslation(response);

                }
            });
        }
        else //back button was pressed, go back to "insert code" mode
        {
            $("#translation-card").empty(); //remove the card with translation
            clearCards(); //Clear cards list
            $('#code-text-area').show();
            $('#input-card').hide();
            pressed = true;
            $("#tranalslateBtn").html("Translate");
            $('#response-card').hide();
        }

    }
);

// This Function responsible for showing cards with translation
var showCards = function () {
    var word = $(this).html();
    console.log(word);
    var cards = document.getElementById("cards-container");

    var h = parseInt(response.length / 3) + 1; // Calculate the total height for all cards
    cards.setAttribute("style", " min-height:" + h * 300 + "px");
    for (var i = 0; i < response.length; i++) { // Run on all translated words got from server
        if (word == response[i].keyword) {  // If word equals to the word hovered now
            var translation = response[i].translation; // Get the translation got from server for the word
            var $found = $('#card' + i);
            if ($found.length) {
                if ($found.is(":hidden")) // If the card already exist and hidden, just show it
                    $found.show();
            }
            else { // The card doesn't exist, create it
                var card = createCard(word, translation, response[i].link, i);
                cards.appendChild(card);
                $('.response-card')
                    .draggable()
                    .resizable(
                    {
                        minHeight: 250,
                        minWidth: 204
                    }
                );
            }
        }
    }
};


// Add listener to all classes responded by the server, to show card when clicked
$(document).on("click", ".keyword, .literal, .function, .operator, .library ", showCards);

// Function responsible to show translation
function showTranslation(res) {
    // Hide code area and show the code in card
    $('#code-text-area').hide();
    $('#input-card').removeClass('hide')
        .show();
    var j;

    var text = res[0];
    //text = text.replace(/\n/g, "<br/>");
    text = text.replace(/(?:\r\n|\r|\n)/g, '<br/>');
    text = text.replace(/    /g, '<span class="tab"></span>');

    $('#translation-card').html(text);
    response = res[1];
    var btn = document.getElementById("tranalslateBtn");
    btn.className = "waves-effect waves-light btn right";
    $(".darken").hide(); // Stop spinner
}

function createCard(word, translatedText, link, i) {
    var card = document.createElement("div"); // <div class="card-panel response-card">
    card.className = "card response-card";
    card.setAttribute("id", "card" + i);
    var initH = $('#cards-container').offset().top;
    var initW = $('#cards-container').offset().left;
    var space = 10;
    var h = initH + parseInt(cardCounter / 3) * 300 + space * (parseInt(cardCounter / 3));
    var w = initW + (cardCounter % 3) * 300 + space * (cardCounter % 3);
    card.setAttribute("style", "left:" + w + "px; top:" + h + "px");
    var img = document.createElement("img"); // <img src="images/exit.png" class="exit">
    img.setAttribute("src", "images/exit.png");
    img.addEventListener("click", function () {
        $("#card" + i).hide();
    });

    img.className = "exit";
    var text_el = document.createElement("div"); //<div class="black-text" id="result-card"></div>
    text_el.setAttribute("class", "card-content result-card");
    text_el.innerHTML = "<h4>" + word + "</h4>" + translatedText;
    var action = document.createElement("div");
    action.className = "card-action";

    var l1 = document.createElement("a");
    var linkText = document.createTextNode("Go To Site");
    l1.setAttribute("target", '_blank');
    l1.href = link;
    l1.title = link;
    l1.appendChild(linkText);

    var l2 = document.createElement("a");
    var linkText2 = document.createTextNode("Wrong?");
    l2.title = "#!";
    l2.href = "/contribution-page?keyword=" + word + "&language=" + languages_response[selected];
    l2.appendChild(linkText2);

    action.appendChild(l1);
    action.appendChild(l2);
    card.appendChild(img);
    card.appendChild(text_el);
    card.appendChild(action);
    cardCounter++;
    return card;
}

//Login
function login() {
    if (!isValidForm("loginform"))
    {
        console.log("wrong");
        return;
    }
    $('#modal1').closeModal();

    var data = {};
    data["email"] = $("#email").val();
    data["password"] = btoa($("#password").val());
    var json = JSON.stringify(data);
     //Show loader (spinner) while waiting for translation
    $('#spinner-text').html("Please wait to login");
    $(".darken").removeClass("hide").show();
    $.ajax({
        //url: "http://code-translator.appspot.com/login",
        url: "/login",
        type: "POST",
        data: json,
        contentType: "json",
        dataType: "json",
        success: function (response, message, jq) {
            $(".darken").hide(); // Stop spinner
            TreatLoginResponse(response);
        },
        error: function (response, text, message) {
        }
    });
}


function isValidForm(id) {
    var valid = true;
    var message = "Please fill ";
    $("form#" + id + " :input").each(function () {
        var input = $(this); //get the object
        if (input.val() == "") {
            valid = false;
            message+= input.attr("name")+" field";
            return false;
        }
        if (input.hasClass("invalid")) {
            valid = false;
            return false;
        }
    });
        $('#err-message').html(message);
    return valid;
}

//Register
function register() {
    var email = $("#email2");
    var firstname = $("#firstname").val();
    var lastname = $("#lastname").val();
    var passwd = $("#password2").val();

    if (!isValidForm("regform"))
    {
        console.log("wrong");
        return;
    }
    $('#modal2').closeModal();

    var data = {};
    data["firstname"] = firstname;
    userName = $("#nickname").val();
    data["nickname"] = userName;
    data["lastname"] = lastname;
    data["email"] = email.val();
    data["password"] = btoa(passwd);
    var json = JSON.stringify(data);

    $('#spinner-text').html("Please wait to register");
     //Show loader (spinner) while waiting for translation
    $(".darken").removeClass("hide").show();
    $.ajax({
        //url:"https://code-translator.appspot.com/register",
        url: "/register",
        type: "POST",
        data: json,
        contentType: "json",
        dataType: "json",
        success: function (response, message, jq) {
            $(".darken").hide(); // Stop spinner
            TreatRegisterResponse(response);
        },
        error: function (response, text, message) {
        }
    });
}

function TreatRegisterResponse(response) {
    var rc = response.rc;
    var message = response.message;
    console.log(message);
    if (rc == 0) {
        localStorage.setItem("userName", userName);
        showLogout();
    }
    else {
        $("#errormessage").html(message);
        $("#errormodal").openModal();
    }
}

var userName = "";


function TreatLoginResponse(response) {
    var rc = response.rc;
    var message = response.message;
    console.log(message);
    if (rc == 0) {
        userName = message;
        localStorage.setItem("userName", message);
        showLogout();
    }
    else {
        $("#errormessage").html(message);
        $("#errormodal").openModal();
    }
}
function showLogout() {
    $("#logoutbutton").show();
    $("#loginbutton").hide();
    $("#regbutton").hide();
    $('#logo-container').html(userName + ", Welcome to Code Translator!");
}

if (storageAvailable('localStorage')) {
    userName = localStorage.getItem("userName");
    if (userName) {
        showLogout();
    }
}
else {
    alert("No Local Storage");
}

function storageAvailable(type) {
    try {
        var storage = window[type],
            x = '__storage_test__';
        storage.setItem(x, x);
        storage.removeItem(x);
        return true;
    }
    catch (e) {
        return false;
    }
}

function logout() {
    userName = "";
    localStorage.removeItem("userName");
    Materialize.toast('Logged Out', 2000);
    $("#logoutbutton").hide();
    $("#loginbutton").show();
    $("#regbutton").show();
    $('#logo-container').html("Welcome to Code Translator!");
}

function contribute() {
    userName = localStorage.getItem("userName");
    if (userName) {
        document.location.href = "/contribution-page";
    }
    else {
        Materialize.toast('Please login', 2000);
    }
}