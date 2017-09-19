var airport_manager_wrong_password_modal = function (angularjs_app) {
  var init_count = 1; // Singleton.
  var instances = [];

  function create_instance () {
    var instance = new airport_manager_wrong_password_modal(angularjs_app);
    return instance;
  }

  function airport_manager_wrong_password_modal () {
    var DOM_ID = Object.freeze({
      AIRPORT_MANAGER_WRONG_PASSWORD: "airport-manager-wrong-password",
      AIRPORT_MANAGER_WRONG_PASSWORD_MODAL:
        "airport-manager-wrong-password-modal"
    });
    this.DOM_ID = DOM_ID;

    this.check_wrong_password = function () {
      var airport_manager_wrong_password  =
        $("#" + DOM_ID.AIRPORT_MANAGER_WRONG_PASSWORD);
      
      // Make sure that the wrong password message is received form the server.
      if (airport_manager_wrong_password.length) {
        var password_was_wrong = string_operation.string_to_bool(
          dom_get_and_set.get_dom_param(
            "#" + DOM_ID.AIRPORT_MANAGER_WRONG_PASSWORD
          )
        );
    
        //If password is wrong then show the wrong password modal.
        if (password_was_wrong) {
          bootstrap_operation.show_bootstrap_modal(
            "#" + DOM_ID.AIRPORT_MANAGER_WRONG_PASSWORD_MODAL
          );
        }
      }
    };
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