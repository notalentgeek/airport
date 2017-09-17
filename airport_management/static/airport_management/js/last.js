$(function () {
  // Initial setup for both pagination.

  // Get the controller.
  var table_scope = get_angular_scope_by_dom_id("arrivaldeparture-table-sets-container");

  // Get pagination pages for both paginations.

  arrival_pagination_number_of_pages = parseInt(dom_get_and_set.get_dom_param("#arrival-flight-table-pagination-number-of-pages"));
  departure_pagination_number_of_pages = parseInt(dom_get_and_set.get_dom_param("#departure-flight-table-pagination-number-of-pages"));

  console.log(arrival_pagination_number_of_pages);
  console.log(departure_pagination_number_of_pages);

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