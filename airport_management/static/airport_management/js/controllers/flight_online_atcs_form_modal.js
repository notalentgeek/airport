var flight_online_atcs_form_modal = function (angularjs_app) {
  var init_count = 1; // Singleton.
  var instances = [];

  function create_instance () {
    var instance = new flight_online_atcs_form_modal(angularjs_app);
    return instance;
  }

  function flight_online_atcs_form_modal (angularjs_app) {
    var ANGULARJS_CONTROLLER = Object.freeze({
      FLIGHT_ATC_FORM: "flight_atc_form"
    });

    var DOM_ID = Object.freeze({
      FLIGHT_ATCS_FORM_MODAL: "flight-atcs-form-modal",
      FLIGHT_ATC_FORM_ARRIVALDEPARTURE: "flight-atc-form-arrivaldeparture",
      FLIGHT_ATC_FORM_FLIGHT_ID: "flight-atc-form-flight-id",
      FLIGHT_ATC_FORM_FLIGHT_ONLINE_ATCS: "flight-atc-form-flight-online-atcs",
      FLIGHT_ONLINE_ATC_CHECK_BOXES_: "flight-online-atc-check-boxes-"
    });
    this.DOM_ID = DOM_ID;

    var DOM_CLASS = Object.freeze({
      FLIGHT_ONLINE_ATCS_CHECK_BOX: "flight-online-atc-check-boxes"
    });

    var JQUERY_SELECTOR_FOR_FORM = Object.freeze([
      "#" + DOM_ID.FLIGHT_ATC_FORM_ARRIVALDEPARTURE,
      "#" + DOM_ID.FLIGHT_ATC_FORM_FLIGHT_ID,
      "#" + DOM_ID.FLIGHT_ATC_FORM_FLIGHT_ONLINE_ATCS
    ]);

    var selected_arrivaldeparture;
    var selected_flight_id;
    var selected_flight_online_atcs;

    var set_selected_flight_properties_to_variables = function (
      arrival_departure, flight_id, flight_online_atcs) {
      selected_arrivaldeparture = arrival_departure;
      selected_flight_id = flight_id;
      selected_flight_online_atcs = flight_online_atcs;
    };

    var set_selected_flight_properties_to_dom = function (
      arrival_departure, flight_id, flight_online_atcs) {
      values = [arrival_departure, flight_id, flight_online_atcs];
      if (JQUERY_SELECTOR_FOR_FORM.length === values.length) {
        for (var i = 0; i < JQUERY_SELECTOR_FOR_FORM.length; i ++) {
          dom_get_and_set.set_dom_value(JQUERY_SELECTOR_FOR_FORM[i], values[i]);
        }
      }
    };

    this.set_selected_flight_properties = function (
      arrival_departure, flight_id, flight_online_atcs) {
      set_selected_flight_properties_to_dom(arrival_departure, flight_id,
        flight_online_atcs);
      set_selected_flight_properties_to_variables(arrival_departure,
        flight_id, flight_online_atcs);
    };

    var get_selected_flight_properties_from_dom = (function () {
      values = [];

      for (var i = 0; i < JQUERY_SELECTOR_FOR_FORM.length; i ++) {
        values.push(dom_get_and_set.get_dom_value(
          JQUERY_SELECTOR_FOR_FORM[i]));
      }

      /*
      Variable destructing! With this method primitives can be put as
      reference instead of value.
      */
      [selected_arrivaldeparture, selected_flight_id,
        selected_flight_online_atcs] = values;

      // Convert the string "list" into a list of strings.
      selected_flight_online_atcs = string_operation.string_to_list(
        selected_flight_online_atcs
      );
    })();

    angularjs_app.controller(
      ANGULARJS_CONTROLLER.FLIGHT_ATC_FORM,
      function ($scope) {
        // List variable to help put all check boxes into `ng-model` array.
        $scope.atc_check_boxes = {};

        // Function to reset all ATC check boxes.
        $scope.reset_atc_check_boxes = function () {
          $("." + DOM_CLASS.FLIGHT_ONLINE_ATCS_CHECK_BOX).prop("checked",
            false);
        };

        // Listener for when `this.DOM_ID.FLIGHT_ATCS_FORM_MODAL` opened.
        $("#" + DOM_ID.FLIGHT_ATCS_FORM_MODAL).on(
          "show.bs.modal",
          function (event) {
            // PENDING: Please wait until HTTP request is finished.

            // Reset all check boxes.
            $scope.reset_atc_check_boxes();

            // Only checked back check boxes whom has its designated ATC online.
            for (var i = 0; i < selected_flight_online_atcs.length; i ++) {
              $("#" + DOM_ID.FLIGHT_ONLINE_ATC_CHECK_BOXES_ +
                selected_flight_online_atcs[i]).prop("checked", true);
            }
          }
        );
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