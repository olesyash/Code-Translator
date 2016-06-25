// Define variables
var sendData;
var pressed = true;
var response = [];
var userName = "";

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

    // Get response from server with code text with colored translated words, and show in card
    var text = res[0];
    text = text.replace(/^ /mg, '&nbsp'); // Replace all spaces in the beginning of line with html spaces
    text = text.replace(/(?:\r\n|\r|\n)/g, '<br/>'); // replace all "enter = \n" => <br>
    text = text.replace(/    /g, '<span class="tab"></span>'); // Replace all "4 spaces" -> <class=tab>
    text = text.replace(/\t/g, '<span class="tab"></span>'); // Replace all tabs "\t" -> <class=tab>

    $('#translation-card').html(text);
    response = res[1];
    // Remove disabled on "back" button
    var btn = document.getElementById("tranalslateBtn");
    btn.className = "waves-effect waves-light btn right";
    $(".darken").hide(); // Stop spinner
}

// Function create one card
function createCard(word, translatedText, link, i) {
    var card = document.createElement("div"); // <div class="card-panel response-card">
    card.className = "card response-card";
    card.setAttribute("id", "card" + i);
    var initH = $('#cards-container').offset().top;
    var initW = $('#cards-container').offset().left;
    var space = 10;
    var h = initH + parseInt(cardCounter / 3) * 300 + space * (parseInt(cardCounter / 3)); // calculate the height for card
    var w = initW + (cardCounter % 3) * 300 + space * (cardCounter % 3); // calculate width for card
    card.setAttribute("style", "left:" + w + "px; top:" + h + "px"); // set height and width for the card
    var img = document.createElement("img"); // <img src="images/exit.png" class="exit">
    img.setAttribute("src", "images/exit.png"); // Add image "x" to close card
    img.addEventListener("click", function () { // Add listener to "x" image, hide the card when pressed
        $("#card" + i).hide();
    });

    img.className = "exit";
    var text_el = document.createElement("div"); //<div class="black-text" id="result-card"></div>
    text_el.setAttribute("class", "card-content result-card");
    text_el.innerHTML = "<h4>" + word + "</h4>" + translatedText; // Add translation as text of the card
    var action = document.createElement("div");
    action.className = "card-action";

    // Add link "go to site" that redirect to the site
    var l1 = document.createElement("a");
    var linkText = document.createTextNode("Go To Site");
    l1.setAttribute("target", '_blank');
    l1.href = link;
    l1.title = link;
    l1.appendChild(linkText);

    // Add link to "Wrong" that redirect to contribution page
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
    // Check if details are valid
    if (!isValidForm("loginform")) {
        console.log("wrong");
        return;
    }
    $('#modal1').closeModal(); //close model

    var data = {};
    data["email"] = $("#email").val();
    data["password"] = btoa($("#password").val());
    var json = JSON.stringify(data);

    //Show loader (spinner) while waiting for login
    $('#spinner-text').html("Please wait until login is finished");
    $(".darken").removeClass("hide").show();
    $.ajax({
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
            $(".darken").hide(); // Stop spinner
            alert("Sorry, there is some error in the server side =(");
        }
    });
}

// This function check if form is valid, by checking all elements in form
function isValidForm(id) {
    var valid = true;
    var message = "Please fill ";
    $("form#" + id + " :input").each(function () {
        var input = $(this); //get the object
        if (input.val() == "") {
            valid = false;
            message += input.attr("name") + " field";
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
    if (!isValidForm("regform")) {
        console.log("wrong");
        return;
    }
    $('#modal2').closeModal();

    var data = {};
    data["firstname"] = $("#firstname").val();
    userName = $("#nickname").val();
    data["nickname"] = userName;
    data["lastname"] = $("#lastname").val();
    data["email"] = $("#email2").val();
    data["password"] = btoa($("#password2").val());
    var json = JSON.stringify(data);

    $('#spinner-text').html("Please wait until registration is finished");
    //Show loader (spinner) while waiting for registration
    $(".darken").removeClass("hide").show();
    $.ajax({
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
            $(".darken").hide(); // Stop spinner
            alert("Sorry, there is some error in the server side =(");
        }
    });
}

// Function responsible to get registration response and treat it
function TreatRegisterResponse(response) {
    var rc = response.rc;
    var message = response.message;
    console.log(message);
    if (rc == 0) { // Registration succeed
        localStorage.setItem("userName", userName);
        showLogout();
    }
    else { // Registration failed
        $("#errormessage").html(message);
        $("#errormodal").openModal();
    }
}

// Function responsible to get login response and treat it
function TreatLoginResponse(response) {
    var rc = response.rc;
    var message = response.message;
    console.log(message);
    if (rc == 0) { // Login succeed
        userName = message;
        localStorage.setItem("userName", message);
        showLogout();
    }
    else { // Login failed
        $("#errormessage").html(message);
        $("#errormodal").openModal();
    }
}

// Show logout icon, hide login and registration icons
function showLogout() {
    $("#logoutbutton").show();
    $("#loginbutton").hide();
    $("#regbutton").hide();
    $('#logo-container').text(userName + ", Welcome to Code Translator!");
}

// Check if local storage of the browser is available, if yes show username in greeting, else show alert warning
if (storageAvailable('localStorage')) {
    userName = localStorage.getItem("userName");
    if (userName) {
        showLogout();
    }
}
else {
    alert("No Local Storage");
}

// Check if local storage of the browser is available
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

// Logout: remove from local host user name, show login and registration icons, hide logout icon
function logout() {
    userName = "";
    localStorage.removeItem("userName");
    Materialize.toast('Logged Out', 2000);
    $("#logoutbutton").hide();
    $("#loginbutton").show();
    $("#regbutton").show();
    $('#logo-container').html("Welcome to Code Translator!");
}

// Function called when contribution ion pressed, if user logged in, enter contribution page, else ask for login
function contribute() {
    userName = localStorage.getItem("userName");
    if (userName) {
        document.location.href = "/contribution-page";
    }
    else {
        Materialize.toast('Please login', 2000);
    }
}