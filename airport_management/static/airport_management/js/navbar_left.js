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
      ATC_MODALS_BUTTONS_DROPDOWN: "atc-modals-buttons-dropdown",
      ATC_REGISTRATION_FORM_MODAL: "atc-registration-form-modal",
      MOBILE_ATC_MODALS_BUTTONS_CONTAINER:
        "mobile-atc-modals-buttons-container",
      NON_MOBILE_ATC_MODALS_BUTTONS_CONTAINER:
        "non-mobile-atc-modals-buttons-container"
    });

    this.atc_modals;

    this.adjust_atc_modal_buttons = function () {
      // Closure.
      var adjust_atc_modal_buttons_ = function (
        is_mobile, button_id, button_container_id,
        button_container_moved_id, button_text) {
        if (is_mobile) {
          $("#" + button_id).empty();
          $("#" + button_id).append(
            "<button class='btn btn-block btn-default'>" + button_text +
            "</button>");
          $("#" + DOM_ID.ATC_MODALS_BUTTONS_DROPDOWN).css("display", "none");
        }
        else {
          $("#" + button_id).html(button_text);
          $("#" + button_id + ">button").remove();
          $("#" + DOM_ID.ATC_MODALS_BUTTONS_DROPDOWN).css("display", "");
        }
        $("#" + button_container_id).detach()
          .appendTo("#" + button_container_moved_id);
      };

      // Check if the current view port rendered as a mobile view.
      var is_mobile_resolution = document.documentElement.clientWidth < 768;

      if (this.atc_modals) {
        for (var i = 0; i < this.atc_modals.length; i ++) {
          if ($("#" + this.atc_modals[i].DOM_ID.MODAL_BUTTON_CONTAINER).length)
          {
            adjust_atc_modal_buttons_(
              is_mobile_resolution ? true : false,
              this.atc_modals[i].DOM_ID.MODAL_BUTTON,
              this.atc_modals[i].DOM_ID.MODAL_BUTTON_CONTAINER,
              is_mobile_resolution ?
                DOM_ID.MOBILE_ATC_MODALS_BUTTONS_CONTAINER :
                DOM_ID.NON_MOBILE_ATC_MODALS_BUTTONS_CONTAINER,
              this.atc_modals[i].STRING.MODAL_BUTTON_TEXT
            );
          }
        }
      }
    };

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