/*
There is a hack I used in the jquery.simplePagination.js to force ellipsed
pagination to select the proper pagination page and table. The hack is located
in line 47 and 373 - 384 of jquery.simplePagination.js.
*/

// Function to return boolean from an exact string.
function string_to_bool (to_bool) {
  if (to_bool === null) {
    return false;
  }

  switch(to_bool.toLowerCase().trim()){
    case "1": case "true": case "yes": case "True": return true;
    case "0": case "false": case "no": case "False": return false;
    default: return Boolean(to_bool);
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

/*
Simple enumeration for arrival or departure. `AOD` is meant for "arrival or
departure". Do not use `0` as an enumeration value because it can be coerced
into `false`.
*/
var AOD = Object.freeze({ ARRIVAL: 1, DEPARTURE: 2 });

// Number of pages in arrival and departure paginations.
var arrival_num_pages, departure_num_pages;

// Initiating AngularJS application.
var app = angular.module("airport_management", ["ngSanitize"]);