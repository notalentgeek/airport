var navbar_left = function (angularjs_app) {
  var init_count = 1; // Singleton.
  var instances = [];

  function create_instance () {
    var instance = new navbar_left(angularjs_app);
    return instance;
  }

  function navbar_left (angularjs_app) {
    var ANGULARJS_CONTROLLER = Object.freeze({
      ATC_MENU: "atc_menu"
    });

    var DOM_ID = Object.freeze({
      ATC_LIST_MODAL: "atc-list-modal",
      ATC_REGISTRATION_FORM_MODAL: "atc-registration-form-modal"
    });

    angularjs_app.controller(
      ANGULARJS_CONTROLLER.ATC_MENU,
      function ($scope) {
        $scope.show_atc_registration_form_modal = function () {
          show_bootstrap_modal("#" + DOM_ID.ATC_REGISTRATION_FORM_MODAL);
        };
        $scope.show_atc_list_modal = function () {
          show_bootstrap_modal("#" + DOM_ID.ATC_LIST_MODAL);
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