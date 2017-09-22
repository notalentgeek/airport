var table = function (
  angularjs_app,
  flight_management_panel_information_id,
  flight_lane_form_modal,
  flight_online_atcs_form_modal,
  inner_table
) {
  var init_count = 1; // Singleton.
  var instances = [];

  function create_instance () {
    var instance = new table(
      angularjs_app,
      flight_management_panel_information_id,
      flight_online_atcs_form_modal
    );
    return instance;
  }

  function table (
    angularjs_app,
    flight_management_panel_information_id,
    flight_online_atcs_form_modal
  ) {
    var ANGULARJS_CONTROLLER = Object.freeze({
      ARRIVALDEPARTURE_TABLE_SETS_CONTAINER:
        "arrivaldeparture_table_sets_container",
    });
    
    var AOD = Object.freeze({
      // Based from Python enumeration.
      ARRIVAL: "1",
      DEPARTURE: "2"
    });
    
    var DOM_CLASS = Object.freeze({
      CLICKABLE: "clickable",
      PAGINATION_BUTTON_DYNAMIC_WIDTH: "pagination-button-dynamic-width",
      PAGINATION_BUTTON_FIXED_WIDTH: "pagination-button-fixed-width"
    });

    var DOM_ID = Object.freeze({
      ARRIVALDEPARTURE_TABLE_SETS_CONTAINER:
        "arrivaldeparture-table-sets-container",
      ARRIVAL_FLIGHT_TABLE: "arrival-flight-table",
      ARRIVAL_FLIGHT_TABLE_ERROR: "arrival-flight-table-error",
      ARRIVAL_FLIGHT_TABLE_PAGINATION: "arrival-flight-table-pagination",
      ARRIVAL_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES:
        "arrival-flight-table-pagination-number-of-pages",
      ARRIVAL_FLIGHT_TABLE_REQUESTING: "arrival-flight-table-requesting",
      DEPARTURE_FLIGHT_TABLE: "departure-flight-table",
      DEPARTURE_FLIGHT_TABLE_ERROR: "departure-flight-table-error",
      DEPARTURE_FLIGHT_TABLE_PAGINATION: "departure-flight-table-pagination",
      DEPARTURE_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES:
        "departure-flight-table-pagination-number-of-pages",
      DEPARTURE_FLIGHT_TABLE_REQUESTING: "departure-flight-table-requesting",
      PAGINATION_REQUEST_FLIGHT_TABLE_URL:
        "pagination-request-flight-table-url",
      TABLE_REQUEST_FLIGHT_URL: "table-request-flight-url"
    });

    var KEY = Object.freeze({
      ARRIVAL_FLIGHT_TABLE_PAGINATION: "arrival_flight_table_pagination",
      ARRIVAL_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES:
        "arrival_flight_table_pagination_number_of_pages",
      DEPARTURE_FLIGHT_TABLE_PAGINATION: "departure_flight_table_pagination",
      DEPARTURE_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES:
        "departure_flight_table_pagination_number_of_pages",  
      FLIGHT_ID: "flight_id",
      FMP_DOM: "fmp_dom",
      FMP_NON_STATUS_LANE: "fmp_non_status_lane",
      FMP_NON_STATUS_ONLINE_ATCS: "fmp_non_status_online_atcs",
      NUMBER_OF_PAGES: "number_of_pages",
      REQUESTED_TABLE: "requested_table",
      REQUESTED_TABLE_PAGINATION_PAGE: "requested_table_pagination_page",
      TABLE_HTML: "table_html"
    });

    // The amount of pages necessary for each paginations.
    var pagination_number_of_pages = {};
    
    var initiate_table_pagination = function () {
      // Get the table's AngularJS scope.
      var table_scope = angularjs_operation.get_angular_scope_by_dom_id(
        DOM_ID.ARRIVALDEPARTURE_TABLE_SETS_CONTAINER
      );

      var initiate_table_pagination_ = function (
        aod,
        pagination_number_of_pages,
        number_of_pages_dom_id,
        number_of_pages_key,
        table_pagination_dom_id,
        table_pagination_key
      ) {
        // Set the amount of pagination pages per paginations.
        pagination_number_of_pages[number_of_pages_key] = parseInt(
          dom_get_and_set.get_dom_param("#" + number_of_pages_dom_id));

        // Create the table pagination.
        table_scope.flight_table_paginations[table_pagination_key] =
          create_pagination_for_arrivaldeparture_table(
            AOD,
            DOM_CLASS,
            DOM_ID,
            aod,
            table_pagination_dom_id,
            pagination_number_of_pages[number_of_pages_key]
          );
      };

      initiate_table_pagination_(
        AOD.ARRIVAL,
        pagination_number_of_pages,
        DOM_ID.ARRIVAL_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES,
        KEY.ARRIVAL_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES,
        DOM_ID.ARRIVAL_FLIGHT_TABLE_PAGINATION,
        KEY.ARRIVAL_FLIGHT_TABLE_PAGINATION
      );

      initiate_table_pagination_(
        AOD.DEPARTURE,
        pagination_number_of_pages,
        DOM_ID.DEPARTURE_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES,
        KEY.DEPARTURE_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES,
        DOM_ID.DEPARTURE_FLIGHT_TABLE_PAGINATION,
        KEY.DEPARTURE_FLIGHT_TABLE_PAGINATION
      );

      table_scope.recompile_table_paginations();
    };

    app.controller(
      ANGULARJS_CONTROLLER.ARRIVALDEPARTURE_TABLE_SETS_CONTAINER,
      function ($compile, $http, $scope) {
        // List that holds DOM reference to each table paginations.
        $scope.flight_table_paginations = {};
    
        // Scope of later recompiled table.
        $scope.table;
    
        /*
        AngularJS HTTP AJAX function to get flight from recently clicked
        object in the table.
    
        The controller is located in flight table because the `ng-click` event
        is in the table's row and not in the flight management panel AngularJS
        controller.
    
        This on-click function is meant to let the user choose the flight
        he/she wants to edit.
    
        CAUTION: The `flight_id` is the database column for flight ID, but the
        `table_pagination_id` is the CSS ID, not database.
        */
        $scope.table_requests_flight = function (
          flight_id,          // The flight ID that was just clicked by the
                              // user.
          table_pagination_id // The pagination CSS ID.
        ) {
          // Dictionary that will be sent though HTTP.
          var dictionary = {};
          dictionary[KEY.FLIGHT_ID] = flight_id;
    
          // URL to request new flight table.
          var url = dom_get_and_set.get_dom_param("#" + 
            DOM_ID.TABLE_REQUEST_FLIGHT_URL);

          // Check if flight management panel is exists.
          if (flight_management_panel.is_exists()) {
            if (table_pagination_id ===
              DOM_ID.ARRIVAL_FLIGHT_TABLE_PAGINATION) {
              dictionary[KEY.REQUESTED_TABLE] = AOD.ARRIVAL;
            }
            else if (table_pagination_id ===
              DOM_ID.DEPARTURE_FLIGHT_TABLE_PAGINATION) {
              dictionary[KEY.REQUESTED_TABLE] = AOD.DEPARTURE;
            }
          }

          // Begin the HTTP request.
          $http({
            method: "GET",
            params: dictionary,
            url: url
          }).then(function (data) {
            // Render back the flight management panel.
            $("#" + flight_management_panel_information_id).html(
                data.data[KEY.FMP_DOM]);

            /*
            Set back the current selected value to flight management panel's
            ATCs modal and lane modal.
            */
            flight_lane_form_modal.set_selected_flight_properties(
              dictionary[KEY.REQUESTED_TABLE], dictionary[KEY.FLIGHT_ID],
              data.data[KEY.FMP_NON_STATUS_LANE]);
            flight_online_atcs_form_modal.set_selected_flight_properties(
              dictionary[KEY.REQUESTED_TABLE], dictionary[KEY.FLIGHT_ID],
              string_operation.string_to_list(
                data.data[KEY.FMP_NON_STATUS_ONLINE_ATCS]
              ));
          });
        };

        $scope.pagination_requests_flight_table = function (
          aod, requested_table_pagination_page
        ) {
          // Undefined variables.
          var arrivaldeparture_table_pagination;
          var arrivaldeparture_table_pagination_recompile;
          var pagination_number_of_pages_local;
    
          // Undefined variables to hold CSS IDs.
          var table_error_id;
          var table_id;
          var table_pagination_id;
          var table_requesting_id;
    
          var dictionary = {};
          dictionary[KEY.REQUESTED_TABLE] = aod
          dictionary[KEY.REQUESTED_TABLE_PAGINATION_PAGE] =
            requested_table_pagination_page;
    
          // Get the URL to process HTTP request.
          var url = dom_get_and_set.get_dom_param("#" +
            DOM_ID.PAGINATION_REQUEST_FLIGHT_TABLE_URL);
    
          // Closure.
          var pagination_request_flight_table_ = function (
            arrivaldeparture_table_pagination_,
            arrivaldeparture_table_pagination_recompile_,
            pagination_number_of_pages_local_,
            table_error_id_,
            table_id_,
            table_pagination_id_,
            table_requesting_id_
          ) {
            arrivaldeparture_table_pagination =
              arrivaldeparture_table_pagination_;
            arrivaldeparture_table_pagination_recompile =
              arrivaldeparture_table_pagination_recompile_;
            pagination_number_of_pages_local =
              pagination_number_of_pages_local_;
            table_error_id = table_error_id_;
            table_id = table_id_;
            table_pagination_id = table_pagination_id_;
            table_requesting_id = table_requesting_id_;
          };      

          if (aod == AOD.ARRIVAL) {
            pagination_request_flight_table_(
              $scope.flight_table_paginations
                [KEY.ARRIVAL_FLIGHT_TABLE_PAGINATION],
              $scope.recompile_arrival_flight_table_pagination,
              pagination_number_of_pages
                [KEY.ARRIVAL_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES],
              DOM_ID.ARRIVAL_FLIGHT_TABLE_ERROR,
              DOM_ID.ARRIVAL_FLIGHT_TABLE,
              DOM_ID.ARRIVAL_FLIGHT_TABLE_PAGINATION,
              DOM_ID.ARRIVAL_FLIGHT_TABLE_REQUESTING
            );
          }
          else if (aod == AOD.DEPARTURE) {
            pagination_request_flight_table_(
              $scope.flight_table_paginations
                [KEY.DEPARTURE_FLIGHT_TABLE_PAGINATION],
              $scope.recompile_departure_flight_table_pagination,
              pagination_number_of_pages
                [KEY.DEPARTURE_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES],
              DOM_ID.DEPARTURE_FLIGHT_TABLE_ERROR,
              DOM_ID.DEPARTURE_FLIGHT_TABLE,
              DOM_ID.DEPARTURE_FLIGHT_TABLE_PAGINATION,
              DOM_ID.DEPARTURE_FLIGHT_TABLE_REQUESTING
            );
          }
    
          $scope.table = $("#" + table_id);
    
          var start_table_style = (function () {
            $("#" + table_error_id).css("display", "none");
            $("#" + table_id).css("display", "none");
            $("#" + table_requesting_id).css("display", "");
          })();
    
          var error_table_style = function () {
            $("#" + table_error_id).css("display", "");
            $("#" + table_id).css("display", "none");
            $("#" + table_requesting_id).css("display", "none");
          };
    
          var success_table_style = function () {
            $("#" + table_error_id).css("display", "none");
            $("#" + table_id).css("display", "");
            $("#" + table_requesting_id).css("display", "none");
          };

          $http({
            method: "GET",
            params: dictionary,
            url: url
          }).then(function (data) {
            if (data.status === 200) {
              // Set the table style when the request is successful.
              success_table_style();

              // Set the inner HTML of the arrival table or departure table.
              $("#" + table_id).html(data.data[KEY.TABLE_HTML]);
    
              // Compile the newly added HTML table back with AngularJS.
              if ($scope.table) {
                angularjs_operation.recompile_dom_in_angularjs_scope(
                  $scope.table,
                  $scope,
                  $compile
                );
              }
    
              // Check if the number of pages is changed.
              if (data.data[KEY.NUMBER_OF_PAGES] !=
                pagination_number_of_pages_local) {
                // Destroy the old pagination.ea
                $("#" + table_pagination_id).pagination("destroy");
    
                // Create new pagination.
                arrivaldeparture_table_pagination = 
                  create_pagination_for_arrivaldeparture_table(
                    AOD,                            // Reference to constants.
                    DOM_CLASS,                      // Reference to constants.
                    DOM_ID,                         // Reference to constants.
                    this,                           // Reference to this
                                                    // object.
                    aod,                            // Enumeration for flight
                                                    // table.
                    "#" + table_pagination_id,      // CSS ID for table
                                                    // pagination.
                    data.data[KEY.NUMBER_OF_PAGES], // Total pages.
                    requested_table_pagination_page // Current requested page.
                  );
    
                /*
                Set back the pagination number of pages for future
                reference.
                */
                if (aod === AOD.ARRIVAL) {
                  /*
                  `items` in pagination object refer to how many pages are
                  there in the pagination.
                  */
                  pagination_number_of_pages
                    [KEY.ARRIVAL_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES] =
                      arrivaldeparture_table_pagination.items;
                }
                else if (aod === AOD.DEPARTURE) {
                  /*
                  `items` in pagination object refer to how many pages are
                  there in the pagination.
                  */
                  tagination_number_of_pages
                    [KEY.DEPARTURE_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES] =
                      arrivaldeparture_table_pagination.items;
                }
              }
              
              // Adjust the inner table.
              inner_table.adjust_table();
            }
            else {
              error_table_style();
            }
          });
        };
    
        /*
        Functions to recompile AngularJS after the DOMs are loaded and initial
        AngularJS components had been rendered.
        */
        $scope.recompile_table_paginations = function () {
          $scope.recompile_arrival_flight_table_pagination();
          $scope.recompile_departure_flight_table_pagination();
        };
    
        $scope.recompile_arrival_flight_table_pagination = function () {
          angularjs_operation.recompile_dom_in_angularjs_scope(
            $scope.flight_table_paginations
              [KEY.ARRIVAL_FLIGHT_TABLE_PAGINATION],
            $scope,
            $compile
          );
        };
        
        $scope.recompile_departure_flight_table_pagination = function () {
          angularjs_operation.recompile_dom_in_angularjs_scope(
            $scope.flight_table_paginations
              [KEY.DEPARTURE_FLIGHT_TABLE_PAGINATION],
            $scope,
            $compile
          );
        };
        
        // Initiate table paginations after the AngularJS elements load.
        initiate_table_pagination();
      }
    );
  }

  return (function () {
    for (var i = 0; i < init_count; i ++) {
      if (!instances[i]) {
        instances.push(create_instance());
      }
    }

    return instances[init_count - 1];
  })();
};