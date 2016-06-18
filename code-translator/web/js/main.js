/**
 * Created by olesya on 30-Apr-16.
 */

(function ($) {
    $(function () {

        $('.button-collapse').sideNav();
        $('.parallax').parallax();
        addPagination();
        setData();
        get_languages();

    }); // end of document ready
})(jQuery); // end of jQuery name space

var counter = 0;
var minPage, maxPage;
var start = 0;
var MAX = 5;
var languages_response = ["Java", "Python", "Ruby-1.9"];
var selected = 0;
var cardCounter = 0;

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
            maxPage = parseInt(response.length / MAX) - 1;
            if (response.length % MAX > 0)
                maxPage++;
            setData();
            addPagination();

        }
    });
}

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
    if (counter == maxPage)
        element.setAttribute("class", disabled);
    else
        element.setAttribute("class", enabled);
    element.setAttribute("id", "pageForward");
    element.setAttribute("onclick", "nextPage()");
    element.innerHTML = '<a><i class="material-icons">chevron_right</i></a>';
    list.appendChild(element);
}


function nextPage() {
    if (counter < maxPage) {
        counter++;
        start = counter * MAX;
        selected = start;
        addPagination();
    }
}

function prevPage() {
    if (counter > minPage) {
        counter--;
        start = counter * MAX;
        selected = start;
        addPagination();
    }
}

function changePage(i) {
    selected = i;
    $("#input_text").val("");
    addPagination();
    clearCards();//Clear cards list

}

function clearCards() //Clear cards list
{
    cardCounter = 0;
    $(".response-card").remove();
}