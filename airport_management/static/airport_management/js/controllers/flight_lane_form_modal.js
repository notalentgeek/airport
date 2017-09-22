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

    angularjs_app.controller(
      ANGULARJS_CONTROLLER.FLIGHT_LANE_FORM,
      function ($scope) {
        
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