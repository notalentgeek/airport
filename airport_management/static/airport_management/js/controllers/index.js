// Initiating AngularJS application.
var app = angular.module("airport_management", ["ngSanitize"]);

/*
Initiate controllers and set the views.

PENDING: Make a setter function for every class that has other object as
parameters. Those objects should not be inputted from parameters but setter
functions.
*/

// Initiate all modal views first.

// Modal that will be shown if username and password combination was wrong.
airport_manager_wrong_password_modal =
  new airport_manager_wrong_password_modal();

// Modal to show all registered air traffic controllers (ATCs).
atc_list_modal = new atc_list_modal(app);

// Modal used to hold a form to register a new ATC.
atc_registration_form_modal = new atc_registration_form_modal(app);

/*
Modal used to let the airport manager (the main user) to assign ATCs in a
registered flight.
*/
flight_online_atcs_form_modal = new flight_online_atcs_form_modal(app);

// Modal page used to control lane of the ongoing flight.
flight_lane_form_modal = new flight_lane_form_modal(app);

/*
Flight management panel located in the top of the table sets and just below
navigation bar.
*/
flight_management_panel = new flight_management_panel(
  app,
  flight_lane_form_modal.DOM_ID.FLIGHT_LANE_FORM_MODAL,
  flight_online_atcs_form_modal.DOM_ID.FLIGHT_ONLINE_ATCS_FORM_MODAL
);

// Navigation bars.

// Right navigation bar.
navbar_right = new navbar_right(app);

// Left navigation bar.
navbar_left = new navbar_left(app,
  navbar_right.JQUERY_SELECTOR.AIRPORT_MANAGER_BUTTON,
  [atc_list_modal, atc_registration_form_modal]  
);

// Initiate the inner part of the both tables.
inner_table = new inner_table();

/*
Initiate both arrival flight table and departure flight table.

PENDING: inner_table.js should be initiated after the table.js. Hence, it
should not be appeared as an argument, but more from setter function.
*/ 
table = new table(
  app,
  flight_management_panel.DOM_ID.FLIGHT_MANAGEMENT_PANEL_INFORMATION,
  flight_online_atcs_form_modal,
  inner_table
);

// Functions that need to be initiated after all views ready.
airport_manager_wrong_password_modal.check_wrong_password();

/*
Functions that adjust user interfaces when the viewport resolution is
changed.
*/
var adjust = function () {
  inner_table.adjust_table();
  navbar_left.adjust_atc_modal_buttons();
  navbar_left.adjust_title();
  navbar_right.adjust_airport_manager_button();
};

// Global listeners.
window.onload = function () {
  adjust();
};

window.addEventListener("resize", function () {
  adjust();
});