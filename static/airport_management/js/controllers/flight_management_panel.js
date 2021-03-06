var flight_management_panel = function (
  angularjs_app,
  dom_id_flight_lane_form_modal,
  dom_id_flight_online_atc_form_modal
) {
  var init_count = 1; // Singleton.
  var instances = [];

  function create_instance () {
    var instance = new flight_management_panel(angularjs_app);
    return instance;
  }

  function flight_management_panel (angularjs_app) {
    var ANGULARJS_CONTROLLER = Object.freeze({
      FLIGHT_MANAGEMENT_PANEL: "flight_management_panel"
    });

    var DOM_ID = Object.freeze({
      FLIGHT_MANAGEMENT_PANEL: "flight-management-panel",
      FLIGHT_MANAGEMENT_PANEL_INFORMATION:
        "flight-management-panel-information"
    });
    this.DOM_ID = DOM_ID;

    // Function to check if flight management panel is exists.
    this.is_exists = function () {
      return $("#" + DOM_ID.FLIGHT_MANAGEMENT_PANEL).length;
    };

    angularjs_app.controller(
      ANGULARJS_CONTROLLER.FLIGHT_MANAGEMENT_PANEL,
      function ($scope) {
        /*
        Function to show a modal form for assigning ATCs into a flight.

        PENDING: Change `...online_atc...` into `...online_atcs...`.
        */
        $scope.show_flight_lane_form_modal = function () {
          bootstrap_operation.show_bootstrap_modal(
            "#" + dom_id_flight_lane_form_modal
          );
        };

        // Function to show a modal form for assigning ATCs into a flight.
        $scope.show_flight_online_atc_form_modal = function () {
          bootstrap_operation.show_bootstrap_modal(
            "#" + dom_id_flight_online_atc_form_modal
          );
        };

        // Flight management panel buttons.
        $scope.flight_management_panel_buttons = [
          {
            bootstrap_color_class: "btn-default",
            ng_click: $scope.show_flight_lane_form_modal,
            text: "add/change<br />lane"
          },
          {
            bootstrap_color_class: "btn-default",
            ng_click: $scope.show_flight_online_atc_form_modal,
            text: "add/change<br />online atc"
          },
        ];
      }
    );
  };

  return (function () {
    for (var i = 0; i < init_count; i ++) {
      if (!instances[i]) {
        instances.push(create_instance());
      }
    }

    return instances[init_count - 1];
  })();
}