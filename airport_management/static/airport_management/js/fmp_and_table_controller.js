/*
Controllers used in table (+ paginations) and the flight management panel
(fmp).
*/

// AngularJS controllers.

// Controller for the flight management panel.
app.controller(
  CONTROLLER_STRING.FLIGHT_MANAGEMENT_PANEL,
  function ($scope) {
    $scope.control_buttons = [
      {
        "bootstrap_color": "btn-default",
        "text": "add/change<br />lane"
      },
      {
        "bootstrap_color": "btn-default",
        "text": "add/remove<br />atc"
      },
      {
        "bootstrap_color": "btn-success",
        "text": "submit"
      }
    ];
  }
);

// Controller for arrival flight table and departure flight table.
app.controller(
  CONTROLLER_STRING.ARRIVALDEPARTURE_TABLE,
  function ($compile, $http, $scope) {
    /*
    AngularJS HTTP AJAX function to get flight from recently clicked object
    in the table.

    The controller is located in flight table because the `ng-click` event is
    in the table's row and not in the flight management panel AngularJS
    controller.

    CAUTION: The `flight_id` is the database column for flight ID, but the
    `pagination_id` is the CSS ID, not database.
    */
    $scope.table_request_flight = function (
      flight_id,     // The flight ID that was just clicked by the user.
      pagination_id, // The pagination ID.
    ) {
      /*
      Check if flight management panel is exists in the view (there is a user
      logged in).
      */
      if ($("#" + CSS.FLIGHT_MANAGEMENT_PANEL_ID).length) {
        /*
        The `requested_table` will be either `1` (for arrival flight table) or
        `2` (for departure flight table).
        */
        var requested_table;
        if (pagination_id === CSS.ARRIVAL_FLIGHT_TABLE_PAGINATION_ID) {
          requested_table = AOD.ARRIVAL;
        }
        else if (pagination_id === CSS.DEPARTURE_FLIGHT_TABLE_PAGINATION_ID) {
          requested_table = AOD.DEPARTURE;
        }

        /*
        HTTP GET request through this URL to get flight data for flight
        management panel.
        */
        var url = $("#" + CSS.TABLE_REQUEST_FLIGHT_ID)
          .attr("param");

        var dictionary = {};
        dictionary[KEY.FLIGHT_ID] = flight_id;
        dictionary[KEY.REQUESTED_TABLE] = requested_table;

        // Begin the HTTP request.
        $http({
          method: "GET",
          params: dictionary,
          url: url
        }).then(function (data) {
          // Render back the set management panel.
          $("#" + CSS.FLIGHT_MANAGEMENT_PANEL_CONTENT_ID).html(data.data);
          /*
          PENDING: Re-render back AngularJS component of the flight management
          panel content.
          */
        });
      }
    };


    /*
    These two variables are initially empty. However, these variable will
    be filled later after the corresponding DOM elements are ready.
    */
    $scope.arrival_flight_pagination;
    $scope.departure_flight_pagination;

    /*
    Functions to re-compile AngularJS after the DOMs loaded and the initial
    AngularJS components had been rendered.
    */
    $scope.recompile_table_pagination = function () {
      $scope.recompile_arrival_table_pagination();
      $scope.recompile_departure_table_pagination();
    };
    $scope.recompile_arrival_table_pagination = function () {
      if ($scope.arrival_flight_pagination) {
        $compile($scope.arrival_flight_pagination.contents())($scope);
      }
    };
    $scope.recompile_departure_table_pagination = function () {
      if ($scope.departure_flight_pagination) {
        $compile($scope.departure_flight_pagination.contents())($scope);
      }
    };

    $scope.pagination_request_flight_table = function (
      arrivaldeparture_enum, requested_pagination_page
    ) {
      var url = $("#" + CSS.PAGINATION_REQUEST_FLIGHT_TABLE_ID).attr("param");

      var arrivaldeparture_scope;
      var arrivaldeparture_scope_recompile;
      var pagination_number_of_pages;

      var pagination_id;
      var table_error_id;
      var table_id;
      var table_requesting_id;

      // Closure, set values before processing.
      var pagination_request_flight_table_ = function (
        arrivaldeparture_scope_value,
        arrivaldeparture_scope_recompile_value,
        pagination_number_of_pages_value,
        pagination_id_value,
        table_error_id_value,
        table_id_value,
        table_requesting_id_value
      ) {
        arrivaldeparture_scope = arrivaldeparture_scope_value;
        arrivaldeparture_scope_recompile =
          arrivaldeparture_scope_recompile_value;
        pagination_number_of_pages = pagination_number_of_pages_value;

        pagination_id  = pagination_id_value;
        table_error_id = table_error_id_value;
        table_id = table_id_value;
        table_requesting_id = table_requesting_id_value;
      };

      if (arrivaldeparture_enum === AOD.ARRIVAL) {
        pagination_request_flight_table_(
          $scope.arrival_flight_pagination,
          $scope.recompile_arrival_table_pagination,
          arrival_pagination_number_of_pages,
          CSS.ARRIVAL_FLIGHT_TABLE_PAGINATION_ID,
          CSS.ARRIVAL_FLIGHT_TABLE_ERROR_ID,
          CSS.ARRIVAL_FLIGHT_TABLE_ID,
          CSS.ARRIVAL_FLIGHT_TABLE_REQUESTING_ID
        );
      }
      else if (arrivaldeparture_enum === AOD.DEPARTURE) {
        pagination_request_flight_table_(
          $scope.departure_flight_pagination,
          $scope.recompile_departure_table_pagination,
          departure_pagination_number_of_pages,
          CSS.DEPARTURE_FLIGHT_TABLE_PAGINATION_ID,
          CSS.DEPARTURE_FLIGHT_TABLE_ERROR_ID,
          CSS.DEPARTURE_FLIGHT_TABLE_ID,
          CSS.DEPARTURE_FLIGHT_TABLE_REQUESTING_ID
        );
      }

      // Set appropriate style before the HTTP requests begin.
      $("#" + table_error_id).css("display", "none");
      $("#" + table_id).css("display", "none");
      $("#" + table_requesting_id).css("display", "");

      var dictionary = {};
      dictionary[KEY.REQUESTED_PAGINATION_PAGE] = requested_pagination_page;
      dictionary[KEY.REQUESTED_TABLE] = arrivaldeparture_enum;

      $http({
        method: "GET",
        params: dictionary,
        url: url
      }).then(function (data) {
        // Make sure the status code returned is a success code.
        if (data.status === 200) {
          // Set appropriate style before the HTTP requests done.
          $("#" + table_error_id).css("display", "none");
          $("#" + table_id).css("display", "");
          $("#" + table_requesting_id).css("display", "none");

          // Set the inner HTML of arrival or departure table.
          $("#" + table_id).html(data.data[KEY.TABLE_HTML]);

          // Compile the HTML table back.
          $compile($("#" + table_id).contents())($scope);

          // In case the total number of pages changed.
          if (data.data[KEY.NUMBER_OF_PAGES] != pagination_number_of_pages) {
            // Destroy and make new pagination.
            $("#" + pagination_id).pagination("destroy");
            arrivaldeparture_scope =
              create_pagination_for_arrivaldeparture_table(
                arrivaldeparture_enum,          // Enumeration for flights.
                "#" + pagination_id,            // ID for table pagination.
                data.data[KEY.NUMBER_OF_PAGES], // Total pages.
                requested_pagination_page       // Currently requested page.
              );

            // Set back the pagination pages number. Hard coded. Sorry!
            if (arrivaldeparture_enum === AOD.ARRIVAL) {
              arrival_pagination_number_of_pages = arrivaldeparture_scope.items;
            }
            else if (arrivaldeparture_enum === AOD.DEPARTURE) {
              departure_pagination_number_of_pages =
                arrivaldeparture_scope.items;
            }

            // Re-compile the newly made pagination bar.
            arrivaldeparture_scope_recompile();
          }
        }
        else {
          // Happens when the server returned error code.
          $("#" + table_error_id).css("display", "");
          $("#" + table_id).css("display", "none");
          $("#" + table_requesting_id).css("display", "none");
        }
      });
    };
  }
);