var airport_manager_wrong_password_modal = function (angularjs_app) {
  var init_count = 1; // Singleton.
  var instances = [];

  function create_instance () {
    var instance = new airport_manager_wrong_password_modal(angularjs_app);
    return instance;
  }

  function airport_manager_wrong_password_modal () {
    this.DOM_ID = Object.freeze({
      AIRPORT_MANAGER_WRONG_PASSWORD: "airport-manager-wrong-password",
      AIRPORT_MANAGER_WRONG_PASSWORD_MODAL:
        "airport-manager-wrong-password-modal"
    });
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