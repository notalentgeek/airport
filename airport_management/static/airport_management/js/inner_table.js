var inner_table = function () {
  var init_count = 1; // Singleton.
  var instances = [];

  function create_instance ()  {
    var instance = new inner_table();
    return instance;
  }

  function inner_table () {
    var DOM_CLASS = Object.freeze({
      HIDE_FOR_SMALL_WIDTH: "hide-for-small-width"
    });

    var VALUE = Object.freeze({
      // According to the need of when the table needs to be shrunk.
      WIDTH_THRESHOLD: 1000
    });

    // For small width (smaller than 1000 pixels) hide some columns.
    this.adjust_table = function () {
      if (document.documentElement.clientWidth <= VALUE.WIDTH_THRESHOLD) {
        $("." + DOM_CLASS.HIDE_FOR_SMALL_WIDTH).css("display", "none");
      }
      else {
        $("." + DOM_CLASS.HIDE_FOR_SMALL_WIDTH).css("display", "");        
      }
    };
  }

  return (function () {
    for (var i = 0; i < init_count; i ++) {
      if (!instances[i]) {
        instances.push(create_instance());
      }
    }

    return instances[instances.length - 1];
  })();
}