var atc_list_modal = function (angularjs_app) {
  var init_count = 1; // Singleton.
  var instances = [];

  function create_instance () {
    var instance = new atc_list_modal(angularjs_app);
    return instance;
  }

  function atc_list_modal (angularjs_app) {
    this.DOM_ID = Object.freeze({
      MODAL_BUTTON: "atc-list-modal-button",
      MODAL_BUTTON_CONTAINER: "atc-list-modal-button-container"
    });

    this.STRING = Object.freeze({
      MODAL_BUTTON_TEXT: "atc list"
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