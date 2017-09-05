// AngularJS controller to check if the `username` empty or has been registered.
app.controller("login_register_form", function ($http, $scope) {
  $scope.disable_register_button = true;
  $scope.disable_register_button_callback = function (value) {
    $scope.disable_register_button = value;
  }
  $scope.check_username_existence = function () {
    button_and_input_http_check(
      $scope.disable_register_button,
      "register-button",
      "username-input",
      $scope.username_input,
      $http,
      "btn-danger",
      "btn-primary",
      "username",
      "processing...",
      "username exists",
      "register",
      "server problem",
      $scope.disable_register_button_callback
    );
  };
});

// Just a simple controller ATC menu.
app.controller("atc_menu", function ($scope) {
  $scope.show_atc_form_modal = function () {
    $("#atc-form-modal").modal("show");
  };
  $scope.show_atc_list_modal = function () {
    $("#atc-list-modal").modal("show");
  };
});

/*
AngularJS controller to check if ATC code is already registered or not.
For the air traffic controller this application will only look for code. Thus,
the first name and the last name can be the existing ones unless the ATC code
is unique.
*/
app.controller("atc_register_form", function ($http, $scope) {
  $scope.disable_atc_register_button = true;
  $scope.disable_atc_register_button_callback = function (value) {
    /*
    If `value` is not `null` then it means this callback function was
    triggered from the HTTP request.
    */
    if (value !== null && value !== undefined) {
      $scope.disable_atc_register_button = value;
    }

    if (
      $scope.atc_register_form.atc_code_input.$valid &&
      $scope.atc_register_form.atc_first_name_input.$valid &&
      $scope.atc_register_form.atc_last_name_input.$valid &&
      !$scope.disable_atc_register_button
    ) {
      $scope.disable_atc_register_button = false;
    }
    else {
      $scope.disable_atc_register_button = true;
    }
  }
  $scope.check_atc_code_existence = function () {
    $scope.disable_atc_register_button = button_and_input_http_check(
      $scope.disable_atc_register_button,
      "atc-submit-button",
      "atc-code-input",
      $scope.atc_code_input,
      $http,
      "btn-danger",
      "btn-success",
      "atc_code",
      "processing...",
      "atc code exists",
      "register",
      "server problem",
      $scope.disable_atc_register_button_callback
    );
  };
});

// Function to automatically resize navigation bar components.
var auto_resize_navbar = function () {
  // Only resize navigation bar when there is no user logged in.
  if (document.getElementById("logout-form") === null) {
    if (document.documentElement.clientWidth < 935 &&
      document.documentElement.clientWidth >= 840) {
      document.getElementById("title").innerHTML = "airport...";
    }
    else if (document.documentElement.clientWidth < 840 &&
      document.documentElement.clientWidth >= 790) {
      document.getElementById("title").innerHTML = "...";
    }
    else if (document.documentElement.clientWidth < 790 &&
      document.documentElement.clientWidth > 767) {
      document.getElementById("title").innerHTML = ".";
    }
    else {
      document.getElementById("title").innerHTML = "airport management";
    }
  }
};

// Function to manually style ATC Form button according to view port.
var auto_style_atc_form_button = function () {
  var id_form = "atc-form-button";
  var id_list = "atc-list-button";
  var atc_form_button = document.getElementById(id_form);
  var atc_list_button = document.getElementById(id_list);

  /*
  `$("#" + id_form + ">button").length` is not used in this `if` statement
  because it is not always available. In case there is no user logged in it will
  be always return `false`.

  PENDING: A lot repetition here. A closure will be good.
  */
  if (
    document.documentElement.clientWidth < 768 &&
    $("#" + id_list + ">button").length == 0
  ) {
    if (atc_form_button) {
      atc_form_button.innerHTML = "";
      $(atc_form_button)
        .append("<button class='btn btn-block btn-default'>atc form</button>");
      $("#" + id_form + "-container").detach()
        .appendTo("#move-atc-menu-here-when-mobile");
    }

    atc_list_button.innerHTML = "";
    $(atc_list_button)
      .append("<button class='btn btn-block btn-default'>atcs list</button>");
    $("#" + id_list + "-container").detach()
      .appendTo("#move-atc-menu-here-when-mobile");

    document.getElementById("hide-atc-menu-when-mobile").style.display = "none";
  }
  else if (
    document.documentElement.clientWidth >= 768 &&
    $("#" + id_list + ">button").length > 0
  ) {
    if (atc_form_button) {
      atc_form_button.innerHTML = "atc form";
      $("#" + id_form + ">button").remove();
      $("#" + id_form + "-container").detach()
        .appendTo("#move-atc-menu-here-when-not-mobile");
    }

    atc_list_button.innerHTML = "atc list";
    $("#" + id_list + ">button").remove();
    $("#" + id_list + "-container").detach()
      .appendTo("#move-atc-menu-here-when-not-mobile");

    document.getElementById("hide-atc-menu-when-mobile").style.display = "";
  }
};

