var navbar_right = function (angularjs_app) {
  var init_count = 1; // Singleton.
  var instances = [];

  function create_instance () {
    var instance = new navbar_right(angularjs_app);
    return instance;
  }

  function navbar_right (angularjs_app) {
    var ANGULARJS_CONTROLLER = Object.freeze({
      AIRPORT_MANAGER_LOGIN_AND_REGISTRATION_FORM:
        "airport_manager_login_and_registration_form"
    });

    var DOM_ID = Object.freeze({
      AIRPORT_MANAGER_BUTTON_CONTAINER: "airport-manager-button-container",
      AIRPORT_MANAGER_NAME: "airport-manager-name",
      AIRPORT_MANAGER_NAME_INPUT: "airport-manager-name-input",
      AIRPORT_MANAGER_REGISTER_BUTTON: "airport-manager-register-button",
      CHECK_AIRPORT_MANAGER_NAME_EXISTENCE_URL:
        "check-airport-manager-name-existence-url"
    });

    var JQUERY_SELECTOR = Object.freeze({
      AIRPORT_MANAGER_BUTTON: "#" + DOM_ID.AIRPORT_MANAGER_BUTTON_CONTAINER +
        ">input"
    });
    this.JQUERY_SELECTOR = JQUERY_SELECTOR;

    var KEY = Object.freeze({
      AIRPORT_MANAGER_NAME: "airport_manager_name"
    });

    this.adjust_airport_manager_button = function () {
      var CSS_VALUE = Object.freeze({
        WIDTH_FULL: "100%",
        WIDTH_NORMAL: "285px"
      });

      var STRING = Object.freeze({
        LOGGED_IN: "hello! ",
        LOGOUT: "logout? "
      });

      var airport_manager_button_jquery_selector =
        JQUERY_SELECTOR.AIRPORT_MANAGER_BUTTON;
      var airport_manager_button = $(airport_manager_button_jquery_selector);
      var airport_manager_name = dom_get_and_set.get_dom_param("#" +
        DOM_ID.AIRPORT_MANAGER_NAME);

      /*
      Check if airport manager button exists and airport manager name can be
      retrieved.
      */
      if (airport_manager_button.length && airport_manager_name) {
        /*
        Shorten the airport manager name into 12 characters with three dots as
        prefix. Then, check if the total characters in airport manager name is
        larger than 15 or not. If the total characters is larger than 15 then
        use the shortened name. If not then keep using the original un-shortened
        name.
        */
        airport_manager_name = string_operation.string_overflow_ellipsis(
          airport_manager_name,
          15
        );

        // Change the airport display name in the view.
        dom_get_and_set.set_dom_value(airport_manager_button_jquery_selector,
          STRING.LOGGED_IN + airport_manager_name);

        /*
        Adjust this button for touch device. `is_touch_device()` check, after
        the web application is fully rendered, if the web browser supports touch
        input or not.
        */
        if (is_touch_device()) {
          airport_manager_button.removeClass("btn-success");
          airport_manager_button.addClass("btn-warning");
          dom_get_and_set.set_dom_value(airport_manager_button_jquery_selector,
            STRING.LOGOUT + airport_manager_name);
        }
        else {
          /*
          Because JQuery selector return a list of DOMs and since the airport
          button manager should be unique, we take the first index.
          */
          airport_manager_button[0].addEventListener("mouseout", function () {
            airport_manager_button.removeClass("btn-danger");
            airport_manager_button.addClass("btn-success");
            dom_get_and_set.set_dom_value(
              airport_manager_button_jquery_selector,
              STRING.LOGGED_IN + airport_manager_name
            );
          });
          airport_manager_button[0].addEventListener("mouseover", function () {
            airport_manager_button.removeClass("btn-success");
            airport_manager_button.addClass("btn-danger");
            dom_get_and_set.set_dom_value(
              airport_manager_button_jquery_selector,
              STRING.LOGOUT + airport_manager_name
            );
          });
        }
      }
    };

    angularjs_app.controller(
      ANGULARJS_CONTROLLER.AIRPORT_MANAGER_LOGIN_AND_REGISTRATION_FORM,
      function ($http, $scope) {
        $scope.disable_airport_manager_register_button = true;

        /*
        Function to check if airport manager name is already exists in database
        or not. This function executed as soon the value in the username input
        for airport manager is changed.
        */
        $scope.check_airport_manager_name_existence = function () {
          check_button_and_input_with_http(
            $scope.disable_airport_manager_register_button,
            DOM_ID.AIRPORT_MANAGER_REGISTER_BUTTON,
            DOM_ID.AIRPORT_MANAGER_NAME_INPUT,
            DOM_ID.CHECK_AIRPORT_MANAGER_NAME_EXISTENCE_URL,
            $scope.airport_manager_name_input, $http,
            "btn-danger", "btn-primary",
            KEY.AIRPORT_MANAGER_NAME,
            "processing...", "name exists", "register", "server problem",
            $scope.disable_airport_manager_register_button_callback
          );
        };

        // Callback function after HTTP request fulfilled.
        $scope.disable_airport_manager_register_button_callback =
          function (value) {
            $scope.disable_airport_manager_register_button = value;
          };
      }
    );
  };

  return (function () {
    for (var i = 0; i < init_count; i ++) {
      if (!instances[i]) {
        instances.push(create_instance());
      }

      return instances[init_count - 1];
    }
  })();
};