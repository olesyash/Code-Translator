/**
 * Created by olesya on 11-Jun-16.
 */

$(document).ready(function () {
    $('.button-collapse').sideNav();
    $('.parallax').parallax();
    $('.modal-trigger').leanModal();
    $('select').material_select();
});

var header =
{
    "language-info": "How to add language: 'language' field",
    "keywords-info": "",
    "operations-info": "",
    "str_symbol1-info": "",
    "str_symbol2-info": "",
    "escape_character-info": "",
    "start_comment_symb-info": "",
    "comment_start1-info": "",
    "comment_end1-info": "",
    "comment_start2-info": "",
    "comment_end2-info": "",
    "add_library-info": "",
    "func_def-info": "",
    "func_start-info": "",
    "function_call_char-info": "",
    "class_keyword-info": ""
};

var empty_not_allowed = ['input-language', 'input-keywords', 'input-operations'];

var information =
{
    "language-info": "Please insert here the name of the language you want to add to Code Translator. " +
    "Please follow first letter upper case convention - for example: Java, Python, Ruby",
    "keywords-info": "",
    "operations-info": "",
    "str_symbol1-info": "",
    "str_symbol2-info": "",
    "escape_character-info": "",
    "start_comment_symb-info": "",
    "comment_start1-info": "",
    "comment_end1-info": "",
    "comment_start2-info": "",
    "comment_end2-info": "",
    "add_library-info": "",
    "func_def-info": "",
    "func_start-info": "",
    "function_call_char-info": "",
    "class_keyword-info": ""
};


var info_dict = {};

$(document).on("click", ".material-icons", showInfo);
$(document).on("click", "#nextBtn", prepareSubmission);

function showInfo(event) {
    console.log(event.target.id);
    $('#modal-header').html(header[event.target.id]);
    $('#modal-text').html(information[event.target.id]);
    $('#modal1').openModal();
}

function prepareSubmission() {
    info_dict["language"] = $('#input-language').val();
    var all_data = {};
    var flag = false;
    $("form#info-form :input").each(function () {
        var input = $(this); //get the object
        if(empty_not_allowed.indexOf(input.attr('id'))!= -1) {
            if(input.val() == "") {
                alert("Please fill the field " + input.attr('placeholder'));
                flag = true;
                return false;
            }
        }

        var list_of_el = input.val().split(",");
        list_of_el = list_of_el.map(Function.prototype.call, String.prototype.trim);
        all_data[input.attr('id').split('-')[1]] = list_of_el;
    });
    if (flag)
        return;
    var e = document.getElementById("select-function_call_must_char");
    all_data["function_call_must_char"] = [e.options[e.selectedIndex].value];
    info_dict["all_data"] = all_data;
    add_language(info_dict);
}


//Send data to server to add language to parser
function add_language(data) {

    var json = JSON.stringify(data);
     //Show loader (spinner) while waiting for server response
    $(".darken").removeClass("hide").show();
    $.ajax({
        url: '/add-language',
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
    if(response["response"])
        document.location.href = "/add-language-classification?language=" + info_dict["language"];
    else{
        alert("Something went wrong")
    }

}