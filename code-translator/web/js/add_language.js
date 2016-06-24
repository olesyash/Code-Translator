/**
 * Created by olesya on 11-Jun-16.
 */

//Get jquery functions ready
$(document).ready(function () {
    $('.button-collapse').sideNav();
    $('.parallax').parallax();
    $('.modal-trigger').leanModal();
    $('select').material_select();
});

// Define variables
var info_dict = {};

// Define headers map to add information showed when information icon pressed
var header =
{
    "language-info": "How to add language: 'language' field",
    "keywords-info": "How to add language: 'keywords' field",
    "literals-info": "How to add language: 'literals' field",
    "operations-info": "How to add language: 'operators' field",
    "str_symbol1-info": "How to add language: 'first string start symbol' field",
    "str_symbol2-info": "How to add language: 'second string start symbol' field",
    "escape_character-info": "How to add language: 'escape character symbol' field",
    "start_comment_symb-info": "How to add language: 'start one line comment symbol' field",
    "comment_start1-info": "How to add language: 'first start symbol for two lines comment ' field",
    "comment_end1-info": "How to add language: 'first end symbol two lines comment' field",
    "comment_start2-info": "How to add language: 'second start symbol for two lines comment' field",
    "comment_end2-info": "How to add language: 'second end symbol two lines comment' field",
    "add_library-info": "How to add language: 'import library' field",
    "func_def-info": "How to add language: 'function definition keyword' field",
    "func_start-info": "How to add language: 'function definition symbol' field",
    "function_call_char-info": "How to add language: 'function call symbol' field",
    "class_keyword-info": "How to add language: 'class definition keyword' field"
};

// List of elements that not allowed to be empty when new language added
var empty_not_allowed = ['input-language', 'input-keywords', 'input-operations', 'input-str_symbol1', 'input-str_symbol2'];

// Define information map to add information showed when information icon pressed
var information =
{
    "language-info": "Please insert here the name of the language you want to add to Code Translator. " +
    "Please follow first letter uppercase convention - for example: Java, Python, Ruby",
    "keywords-info": "Please insert here list of all keywords, separated by comma. Please pay attention - it case sensitive! <br>" +
    "Example: for, if, else ",
    "literals-info": "Please insert here list of all literals, separated by comma. Please pay attention - it case sensitive! <br>" +
    "Example: True, False",
    "operations-info": "Please insert here list of all operators, separated by comma. <br> " +
    "Example: ++, --, ==, +=",
    "str_symbol1-info": "Please insert here single symbol that string begin with, usually \" or \' ",
    "str_symbol2-info": "Please insert here single symbol that string begin with, usually \" or \' ",
    "escape_character-info": "Please insert here single symbol that represents escape character, usually \\",
    "start_comment_symb-info": "Please insert here single symbol that one line comment begin with <br>" +
    "Example: Python: # ; Java, C: // ",
    "comment_start1-info": "Please insert here single symbol that 2 lines comment begin with <br>" +
    "Example: Python: ' ' ', Java, C: /*",
    "comment_end1-info": "Please insert here single symbol that 2 lines comment end with <br>" +
    "Example: Python: ' ' ', Java, C: */",
    "comment_start2-info": "Please insert here another single symbol that 2 lines comment begin with <br>" +
    "Example: Python:  \" \" \" <br> If there is no such, leave it empty",
    "comment_end2-info": "Please insert here another single symbol that 2 lines comment end with <br>" +
    "Example: Python:  \" \" \"" +" <br> If there is no such, leave it empty",
    "add_library-info": "Please insert here the keywords describing adding library. <br>" +
    "Example: Python: import, from ; Java: import ; Ruby: require",
    "func_def-info": "Please insert here the keyword/s used to define function <br>" +
    "Example: Python: def; Java: public, private ; JS: function",
    "func_start-info": "Please insert here the symbol that describing start of function definition, usually '(' " +
    "<br> If not required as it in ruby, leave it empty. <br>" +
    "Example: in ruby you can define method without '('  <br> def method_name <br>"+
                                                    "<span class=\"tab\">expresion</span>  <br>"+
                                                      "end<br>",
    "function_call_char-info": "Please insert here the symbol that describing function call, usually '( <br>" +
    "Example: if function foo is defined, to call the function use foo()",
    "class_keyword-info": "Please insert here the keyword describing class definition, please pay attention - it case sensitive! <br>" +
    "Example: class, Class",
    "function_call_must_char-info": "Please choose True/False. Is the function call char must appear to call a function?" +
    "<br> Example: in ruby, if function foo is defined, you can call it foo() or foo. So in ruby, we will choose False. <br>" +
    "Default is True"
};

// Add listener to information icons
$(document).on("click", ".material-icons", showInfo);
// Add listener to next button
$(document).on("click", "#nextBtn", prepareSubmission);

// This function responsible to show the information of the element when "information" icon near the element pressed
function showInfo(event) {
    console.log(event.target.id);
    $('#modal-header').html(header[event.target.id]);
    $('#modal-text').html(information[event.target.id]);
    $('#modal1').openModal();
}

// This function preparing the data to be sent to server when "next" button pressed
function prepareSubmission() {
    info_dict["language"] = $('#input-language').val(); // prepare language
    var all_data = {};
    var flag = false;
    // Take details from the form
    $("form#info-form :input").each(function () {
        var input = $(this); //get the object
        if(empty_not_allowed.indexOf(input.attr('id'))!= -1) {
            if(input.val() == "") {
                alert("Please fill the field " + input.attr('placeholder'));
                flag = true;
                return false;
            }
        }
        // Save all lists in array by splitting it by comma and removing all spaces around the words
        var list_of_el = input.val().split(",");
        list_of_el = list_of_el.map(Function.prototype.call, String.prototype.trim);
        all_data[input.attr('id').split('-')[1]] = list_of_el;
    });
    if (flag) // If one of the must fields in empty, do not sent the data
        return;
    var e = document.getElementById("select-function_call_must_char");
    all_data["function_call_must_char"] = [e.options[e.selectedIndex].value];
    info_dict["all_data"] = all_data;
    console.log(info_dict);
    add_language(info_dict); //Send to server the information collected from contributor
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
                $("2.darken").hide(); //stop spinner
            },
            500: function () {
                 $(".darken").hide(); //stop spinner
                alert("Sorry, there is some error in the server side =(")
            }
        },
        success: function (response, message, jq) {
            console.log(response);
             $(".darken").hide(); //stop spinner
            TreatResponse(response); // treat response
        }
    });
}

// Treat response from server, if succeed redirect to next page, if not - alert on error
function TreatResponse(response) {
    console.log(response["response"]);
    if(response["response"])
        document.location.href = "/add-language-classification?language=" + info_dict["language"];
    else{
        alert("Something went wrong")
    }

}