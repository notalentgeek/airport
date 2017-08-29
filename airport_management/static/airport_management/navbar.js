// Angular controller to check if the `username` empty or has been registered.
app.controller("login_register_form", function ($scope, $http) {
  // Generally, disabled the register button until proper `username` is inputed.
  $scope.disabled = true;

  var register_button = document.getElementById("register_button");
  var username_input = document.getElementById("username_input");

  if (register_button !== null && username_input !== null) {
    var url = username_input.getAttribute("param");

    $scope.check_user_existence = function () {
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
        });
      }
    };
  }
});

// Function to automatically resize navigation bar components.
var auto_resize_navbar = function (){
  if (document.documentElement.clientWidth < 935 &&
    document.documentElement.clientWidth >= 840) {
    document.getElementById("title").innerHTML = "airport...";
    document.getElementById("atc_form_button").innerHTML = "atc form";
  }
  else if (document.documentElement.clientWidth < 840 &&
    document.documentElement.clientWidth >= 790) {
    document.getElementById("title").innerHTML = "...";
    document.getElementById("atc_form_button").innerHTML = "atc form";
  }
  else if (document.documentElement.clientWidth < 790 &&
    document.documentElement.clientWidth >= 768) {
    document.getElementById("title").innerHTML = "";
    document.getElementById("atc_form_button").innerHTML = "atc...";
  }
  else {
    document.getElementById("title").innerHTML = "airport management";
    document.getElementById("atc_form_button").innerHTML = "atc form";
  }
};

// Check if wrong password UI is exists. If so, show wrong password modal.
var check_wrong_password_modal = (function () {
  // Modal for wrong password.
  var password_input = document.getElementById("password_input");

  if (password_input !== null) {
    if (string_to_bool(password_input.getAttribute("param"))) {
      $("#wrong_password_modal").modal("show");
    }
  }
})();

/*
Adjust the logout button for touch and non-touch browser. This is necessary
because the log out button has a hover event.
*/
var user_button = (function () {
  var user_button = document.getElementById("user_button");

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

// Adjust the string in the navigation bar.
window.onload = auto_resize_navbar();

/*
Adding fix to the title "ellipse" when the view port is below 855 pixels but
still above 769 pixels (before the burger button shows)
*/
window.addEventListener("resize", function () {
  auto_resize_navbar();
});