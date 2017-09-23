var flight_lane_form_modal = function (angularjs_app) {
  var init_count = 1; // Singleton.
  var instances = [];

  function create_instance (angularjs_app) {
    var instance = new flight_lane_modal(angularjs_app);
    return instance;
  }

  function flight_lane_modal (angularjs_app) {
    var ANGULARJS_CONTROLLER = Object.freeze({
      FLIGHT_LANE_FORM: "flight_lane_form"
    });

    var DOM_ID = Object.freeze({
      FLIGHT_LANE_FORM_ARRIVALDEPARTURE: "flight-lane-form-arrivaldeparture",
      FLIGHT_LANE_FORM_FLIGHT_ID: "flight-lane-form-flight-id",
      FLIGHT_LANE_FORM_FLIGHT_LANE_ID: "flight-lane-form-flight-lane-id",
      FLIGHT_LANE_FORM_MODAL: "flight-lane-form-modal",
      FLIGHT_LANE_RADIO_: "flight-lane-radio-"
    });
    this.DOM_ID = DOM_ID;

    var JQUERY_SELECTOR_FOR_FORM = Object.freeze([
      "#" + DOM_ID.FLIGHT_LANE_FORM_ARRIVALDEPARTURE,
      "#" + DOM_ID.FLIGHT_LANE_FORM_FLIGHT_ID,
      "#" + DOM_ID.FLIGHT_LANE_FORM_FLIGHT_LANE_ID
    ]);

    var selected_arrivaldeparture;
    var selected_flight_id;
    var selected_flight_lane_id;

    var set_selected_flight_properties_to_variables = function (
      arrival_departure, flight_id, flight_lane) {
      selected_arrivaldeparture = arrival_departure;
      selected_flight_id = flight_id;
      selected_flight_lane_id = flight_lane;
    };

    var set_selected_flight_properties_to_dom = function (
      arrival_departure, flight_id, flight_lane) {
      values = [arrival_departure, flight_id, flight_lane];
      if (JQUERY_SELECTOR_FOR_FORM.length === values.length) {
        for (var i = 0; i < JQUERY_SELECTOR_FOR_FORM.length; i ++) {
          dom_get_and_set.set_dom_value(
            JQUERY_SELECTOR_FOR_FORM[i],
            values[i]
          );
        }
      }
    };

    this.set_selected_flight_properties = function (
      arrival_departure, flight_id, flight_lane) {
      set_selected_flight_properties_to_dom(arrival_departure, flight_id,
        flight_lane);
      set_selected_flight_properties_to_variables(arrival_departure,
        flight_id, flight_lane);
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
        selected_flight_lane_id] = values;
    })();

    angularjs_app.controller(
      ANGULARJS_CONTROLLER.FLIGHT_LANE_FORM,
      function ($scope) {       
        // Function to reset all ATC check boxes.
        $scope.reset_lane_radios = function () {
          $("." + DOM_CLASS.FLIGHT_ONLINE_ATCS_CHECK_BOX).prop("checked",
            false);
        };

        $("#" + DOM_ID.FLIGHT_LANE_FORM_MODAL).on(
          "show.bs.modal",
          function (event) {
            // PENDING: Please wait until HTTP request is finished.

            $("#" + DOM_ID.FLIGHT_LANE_RADIO_ +
              selected_flight_lane_id).prop("checked", true);
          }
        );
      }
    );
  }

  return (function () {
    for (var i = 0; i < init_count; i ++) {
      if (!instances[i]) {
        instances.push(create_instance(angularjs_app));
      }
    }

    return instances[instances.length - 1];
  })();
};