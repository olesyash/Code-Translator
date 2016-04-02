#Watir script to show clicking a JavaScript popup box
require "watir"
require 'watir\contrib\enabled_popup'
require 'startClicker'
require 'net/http'
require 'net/https'

$ie = Watir::IE.new  #create an object to drive the browser
$ie.goto "http://mydomain.com/ListGroups.aspx"
if $ie.contains_text("Log In")
  $ie.text_field(:name, "Login1$UserName").set("fincherm")
  $ie.text_field(:name, "Login1$Password").set("mitch")
  $ie.button(:name, "Login1$LoginButton").click
end
$ie.link(:text, "Baseline").click
$ie.link(:text, "MoonManC").click
def setDdlPriority(priority)
   ddlPriority = $ie.select_list( :name , /ddlPriority/)
   puts ddlPriority
   ddlPriority.select(priority)
   puts ddlPriority
   $ie.button(:name, "ctl00$btnSave").click_no_wait
      startClicker( "OK", 4 , "User Input" )
      sleep 1
end
setDdlPriority("2")
setDdlPriority("9")