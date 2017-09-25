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
      ATC_REGISTRATION_BUTTON: "atc-registration-button",
      CHECK_ATC_CODE_EXISTENCE_URL: "check-atc-code-existence-url",
      MODAL_BUTTON: "atc-registration-form-modal-button",
      MODAL_BUTTON_CONTAINER: "atc-registration-form-modal-button-container"
    });
    this.DOM_ID = DOM_ID;

    var KEY = Object.freeze({
      ATC_CODE: "atc_code"
    });

    this.STRING = Object.freeze({
      MODAL_BUTTON_TEXT: "atc registration form"
    });

    angularjs_app.controller(
      ANGULARJS_CONTROLLER.ATC_REGISTRATION_FORM,
      function ($http, $scope) {
        $scope.disable_atc_register_button = true;

        $scope.check_atc_code_existence = function () {
          $scope.disable_atc_register_button =
            check_button_and_input_with_http(
              $scope.disable_atc_register_button,
              DOM_ID.ATC_REGISTRATION_BUTTON,
              DOM_ID.ATC_CODE_INPUT,
              DOM_ID.CHECK_ATC_CODE_EXISTENCE_URL,
              $scope.atc_code_input, $http,
              "btn-danger", "btn-primary",
              KEY.ATC_CODE,
              "processing...", "atc code exists", "register", "server problem",
              $scope.disable_atc_register_button_callback
            );
        };

        // Callback function after HTTP request fulfilled.
        $scope.disable_atc_register_button_callback = function (value) {
          if (value !== null && value !== undefined) {
            $scope.disable_atc_register_button = value;
          }

          var ng_models_is_valid = (
            $scope.atc_registration_form.atc_code_input.$valid &&
            $scope.atc_registration_form.atc_first_name_input.$valid &&
            $scope.atc_registration_form.atc_last_name_input.$valid
          );

          /*
          If `value` is not `null` then it means this callback function was
          triggered from the HTTP request.
          */
          if (ng_models_is_valid && !$scope.disable_atc_register_button) {
            $scope.disable_atc_register_button = false;
          }
          else {
            $scope.disable_atc_register_button = true;
          }
        };

        // Reset ATC form.
        $scope.reset_atc_registration_form = function () {
          $scope.atc_registration_form.atc_code_input = "";
          $scope.atc_registration_form.atc_first_name_input = "";
          $scope.atc_registration_form.atc_last_name_input = "";
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