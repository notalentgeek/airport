/*
Function to disable button for any cases in input field sent to server.
Components must be inside AngularJS controller.
*/
var check_button_and_input_with_http = function (
  disable,                      // Boolean to disable the button using
                                // `ng-disabled`.
  button_id,                    // The button's DOM id which we want to disable
                                // and enable accordingly.
  input_id,                     // The input's DOM id which used to determine
                                // if the `button` will be disabled or not.
  url_id,                       // DOM element where URL resides in `param`
                                // attribute.
  input_value,                  // The value from the element with `input_id`
                                // id.
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
  var button_jquery_selector = "#" + button_id;
  var input_jquery_selector = "#" + input_id;
  var button = $(button_jquery_selector);
  var input = $(input_jquery_selector);

  // Check the availability of the mentioned DOMs.
  if (button.length && input.length) {

    // Get URL from the used DOMs attribute `param`.
    var url = dom_get_and_set.get_dom_param("#" + url_id);

    // Make sure the input is not empty.
    if (input_value) {
      /*
      Set the button style when the before the HTTP request is being
      processed.
      */
      button.removeClass(disable_class);
      button.removeClass(enable_class);
      button.addClass(disable_class);
      dom_get_and_set.set_dom_value(
        button_jquery_selector,
        button_processing_string
      );

      // The value that will be sent through HTTP "GET".
      http_dict_params = {};
      http_dict_params[param_name] = input_value;

      // Begin the HTTP request.
      http({
        method: "GET",
        params: http_dict_params,
        url: url
      }).then(function (data) {
        disable = string_operation.string_to_bool(data.data);
        callback(disable);

        if (data.status === 200) {
          /*
          When the data returned is `true` (for example same username found
          in the table).
          */
          if (disable) {
            dom_get_and_set.set_dom_value(
              button_jquery_selector,
              button_disabled_string
            );
          }
          // When the data returned is `false` (for example unique username).
          else {
            button.removeClass(disable_class);
            button.removeClass(enable_class);
            button.addClass(enable_class);
            dom_get_and_set.set_dom_value(
              button_jquery_selector,
              button_enabled_string
            );
          }
        }
        // If there is a server problem.
        else {
          dom_get_and_set.set_dom_value(
            button_jquery_selector,
            button_server_problem_string
          );
        }
      });
    }
  }

  return disable;
};