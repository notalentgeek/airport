$(function () {
  // Initial setup for both pagination.

  // Get the controller.
  var table_scope = get_angularjs_scope(
    CSS.ARRIVALDEPARTURE_TABLE_SET_CONTAINER_ID);

  // Get pagination pages for both paginations.
  arrival_pagination_number_of_pages = parseInt(
    $("#" + CSS.ARRIVAL_FLIGHT_TABLE_PAGINATION_ID).attr("param"));
  departure_pagination_number_of_pages = parseInt(
    $("#" + CSS.DEPARTURE_FLIGHT_TABLE_PAGINATION_ID).attr("param"));

  // Create paginations.
  table_scope.arrival_flight_pagination =
    create_pagination_for_arrivaldeparture_table(
      AOD.ARRIVAL,
      CSS.ARRIVAL_FLIGHT_TABLE_PAGINATION_ID,
      arrival_pagination_number_of_pages
    );
  table_scope.departure_flight_pagination =
    create_pagination_for_arrivaldeparture_table(
      AOD.DEPARTURE,
      CSS.DEPARTURE_FLIGHT_TABLE_PAGINATION_ID,
      departure_pagination_number_of_pages
    );

  // Re-compile paginations back with AngularJS.
  table_scope.recompile_table_pagination();
});

window.onload = function () {
  auto_adjust();
};

window.addEventListener("resize", function () {
  auto_adjust();
});