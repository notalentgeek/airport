// Angular controller to check if the `username` empty or has been registered.
app.controller("login_register_form", function ($scope, $http) {
  // Generally, disabled the register button until proper `username` is inputed.
  $scope.disabled = true;

  var register_button = document.getElementById("register-button");
  var username_input = document.getElementById("username-input");

  if (register_button !== null && username_input !== null) {
    $scope.check_user_existence = function () {
      var url = username_input.getAttribute("param");
      $scope.disabled = true;

      // Make sure the `username` is not empty.
      if ($scope.username_input) {
        // Set the button style to processing, while the HTTP request is going.
        register_button.classList.remove("btn-primary");
        register_button.classList.remove("btn-danger");
        register_button.classList.add("btn-primary");
        register_button.setAttribute("value", "processing...");

        $http({
          method: "GET",
          params: { "username": $scope.username_input },
          url: url
        }).then(function(data){
          $scope.disabled = string_to_bool(data.data);

          if (data.status === 200){
            // If the `username` found then change the button color to red.
            if ($scope.disabled) {
              register_button.classList.remove("btn-primary");
              register_button.classList.remove("btn-danger");
              register_button.classList.add("btn-danger");
              register_button.setAttribute("value", "username exists");
            }
            // If the `username` is new, enable the registration button.
            else {
              register_button.classList.remove("btn-primary");
              register_button.classList.remove("btn-danger");
              register_button.classList.add("btn-primary");
              register_button.setAttribute("value", "register");
            }
          }
          // In case of unresponsive server.
          else {
            $scope.disabled = false;
            register_button.classList.remove("btn-primary");
            register_button.classList.remove("btn-danger");
            register_button.classList.add("btn-primary");
            register_button.setAttribute("value", "server problem");
          }
        });
      }
    };
  }
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

  /* PENDING: A lot repetition here. A closure will be good. */
  if (
    document.documentElement.clientWidth < 768 &&
    $("#" + id_form + ">button").length == 0 &&
    $("#" + id_list + ">button").length == 0
  ) {
    atc_form_button.innerHTML = "";
    $(atc_form_button)
      .append("<button class='btn btn-block btn-default'>atc form</button>");

    atc_list_button.innerHTML = "";
    $(atc_list_button)
      .append("<button class='btn btn-block btn-default'>atcs list</button>");

    document.getElementById("hide-atc-menu-when-mobile").style.display = "none";
    $("#" + id_form + "-container").detach()
      .appendTo("#move-atc-menu-here-when-mobile");
    $("#" + id_list + "-container").detach()
      .appendTo("#move-atc-menu-here-when-mobile");
  }
  else if (
    document.documentElement.clientWidth >= 768 &&
    $("#" + id_form + ">button").length > 0 &&
    $("#" + id_list + ">button").length > 0
  ) {
    atc_form_button.innerHTML = "atc form";
    $("#" + id_form + ">button").remove();

    atc_list_button.innerHTML = "atc list";
    $("#" + id_list + ">button").remove();

    document.getElementById("hide-atc-menu-when-mobile").style.display = "";
    $("#" + id_form + "-container").detach()
      .appendTo("#move-atc-menu-here-when-not-mobile");
    $("#" + id_list + "-container").detach()
      .appendTo("#move-atc-menu-here-when-not-mobile");
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
        user_button.style.width = user_button_width + "px";
      });
      user_button.addEventListener("mouseout", function () {
        user_button.classList.remove("btn-danger");
        user_button.classList.add("btn-success");
        user_button.setAttribute("value", "hello! " + user_name);
        user_button.style.width = user_button_width + "px";
      });
    }
  }
})();