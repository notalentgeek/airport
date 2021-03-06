var navbar_left = function (
  angularjs_app,
  airport_manager_button_jquery_selector,
  atc_modals
) {
  var init_count = 1; // Singleton.
  var instances = [];

  function create_instance () {
    var instance = new navbar_left(
      angularjs_app,
      airport_manager_button_jquery_selector,
      atc_modals
    );
    return instance;
  }

  function navbar_left (
    angularjs_app,
    airport_manager_button_jquery_selector,
    atc_modals
  ) {
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

    var STRING = Object.freeze({
      TITLE_STRING: ["airport_management", "airport...", "...", "."]
    });

    var VALUE = Object.freeze({
      // According to when the `TITLE_STRING` collapse.
      WIDTH_THRESHOLD: [935, 840, 790, 767]
    });

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

      if (atc_modals) {
        for (var i = 0; i < atc_modals.length; i ++) {
          if ($("#" + atc_modals[i].DOM_ID.MODAL_BUTTON_CONTAINER).length)
          {
            adjust_atc_modal_buttons_(
              is_mobile_resolution ? true : false,
              atc_modals[i].DOM_ID.MODAL_BUTTON,
              atc_modals[i].DOM_ID.MODAL_BUTTON_CONTAINER,
              is_mobile_resolution ?
                DOM_ID.MOBILE_ATC_MODALS_BUTTONS_CONTAINER :
                DOM_ID.NON_MOBILE_ATC_MODALS_BUTTONS_CONTAINER,
              atc_modals[i].STRING.MODAL_BUTTON_TEXT
            );
          }
        }
      }
    };

    this.adjust_title = function () {
      // Only resize the navigation bar when there is no user logged in.
      if (!$(airport_manager_button_jquery_selector).length) {
        if (
          document.documentElement.clientWidth < VALUE.WIDTH_THRESHOLD[0] &&
          document.documentElement.clientWidth >= VALUE.WIDTH_THRESHOLD[1]
        ) {
          $(airport_manager_button_jquery_selector).html(
            STRING.TITLE_STRING[1]);
        }
        else if (
          document.documentElement.clientWidth < VALUE.WIDTH_THRESHOLD[1] &&
          document.documentElement.clientWidth >= VALUE.WIDTH_THRESHOLD[2]
        ) {
          $(airport_manager_button_jquery_selector).html(
            STRING.TITLE_STRING[2]);          
        }
        else if (
          document.documentElement.clientWidth < VALUE.WIDTH_THRESHOLD[2] &&
          document.documentElement.clientWidth >= VALUE.WIDTH_THRESHOLD[3]
        ) {
          $(airport_manager_button_jquery_selector).html(
            STRING.TITLE_STRING[3]);          
        }
        else {
          $(airport_manager_button_jquery_selector).html(
            STRING.TITLE_STRING[0]);
        }
      }
    };

    angularjs_app.controller(
      ANGULARJS_CONTROLLER.ATC_MENU,
      function ($scope) {
        $scope.show_atc_registration_form_modal = function () {
          bootstrap_operation.show_bootstrap_modal(
            "#" + DOM_ID.ATC_REGISTRATION_FORM_MODAL
          );
        };
        $scope.show_atc_list_modal = function () {
          bootstrap_operation.show_bootstrap_modal(
            "#" + DOM_ID.ATC_LIST_MODAL
          );
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