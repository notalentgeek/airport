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