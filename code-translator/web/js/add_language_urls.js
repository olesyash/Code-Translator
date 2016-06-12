/**
 * Created by olesya on 12-Jun-16.
 */

$(document).ready(function () {
    $('.button-collapse').sideNav();
    $('.parallax').parallax();
    $('.modal-trigger').leanModal();
    $('select').material_select();
});
var name = "";
var selected_option;
var options_list = ["class", "id"];
var counter = 1;

for(var i=0;i<3;i++) {
    $(document).on("change", "#select-option"+i, select_listener);
}
$(document).on("click", "#add-other", addOther);
$(document).on("click", "#remove-other", removeOther);
$(document).on("click", "#addLanguageBtn",add_language);


function add_language(){
    var url = [];
    for(var i=1;i<4;i++)
    {
        var u = $('#'+ "input-url"+i);
        url[i-1] = u.val();
        console.log(url[i-1]);
    }
}


//Select option listener
function select_listener(e) {
    var id = e.target.id;
    console.log("select pressed " + id);
    var hidden;
    var e2 = document.getElementById(id);
    selected_option = e2.options[e2.selectedIndex ].value;

    if (options_list.indexOf(selected_option) != -1) {
        console.log("in if");
        hidden = "name" + id.split('select-option')[1];
        console.log(hidden);
        $("#"+hidden).removeClass("hide").show();
    }
    else {
        name = "";
        hidden = "name" + id.split('select-option')[1];
        $("#" + hidden).addClass('hide');
    }
}

function addOther(){
    if (counter <3)
        counter++;
    $("#" + counter).removeClass('hide');

}

function removeOther(){
    console.log("in remove");
    $("#" + counter).addClass('hide');
    if(counter > 1)
        counter--;
}