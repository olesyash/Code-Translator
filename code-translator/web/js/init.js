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
var placeholders;

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
            li.setAttribute("onclick", "javascript:changePage(" + i + ")");
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
    add_pagination();
}

function nextPage()
{
    if(counter < maxPage) {
        counter++;
        start = counter * MAX;
        selected = start;
        console.log(start);
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

$('.exit').click(function(){
     $('.card-panel').hide();
});


$("#tranalslateBtn").click(

function ()
{
    if(pressed) { //Translate button was pressed, show translation
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
                show_translation(response);

            }
        });
    }
    else //back button was pressed, go back to translation
    {
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
    // placeholders = document.getElementById("cards-container");

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
                 var card = createCard(translation, i);
                cards.appendChild(card);
                $('.response-card')
                .draggable()
                .resizable();
            }

            //var element =  "<a target='_blank' href='"+response[i].link+"'>"+response[i].link +"<a>";

           // $('#result-card').html(translation.toString() + element);
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
    var newText = "";
    var j = 0;
    for(var i =0; i<res.length; i++)
    {
        if(j < response.length && response[j].keyword == res[i]) {
            var span = "<span style='color: red;'>" + res[i] +"</span>";
            newText = newText + " " + span;
            j++;
        }
        else
        {
            newText = newText + " " + res[i];
        }
    }
    return newText;
}


function createCard(text, i)
{
   // var col =  document.createElement("div");//"<div class="col s4">"
   // col.className = "col s4";
    var card = document.createElement("div"); // <div class="card-panel response-card">
     card.className = "card-panel response-card";
    card.setAttribute("id", "card"+i);
    var initH = $('#cards-container').offset().top;
    var initW = $('#cards-container').offset().left;
    var space = 10;
    var h = initH + parseInt(i/3)*300 + space*(parseInt(i/3));
    var w = initW + (i%3)*300 + space*(i%3);
    card.setAttribute("style", "left:"+ w +"px; top:"+ h +"px");
    var img = document.createElement("img"); // <img src="images/exit.png" class="exit">
    img.setAttribute("src", "images/exit.png");
    img.addEventListener("click", function(){
            $("#card"+i).hide();
        });

    img.className = "exit";
    var text_el = document.createElement("div"); //<div class="black-text" id="result-card"></div>
    text_el.setAttribute("class", "black-text result-card");
    text_el.innerHTML = text;

    card.appendChild(img);
    card.appendChild(text_el);
   // col.appendChild(card);
   // placeholders.appendChild(col);
    return  card;
}
