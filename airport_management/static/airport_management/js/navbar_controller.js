// AngularJS controllers.

/*
AngularJS controller to check if the value in
`CSS.AIRPORT_MANAGER_USERNAME_INPUT` is empty or exists in the database.
*/
app.controller(
  CONTROLLER_STRING.LOGIN_AND_REGISTER_FORM,
  function ($http, $scope) {
    $scope.disable_airport_manager_register_button = true;

    // Callback function after HTTP request finished.
    $scope.disable_airport_manager_register_button_callback =
      function (value) {
        $scope.disable_airport_manager_register_button = value;
      };

    /*
    Function to check if airport manager name is already exists in database or
    not.
    */
    $scope.check_airport_manager_name_existstence = function () {
      button_and_input_http_check(
        $scope.disable_airport_manager_register_button,
        CSS.AIRPORT_MANAGER_REGISTER_BUTTON_ID,
        CSS.AIRPORT_MANAGER_NAME_INPUT_ID,
        $scope.airport_manager_name_input,
        $http,
        "btn-danger",
        "btn-primary",
        KEY.AIRPORT_MANAGER_NAME,
        "processing...",
        "name exists",
        "register",
        "server problem",
        $scope.disable_airport_manager_register_button_callback
      );
    };
  }
);

// Simple ANgularJS controller for the ATC menu in the navigation bar.
app.controller(CONTROLLER_STRING.ATC_MENU, function ($scope) {
  $scope.show_atc_form_modal = function () {
    $("#" + CSS.ATC_FORM_MODAL_ID).modal("show");
  };
  $scope.show_atc_list_modal = function () {
    $("#" + CSS.ATC_LIST_MODAL_ID).modal("show");
  };
});

/*
AngularJS controller to check if ATC code is already registered or not.
For the air traffic controller this application will only look for code. Thus,
the first name and the last name can be the existing ones unless the ATC code
is unique.
*/
app.controller(
  CONTROLLER_STRING.ATC_FORM,
  function ($http, $scope) {
    $scope.disable_atc_register_button = true;
    $scope.disable_atc_register_button_callback = function (value) {
      /*
      If `value` is not `null` then it means this callback function was
      triggered from the HTTP request.
      */
      if (value !== null && value !== undefined) {
        $scope.disable_atc_register_button = value;
        if (
          $scope.atc_form.atc_form_code_input.$valid &&
          $scope.atc_form.atc_form_first_name_input.$valid &&
          $scope.atc_form.atc_form_last_name_input.$valid &&
          !$scope.disable_atc_register_button // The difference.
        ) {
          $scope.disable_atc_register_button = false;
        }
        else {
          $scope.disable_atc_register_button = true;
        }
      }
      else {
        if (
          $scope.atc_form.atc_form_code_input.$valid &&
          $scope.atc_form.atc_form_first_name_input.$valid &&
          $scope.atc_form.atc_form_last_name_input.$valid
        ) {
          $scope.disable_atc_register_button = false;
        }
        else {
          $scope.disable_atc_register_button = true;
        }
      }
    };
    $scope.check_atc_code_existence = function () {
      $scope.disable_atc_register_button = button_and_input_http_check(
        $scope.disable_atc_register_button,
        CSS.ATC_FORM_REGISTER_BUTTON_ID,
        CSS.ATC_FORM_CODE_INPUT_ID,
        $scope.atc_form_code_input,
        $http,
        "btn-danger",
        "btn-success",
        KEY.ATC_CODE,
        "processing...",
        "atc code exists",
        "register",
        "server problem",
        $scope.disable_atc_register_button_callback
      );
    };
    $scope.reset_values = function () {
      $scope.atc_form_code_input = "";
      $scope.atc_form_first_name_input = "";
      $scope.atc_form_last_name_input = "";
    };
  }
);