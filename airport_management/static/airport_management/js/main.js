// Number of pages in arrival and departure paginations.
var arrival_pagination_number_of_pages;
var departure_pagination_number_of_pages;

// Initiating AngularJS application.
var app = angular.module("airport_management", ["ngSanitize"]);

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