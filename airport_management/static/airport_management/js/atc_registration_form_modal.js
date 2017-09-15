var atc_registration_form_modal = function (angularjs_app) {
  var init_count = 1; // Singleton.
  var instances = [];

  function create_instance () {
    var instance = new atc_registration_form_modal(angularjs_app);
    return instance;
  }

  function atc_registration_form_modal (angularjs_app) {
    var ANGULARJS_CONTROLLER = Object.freeze({
      ATC_REGISTRATION_FORM: "atc-registration-form"
    });

    var DOM_ID = Object.freeze({
      ATC_CODE_INPUT: "atc-code-input",
      ATC_REGISTER_BUTTON: "atc-register-button"
    });

    var KEY = Object.freeze({
      ATC_CODE: "atc-code"
    });

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
  }

  return (function () {
    for (var i = 0; i < init_count; i ++) {
      if (!instances[i]) {
        instances.push(create_instance());
      }

      return instances[init_count - 1];
    }
  })();
};