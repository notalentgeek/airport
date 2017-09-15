// Number of pages in arrival and departure paginations.
var arrival_pagination_number_of_pages;
var departure_pagination_number_of_pages;

var dom_get_and_set = {
  get_dom_attribute: function (jquery_selector, attribute) {
    return $(jquery_selector).attr(attribute);
  },
  get_dom_param: function (jquery_selector) {
    return this.get_dom_attribute(jquery_selector, "param");
  },
  get_dom_value: function (jquery_selector) {
    return this.get_dom_attribute(jquery_selector, "value");
  },
  set_dom_attribute: function (jquery_selector, attribute, value) {
    return $(jquery_selector).attr(attribute, value);
  },
  set_dom_value: function (jquery_selector, value) {
    return this.set_dom_attribute(jquery_selector, "value", value);
  }
};

var string_to_list = function (string) {
  return string.replace(" ", "").replace("[", "").replace("]", "").split(",");
};

// Start-up function related to DjangoTemplate.

/*
Check if wrong password UI is exists. If so, show wrong password modal. This
function only executed when the index.html rendered for the first time.
*/
var check_wrong_password_modal = (function () {
  // Modal for wrong password.
  var password_input = $("#" + CSS.AIRPORT_MANAGER_PASSWORD_INPUT_ID);

  // Check if the DOM element exists in the view port.
  if (password_input.length) {
    /*
    `string_to_bool(password_input.attr("param"))` return a boolean from Django
    for the index.html to be rendered with password wrong modal or not.
    */
    if (password_input.attr("param")){
      if (string_to_bool(password_input.attr("param"))) {
        $("#" + CSS.AIRPORT_MANAGER_WRONG_PASSWORD_MODAL_ID).modal("show");
      }
    }
  }
})();

/*
JavaScript string ellipsis to prevent overflow and limit the number of
characters.
*/
var string_overflow_ellipsis = function(string, limit, ellipsis_string) {
  if (!ellipsis_string) {
    ellipsis_string = "...";
  }

  if (ellipsis_string.length < string.length &&
    ellipsis_string.length < limit){
    string_reduced = string.substr(0, limit - ellipsis_string.length);
    string_ellipsed = string_reduced + ellipsis_string;
    return string > limit ? string_ellipsed : string;
  }
  return string;
};

var show_bootstrap_modal = function (jquery_selector) {
  $(jquery_selector).modal("show");
}

// Initiating AngularJS application.
var app = angular.module("airport_management", ["ngSanitize"]);