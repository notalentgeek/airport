var navbar_right = function (angularjs_app) {
  var init_count = 1; // Singleton.
  var instances;

  function create_instances () {
    var instance = new navbar(angularjs_app);
    return instance;
  }

  function navbar (angularjs_app) {
    var ANGULARJS_CONTROLLER = Object.freeze({
      LOGIN_AND_REGISTER_FORM: "login_and_register_form"
    });

    var DOM_ID = Object.freeze({
      AIRPORT_MANAGER_BUTTON_CONTAINER: "airport-manager-button-container",
      AIRPORT_MANAGER_NAME: "airport-manager-name",
      AIRPORT_MANAGER_NAME_INPUT: "airport-manager-name-input",
      AIRPORT_MANAGER_REGISTER_BUTTON: "airport-manager-register-button"
    });

    var JQUERY_SELECTOR = Object.freeze({
      AIRPORT_MANAGER_BUTTON: "#" + DOM_ID.AIRPORT_MANAGER_BUTTON_CONTAINER +
        ">.input"
    });

    var KEY = Object.freeze({
      AIRPORT_MANAGER_NAME: "airport-manager-name"
    });

    angularjs_app.controller(
      ANGULARJS_CONTROLLER.LOGIN_AND_REGISTER_FORM,
      function ($http, $scope) {
        $scope.disable_airport_manager_register_button = true;

        /*
        Function to check if airport manager name is already exists in database
        or not. This function executed as soon the value in the username input
        for airport manager is changed.
        */
        $scope.check_airport_manager_name_existence = function () {
          button_and_input_http_check(
            $scope.disable_airport_manager_register_button,
            DOM_ID.AIRPORT_MANAGER_REGISTER_BUTTON,
            DOM_ID.AIRPORT_MANAGER_NAME_INPUT,
            $scope.airport_manager_name_input, $http,
            "btn-danger", "btn-primary",
            KEY.AIRPORT_MANAGER_NAME,
            "processing...", "name exists", "register", "server problem",
            $scope.disable_airport_manager_register_button_callback
          );
        };

        // Callback function after HTTP request fulfilled.
        $scope.disable_airport_manager_register_button_callback = function (value) {
          $scope.disable_airport_manager_register_button = value;
        };
      }
    );

    return (function () {
      for (var i = 0; i < init_count; i ++) {
        if (!instances[i]) {
          instances[i] = create_instances();
        }

        return instances[init_count - 1];
      }
    })();
  }
}