/*
Function to disable button for any cases in input field sent to server.
Components must be inside AngularJS controller.
*/
var button_and_input_http_check = function (
  disable,                      // Boolean to disable the button using
                                // `ng-disabled`.
  button_id,                    // The button's DOM id which we want to disable
                                // and enable accordingly.
  input_id,                     // The input's DOM id which used to determine if
                                // the `button` will be disabled or not.
  input_value,                  // The value from the element with `input_id` id.
  http,                         // `$http` application object from AngularJS.
  disable_class,                // CSS class used for the `button` if it is
                                // disabled.
  enable_class,                 // CSS class used for the `button` if it is
                                // enabled.
  param_name,                   // Parameter to be expected in the server.
  button_processing_string,     // The `button` string when `$http` is being
                                // processed.
  button_disabled_string,       // The `button` string when the returned value
                                // makes the `button` to be disabled.
  button_enabled_string,        // The `button` string when the returned value
                                // makes the `button` to be enabled.
  button_server_problem_string, // The `button` string when there is a server
                                // problem.
  callback                      // Function to call after successful HTTP call.
) {
  /*
  Keep the register button to be disabled. Only let the button to be enabled
  from this AngularJS controller.
  */
  disable = true;

  // Get access to necessary DOMs.
  var button = document.getElementById(button_id);
  var input = document.getElementById(input_id);

  // Check the availability of the mentioned DOMs.
  if (button && input) {
    // Get URL from the used DOMs attribute `param`.
    var url = input.getAttribute("param");

    // Make sure the input is not empty.
    if (input_value) {
      /*
      Set the button style when the before the HTTP request is being
      processed.
      */
      button.classList.remove(disable_class);
      button.classList.remove(enable_class);
      button.classList.add(disable_class);
      button.setAttribute("value", button_processing_string);

      // Begin the HTTP request.
      http_dict_params = {};
      http_dict_params[param_name] = input_value;
      http({
        method: "GET",
        params: http_dict_params,
        url: url
      }).then(function (data) {
        disable = string_to_bool(data.data);
        callback(disable);

        if (data.status === 200) {
          /*
          When the data returned is `true` (for example same username found
          in the table).
          */
          if (disable) {
            button.setAttribute("value", button_disabled_string);
          }
          // When the data returned is `false` (for example unique username).
          else {
            button.classList.remove(disable_class);
            button.classList.remove(enable_class);
            button.classList.add(enable_class);
            button.setAttribute("value", button_enabled_string);
          }
        }
        // If there is a server problem.
        else {
          button.setAttribute("value", button_server_problem_string);
        }
      });
    }
  }
};

// Check if wrong password UI is exists. If so, show wrong password modal.
var check_wrong_password_modal = (function () {
  // Modal for wrong password.
  var password_input = document.getElementById("password-input");

  if (password_input !== null) {
    if (string_to_bool(password_input.getAttribute("param"))) {
      $("#wrong-password-modal").modal("show");
    }
  }
})();

/*
Adjust the logout button for touch and non-touch browser. This is necessary
because the log out button has a hover event.
*/
var user_button = (function () {
  var user_button = document.getElementById("user-button");

  if (user_button !== null) {
    var user_button_width = user_button.offsetWidth;

    // Transfer variable value from DjangoTemplates.
    var user_name = user_button.getAttribute("param");
    user_name_12 = user_name.substring(0, 12 != -1 ? 12 : user_name.length);
    user_name = user_name.length > 12 ?  user_name_12 + "..." : user_name;

    /*
    Change the default `user_name` display, in case the `user_name` is
    longer than 12 characters!
    */
    user_button.setAttribute("value", "hello! " + user_name);

    // Adjust button for touch screen device.
    if (is_touch_device()) {
      user_button.classList.remove("btn-success");
      user_button.classList.add("btn-warning");
      user_button.setAttribute("value", "logout? " + user_name);
      user_button.style.width = user_button_width + "px";
    }
    // Non-touch screen display.
    else {
      user_button.addEventListener("mouseover", function () {
          user_button.classList.remove("btn-success");
        user_button.classList.add("btn-danger");
        user_button.setAttribute("value", "logout?");
        user_button.style.width = "285px";
      });
      user_button.addEventListener("mouseout", function () {
        user_button.classList.remove("btn-danger");
        user_button.classList.add("btn-success");
        user_button.setAttribute("value", "hello! " + user_name);
        user_button.style.width = "285px";
      });
    }
  }
})();