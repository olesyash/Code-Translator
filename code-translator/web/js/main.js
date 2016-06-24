/**
 * Created by olesya on 30-Apr-16.
 */

//Get jquery functions ready
(function ($) {
    $(function () {
        $('.modal-trigger').leanModal();
        $('.button-collapse').sideNav();
        $('.parallax').parallax();
        $('select').material_select();
        addPagination();
        setData();
        get_languages();

    }); // end of document ready
})(jQuery); // end of jQuery name space

// Define variables
var counter = 0;
var minPage, maxPage;
var start = 0;
var MAX = 5;
var languages_response = ["Java", "Python", "Ruby-1.9"];
var selected = 0;
var cardCounter = 0;

// In contribution page, if redirected from "wrong" on card, prepare the language and the keyword
function setData(){
    if (document.location.href.indexOf("contribution-page") > -1 && document.location.href.indexOf("keyword") > -1) {
            var ref = document.location.href.split("keyword=")[1];
            var lang = ref.split("language=")[1];
            ref = ref.split("&language=")[0];

            console.log("lang= " + lang + " kw= " + ref);
            $('#keyword').val(ref);
            var enabled = 'waves-effect';
            $('#java').attr("class", enabled);
            var active = 'teal lighten-1 z-depth-1 waves-effect waves-light active';
            $('#' + lang).attr("class", active);
            selected = languages_response.indexOf(lang);

        }
}

// Function responsible to get all languages from server and add them to pagination
function get_languages() {
    $.ajax({
        url: '/gettranslation',
        type: "GET",
        contentType: 'text/html; charset=utf-8',
        dataType: "json ",
        statusCode: {
            400: function () {
            }
        },
        success: function (response, message, jq) {
            languages_response = response;
            minPage = 0;
            maxPage = parseInt(response.length / MAX) - 1; // prepare max number of languages per pagination 'page'
            if (response.length % MAX > 0)
                maxPage++;
            setData(); // Treat languages on contribution page
            addPagination(); // Add languages to pagination

        }
    });
}

// Function responsible to add languages to pagination
function addPagination() {
    var list = document.getElementById("languages");
    var disabled = "disabled";
    var enabled = 'waves-effect';
    var active = 'teal lighten-1 z-depth-1 waves-effect waves-light active';

    //Clear pagination list
    while (list.firstChild) {
        list.removeChild(list.firstChild);
    }

    //Add left sign
    var element = document.createElement("li");
    if (counter == minPage)
        element.setAttribute("class", disabled);
    else
        element.setAttribute("class", enabled);
    element.setAttribute("id", "returnPage");
    element.setAttribute("onclick", "prevPage()");
    element.innerHTML = '<a><i class="material-icons">chevron_left</i></a>';
    list.appendChild(element);

    // Add pagination elements
    for (var i = start; i < MAX * (counter + 1); i++) {
        if (languages_response[i] != undefined) {
            var li = document.createElement("li");
            if (i == selected)
                li.setAttribute("class", active);
            else
                li.setAttribute("class", enabled);
            li.setAttribute("onclick", "changePage(" + i + ")");
            li.innerHTML = '<a>' + languages_response[i] + '</a>';
            li.setAttribute("id", languages_response[i]);
            list.appendChild(li);
        }
    }

    //Add right sign
    element = document.createElement("li");

    // Check if need to enable or disable right sign
    if (counter == maxPage)
        element.setAttribute("class", disabled);
    else
        element.setAttribute("class", enabled);
    element.setAttribute("id", "pageForward");
    element.setAttribute("onclick", "nextPage()");
    element.innerHTML = '<a><i class="material-icons">chevron_right</i></a>';
    list.appendChild(element);
}

// Function called when right sign pressed, redesign pagination
function nextPage() {
    if (counter < maxPage) {
        counter++;
        start = counter * MAX;
        selected = start;
        addPagination();
    }
}

// Function called when left sign pressed redesign pagination
function prevPage() {
    if (counter > minPage) {
        counter--;
        start = counter * MAX;
        selected = start;
        addPagination();
    }
}

// Function called when selected element on pagination
function changePage(i) {
    selected = i;
    $("#input_text").val("");
    addPagination();
    clearCards();//Clear cards list

}

//Clear cards list
function clearCards()
{
    cardCounter = 0;
    $(".response-card").remove();
}