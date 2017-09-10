// Functions.

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
Get the AngularJS controller for the pagination buttons. The `.element()`'s
parameter for some reason cannot accept JQuery selector.
*/
function get_angularjs_scope (dom_id) {
  return angular.element(document.getElementById(dom_id)).scope();
}

/*
Function to detect THE INITIAL device, whether it is a touch screen or
non-touch screen display.
*/
function is_touch_device () {
  return (("ontouchstart" in window)
    || (navigator.MaxTouchPoints > 0)
    || (navigator.msMaxTouchPoints > 0));
}