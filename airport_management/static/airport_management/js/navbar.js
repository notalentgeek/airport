var navbar = function (angularjs_app) {
  var init_count = 1; // Singleton.
  var instances;

  function create_instances () {
    var instance = new navbar(angularjs_app);
    return instance;
  }

  function navbar (angularjs_app) {
    var ANGULARJS_CONTROLLER = Object.freeze({
      ATC_REGISTRATION_FORM: "atc-registration-form",
      ATC_MENU: "atc_menu",
      LOGIN_AND_REGISTER_FORM: "login_and_register_form"
    });

    var DOM_ID = Object.freeze({
      AIRPORT_MANAGER_NAME_INPUT: "airport-manager-name-input",
      AIRPORT_MANAGER_REGISTER_BUTTON: "airport-manager-register-button",
      ATC_CODE_INPUT: "atc-code-input",
      ATC_LIST_MODAL: "atc-list-modal",
      ATC_REGISTER_BUTTON: "atc-register-button",
      ATC_REGISTRATION_FORM_MODAL: "atc-registration-form-modal"
    });

    var KEY = Object.freeze({
      AIRPORT_MANAGER_NAME: "airport-manager-name",
      ATC_CODE: "atc-code"
    });

    var show_bootstrap_modal = function (jquery_selector) {
      $(jquery_selector).modal("show");
    }

    angularjs_app.controller(
      ANGULARJS_CONTROLLER.ATC_REGISTRATION_FORM,
      function ($http, $scope) {
        $scope.disable_atc_register_button = true;

        $scope.check_atc_code_existence = function () {
          button_and_input_http_check(
            $scope.disable_atc_register_button,
            DOM_ID.ATC_REGISTER_BUTTON,
            DOM_ID.ATC_CODE_INPUT,
            $scope.atc_code_input, $http,
            "btn-danger", "btn-primary",
            KEY.ATC_CODE,
            "processing...", "atc code exists", "register", "server problem",
            $scope.disable_atc_register_button_callback
          );
        };

        // Callback function after HTTP request fulfilled.
        $scope.disable_atc_register_button_callback = function (value) {
          var ng_models_is_valid = (
            $scope.ATC_REGISTRATION_FORM.atc_code_input.$valid &&
            $scope.ATC_REGISTRATION_FORM.atc_first_name_input.$valid &&
            $scope.ATC_REGISTRATION_FORM.atc_last_name_input.$valid
          );

          /*
          If `value` is not `null` then it means this callback function was
          triggered from the HTTP request.
          */
          if ((Boolean(value) ? true : false) && ng_models_is_valid) {
            $scope.disable_atc_register_button = false;
          }
          else {
            $scope.disable_atc_register_button = true;
          }
        };

        // Reset ATC form.
        $scope.reset_ATC_REGISTRATION_FORM = function () {
          $scope.ATC_REGISTRATION_FORM.atc_code_input = "";
          $scope.ATC_REGISTRATION_FORM.atc_first_name_input = "";
          $scope.ATC_REGISTRATION_FORM.atc_last_name_input = "";
        };
      }
    );

    angularjs_app.controller(
      ANGULARJS_CONTROLLER.ATC_MENU,
      function ($scope) {
        $scope.show_ATC_REGISTRATION_FORM_modal = function () {
          show_bootstrap_modal("#" + DOM_ID.ATC_REGISTRATION_FORM_MODAL);
        };
        $scope.show_ATC_REGISTRATION_FORM_list = function () {
          show_bootstrap_modal("#" + DOM_ID.ATC_REGISTRATION_FORM_LIST);
        };
      }
    );

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