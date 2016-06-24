/**
 * Created by olesya on 12-Jun-16.
 */


$(document).ready(function () {
    $('.button-collapse').sideNav();
    $('.parallax').parallax();
    $('.modal-trigger').leanModal();
    $('select').material_select();
});

if (document.location.href.indexOf("language=") != -1) {
    var language = document.location.href.split("language=")[1];
}
else {
    alert("Missing language parameter");
    document.location.href = "/add-language"
}

$(document).on("click", "#add-other", addOther);
$(document).on("click", ".mi", showInfo);
$(document).on("click", "#nextBtn", prepareSubmission);

var header = {
    "statements-info": "How to add language: 'statements' field",
    "data_types-info": "How to add language: 'data types' field",
    "expressions-info": "How to add language: 'expressions' field",
    "operators-info": "How to add language: 'operators' field",
    "add-other-info": "How to add language: 'other' field"
};

var information = {
    "statements-info": "Please insert here list of keywords describing statements, devided by comma <br> " +
    "Example: for, if, return  <br>For more information about statments, press  <a target='_blank' href=https://en.wikipedia.org/wiki/Statement_(computer_science)>here</a>",
    "data_types-info": "Please insert here list of keywords describing data types, devided by comma <br> " +
    "Example: int, char, float, double  <br>For more information about data types, press  <a target='_blank' href=https://en.wikipedia.org/wiki/Data_type>here</a>",
    "expressions-info": "Please insert here list of keywords describing expressions, devided by comma <br> " +
    "Example: Python: print, yield, lambda  <br>For more information about expressions, press  <a target='_blank' href=https://en.wikipedia.org/wiki/Expression_(computer_science)>here</a>",
    "operators-info": "Please insert here list of keywords describing operators, devided by comma <br> " +
    "Example: not, or, and <br>For more information about operators, press  <a target='_blank' href=https://en.wikipedia.org/wiki/Operator_(computer_programming)>here</a>",
    "add-other-info": "Here you can define new group name, and add keywords to this group. <br>"

};

var expected = ["input-statements", "input-operators", "input-expressions", "input-data_types"];

var others_counter = 0;

function showInfo(event) {
    console.log(event.target.id);
    $('#modal-header').html(header[event.target.id]);
    $('#modal-text').html(information[event.target.id]);
    $('#modal1').openModal();
}


function addOther() {
    //<div class="row myrow">
    //             <div class="input-field col s4 push-s2">
    //                 <input id="other-name" type="text" class="validate">
    //                 <label for="other-name">Other Name</label>
    //             </div>
    //             <div class="input-field col s4 push-s2">
    //                 <input id="last_name" type="text" class="validate">
    //                 <label for="last_name">Other keywords</label>
    //             </div>
    //         </div>
    console.log("in add other");
    var span = document.getElementById("other-container");
    var row = document.createElement("div");
    row.className = "row myrow";
    var col1 = document.createElement("div");
    col1.className = "input-field col s4 push-s2";


    var input = document.createElement("input");
    input.setAttribute("id", "name" + others_counter);
    input.setAttribute("type", "text");
    var label = document.createElement("label");
    label.setAttribute("for", "name" + others_counter);
    label.innerHTML = "Group name:";

    col1.appendChild(input);
    col1.appendChild(label);

    var col2 = document.createElement("div");
    col2.className = "input-field col s4 push-s2";
    var input2 = document.createElement("input");
    input2.setAttribute("id", "list" + others_counter);
    input2.setAttribute("type", "text");
    var label2 = document.createElement("label");
    label2.setAttribute("for", "list" + others_counter);
    label2.innerHTML = "Group elements:";

    col2.appendChild(input2);
    col2.appendChild(label2);

    row.appendChild(col1);
    row.appendChild(col2);
    span.appendChild(row);
    others_counter++;

}

function prepareSubmission() {
    var send_data = {};
    send_data["language"] = language;
    var all_data = {};
    var other = {};
    var counter = 0;
    var list_of_el;
    var name;
    $("form#info-form :input").each(function () {
        var input = $(this); //get the object
        list_of_el = input.val().split(",");
        if (input.attr('id').indexOf("list") > -1) {
            console.log("in list if  " + input.attr('id'));
            list_of_el = input.val().split(",");
            list_of_el = list_of_el.map(Function.prototype.call, String.prototype.trim);
            counter++;
        }
        else if (input.attr('id').indexOf("name") > -1) {
            console.log("in name if  " + input.attr('id'));
            name = input.val();
            counter++;
        }
        if (counter % 2 == 0 && counter != 0) {
            other[name] = list_of_el
        }
        else {
            list_of_el = list_of_el.map(Function.prototype.call, String.prototype.trim);
            all_data[input.attr('id').split('-')[1]] = list_of_el;
        }
    });
    all_data['other'] = other;
    console.log(all_data);
    send_data["all_data"] = all_data;
    add_language(send_data);
}

//Send data to server to add language classification to DB
function add_language(data) {

    var json = JSON.stringify(data);
    //Show loader (spinner) while waiting for server response
    $(".darken").removeClass("hide").show();
    $.ajax({
        url: '/add-language-classification',
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
    if (response["response"])
        document.location.href = "/add-language-urls?language=" + language;
    else {
        alert("Something went wrong")
    }
}