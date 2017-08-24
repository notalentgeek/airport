// Function to return boolean from an exact string.
function string_to_bool (string) {
  switch(string.toLowerCase().trim()){
    case "1": case "true": case "yes": case "True": return true;
    case "0": case "false": case "no": case "False": case null: return false;
    default: return Boolean(string);
  }
}

/*
Function to detect THE INITIAL device, whether it is a touch screen or
non-touch screen display.
*/
function is_touch_device () {
  return (('ontouchstart' in window)
    || (navigator.MaxTouchPoints > 0)
    || (navigator.msMaxTouchPoints > 0));
}

// Initiating AngularJS application.
var app = angular.module("airport_management", []);