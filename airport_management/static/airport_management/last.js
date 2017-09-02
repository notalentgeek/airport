$(function() {
  /*
  Initiate the paginations for arrival and departure. Get the reference to
  arrival pagination and departure pagination AngularJS controller.
  */
  var scope_angularjs_controller = angular.element(
    document.getElementById("table-arrivaldeparture-main")).scope();

  var arrival_pagination_id = "pagination-arrival";
  var departure_pagination_id = "pagination-departure";

  /*
  The amount of pagination to hold all tables. Both are global variables in
  airplane_ticket.js.
  */
  arrival_num_pages = parseInt(
    document.getElementById(arrival_pagination_id).getAttribute("param"));
  departure_num_pages = parseInt(
    document.getElementById(departure_pagination_id).getAttribute("param"));

  // Create the pagination and assign it to AngularJS controller's scope.
  scope_angularjs_controller.arrival_pagination =
    set_table_pagination_for_arrivaldeparture(AOD.ARRIVAL,
      "#" + arrival_pagination_id, arrival_num_pages);
  scope_angularjs_controller.departure_pagination =
    set_table_pagination_for_arrivaldeparture(AOD.DEPARTURE,
      "#" + departure_pagination_id, departure_num_pages);

  // Re-compile/re-render the paginations.
  scope_angularjs_controller.recompile_pagination();

  /*
  For debug purposes only, show manually the atc registration form pagination.
  */
  $("#atc-form-modal").modal("show");
});

window.onload = function () {
  // Adjust the string in the navigation bar.
  auto_resize_navbar();
  auto_style_atc_form_button();

  // Adjust the tables.
  auto_adjust_tables();
};

window.addEventListener("resize", function () {
  /*
  Adding fix to the title "ellipse" when the view port is below 855 pixels but
  still above 769 pixels (before the burger button shows)
  */
  auto_resize_navbar();
  auto_style_atc_form_button();

  // Adjust the tables.
  auto_adjust_tables();
});