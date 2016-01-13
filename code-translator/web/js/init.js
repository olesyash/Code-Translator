(function ($){
  $(function(){

    $('.button-collapse').sideNav();
    $('.parallax').parallax();
    get_languages();
  }); // end of document ready
})(jQuery); // end of jQuery name space

var sendData;
var pressed = true;
var selected = 0;
var languages_response;
var start = 0;
var counter = 0;
var MAX = 5;
var minPage, maxPage;
var cardCounter = 0;

/////////////debugging
//            $('#response-card').removeClass('hide').show()
//            .draggable()
//            .resizable();
//            $('#result-card').html("sssssssssssssssssssss" +
//                "sssss sss ssss ssssss ssss s s s s  s sss s s s s s s s s s s s s s s  sssssssssssss" +
//                "ssssssssss s s      sssss ssssssssssss s s s s ssssssssss ssssss sssss ssss ssss ss  ssss ss sss" +
//                "ssssssssss s s      sssss ssssssssssss s s s s ssssssssss ssssss sssss ssss ssss ss  ssss ss sss" +
//                "ssssssssss s s      sssss ssssssssssss s s s s ssssssssss ssssss sssss ssss ssss ss  ssss ss sss"
//            );

/////////////////////////////////////////

function get_languages()
{
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
                maxPage = parseInt(response.length/MAX) - 1;
                if(response.length%MAX >0)
                    maxPage ++;
                add_pagination();

            }
        });
}

function add_pagination()
{
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
    if(counter == minPage)
	    element.setAttribute("class", disabled);
    else
        element.setAttribute("class", enabled);
	element.setAttribute("id", "returnPage");
	element.setAttribute("onclick", "prevPage()");
	element.innerHTML = '<a><i class="material-icons">chevron_left</i></a>';
	list.appendChild(element);

     for(var i = start; i< MAX*(counter+1); i++)
    {
        if(languages_response[i] != undefined) {
            var li = document.createElement("li");
            if (i == selected)
                li.setAttribute("class", active);
            else
                li.setAttribute("class", enabled);
            li.setAttribute("onclick", "changePage(" + i + ")");
            li.innerHTML = '<a>' + languages_response[i] + '</a>';
            list.appendChild(li);
        }
    }

    //Add right sign
    element = document.createElement("li");
    if(counter == maxPage)
        element.setAttribute("class", disabled);
    else
        element.setAttribute("class", enabled);
	element.setAttribute("id", "pageForward");
	element.setAttribute("onclick", "nextPage()");
	element.innerHTML = '<a><i class="material-icons">chevron_right</i></a>';
	list.appendChild(element);
}

function changePage(i)
{
    selected = i;
    $("#input_text").val("");
    add_pagination();
    clearCards();//Clear cards list

}

function clearCards() //Clear cards list
{
    cardCounter = 0;
    $(".response-card").remove();
}
function nextPage()
{
    if(counter < maxPage) {
        counter++;
        start = counter * MAX;
        selected = start;
        add_pagination();
    }
}

function prevPage() {
    if (counter > minPage) {
    counter--;
    start = counter * MAX;
        selected = start;
    add_pagination();
    }
}

$("#tranalslateBtn").click(

function ()
{
    if(pressed) { //Translate button was pressed, show translation
        pressed = false;
        sendData = $('#input_text').val();
        var dict = {"text": sendData, "language": languages_response[selected]};
        var json = JSON.stringify(dict);
        $.ajax({
            url: '/gettranslation',
            type: "POST",
            data: json,
            contentType: "json", //'text/html; charset=utf-8',
            dataType: "json",
            statusCode: {
                400: function () {
                }
            },
            success: function (response, message, jq) {
                var res = response;
                $("#input-card").append('<span class="black-text" id="translation-card"></span>');
                show_translation(res);

            }
        });
    }
    else //back button was pressed, go back to translation
    {
          $("#translation-card").remove();
        clearCards(); //Clear cards list
        $('.input-field').show();
        $('#input-card').hide();
        pressed = true;
         $("#tranalslateBtn").html("Translate");
        $('#response-card').hide();
    }

}
);

function show_translation(response)
{
     var cards = document.getElementById("cards-container");

    $('.input-field').hide();
    $('#input-card').removeClass('hide')
    .show();

    $('#translation-card')
    .lettering('words')
        .mouseover(function (event) {
        var word = event.target.innerHTML;
     var h = parseInt(response.length/3) + 1;
     cards.setAttribute("style", " min-height:"+h*300+"px");
    for(var i = 0; i< response.length; i++)
    {
        if(word == response[i].keyword) {
            translation = response[i].translation;
            var $found = $('#card'+i);
            if($found.length)
            {
                if($found.is(":hidden"))
                   $found.show();
            }
            else
            {
                 var card = createCard(translation, response[i].link, i);
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

    });
    $('#translation-card').html(color_keywords(response));

    $("#tranalslateBtn").html("Back");
    pressed = false;
}

function color_keywords(response)
{
    var text = sendData.toString();
    var res = text.split(" ");
    var res2 = text.split(" ");
    res2.sort();
    console.log(""+res);
    console.log(""+res2);
    var newText = "";
    var j = 0;
    var flag;
    for(var i = 0; i<res.length; i++)
    {
        flag = false;
        for(j = 0; j<response.length; j++)
        {
            if(res[i] == response[j].keyword)
            {
                var span = "<span style='color: red;'>" + res[i] +"</span>";
                newText = newText + " " + span;
                flag = true;
            }
        }
        if(!flag)
        {
             newText = newText + " " + res[i];
        }
    }
    return newText;
}


function createCard(translatedText, link, i)
{
    var card = document.createElement("div"); // <div class="card-panel response-card">
     card.className = "card response-card";
    card.setAttribute("id", "card"+i);
    var initH = $('#cards-container').offset().top;
    var initW = $('#cards-container').offset().left;
    var space = 10;
    var h = initH + parseInt(cardCounter/3)*300 + space*(parseInt(cardCounter/3));
    var w = initW + (cardCounter%3)*300 + space*(cardCounter%3);
    card.setAttribute("style", "left:"+ w +"px; top:"+ h +"px");
    var img = document.createElement("img"); // <img src="images/exit.png" class="exit">
    img.setAttribute("src", "images/exit.png");
    img.addEventListener("click", function(){
            $("#card"+i).hide();
        });

    img.className = "exit";
    var text_el = document.createElement("div"); //<div class="black-text" id="result-card"></div>
    text_el.setAttribute("class", "card-content black-text result-card");
    text_el.innerHTML = translatedText;
    var action = document.createElement("div");
    action.className = "card-action";

    var l1  = document.createElement("a");
    var linkText = document.createTextNode("Go To Site");
    l1.setAttribute("target", '_blank');
    l1.href = link;
    l1.title = link;
    l1.appendChild(linkText);

    var l2  = document.createElement("a");
    var linkText2 = document.createTextNode("Wrong?");
    l2.title = "#!";
    l2.href = "#!";
    l2.appendChild(linkText2);

    action.appendChild(l1);
    action.appendChild(l2);
    card.appendChild(img);
    card.appendChild(text_el);
    card.appendChild(action);
    cardCounter ++;
    return  card;
}


