var dom_get_and_set = {
  get_dom_attribute: function (jquery_selector, attribute) {
    return $(jquery_selector).attr(attribute);
  },
  get_dom_param: function (jquery_selector) {
    return this.get_dom_attribute(jquery_selector, "param");
  },
  get_dom_value: function (jquery_selector) {
    return this.get_dom_attribute(jquery_selector, "value");
  },
  set_dom_attribute: function (jquery_selector, attribute, value) {
    return $(jquery_selector).attr(attribute, value);
  },
  set_dom_value: function (jquery_selector, value) {
    return this.set_dom_attribute(jquery_selector, "value", value);
  }
};

var angularjs_operation = {
  /*
  Get the AngularJS controller for the pagination buttons. The `.element()`'s
  parameter for some reason cannot accept JQuery selector.
  */
  get_angular_scope_by_dom_id: function (dom_id) {
    return angular.element(document.getElementById(dom_id)).scope();
  },
  recompile_dom_in_angularjs_scope: function (
    scope,
    angularjs_scope,
    compile
  ) {
    if (scope) {
      compile(scope.contents())(angularjs_scope);
    }
  }
};

var bootstrap_operation = {
  show_bootstrap_modal: function (jquery_selector) {
    $(jquery_selector).modal("show");
  }
};

var string_operation = {
  // Function to escape `RegExp` forbidden characters.
  escape_regexp: function (string) {
    return string.replace(/([.*+?^=!:${}()|\[\]\/\\])/g);
  },
  /*
  JavaScript `replace()` only replace once not all. This `replace_all()`
  function can be used similar to Python's replace.

  CAUTION: This function cannot replace special characters that are forbidden
  to use in RegularExpression. See `escape_regexp` to know those characters.
  */
  replace_all: function (string, find, replace) {
    return string.replace(new RegExp(this.escape_regexp(find), "g"), replace);
  },
  /*
  Limit string display from "long string" to "long str...". Use this because
  I do not understand how CSS ellipsis works.
  */
  string_overflow_ellipsis: function(string, limit, ellipsis_string) {
    if (!ellipsis_string) {
      ellipsis_string = "...";
    }
  
    if (ellipsis_string.length < string.length &&
      ellipsis_string.length < limit){
      string_reduced = string.substr(0, limit - ellipsis_string.length);
      string_ellipsed = string_reduced + ellipsis_string;
      return string > limit ? string_ellipsed : string;
    }
    return string;
  },
  string_to_bool: function (to_bool) {
    if (to_bool === null) {
      return false;
    }

    switch(to_bool.toLowerCase().trim()){
      case "1": case "true": case "yes": case "True": return true;
      case "0": case "false": case "no": case "False": return false;
      default: return Boolean(to_bool);
    }
  },
  // Convert string to list.
  string_to_list: function (string) {
    // If the inputted `string` is actually a list then return it directly.
    if (string.constructor === Array) {
      return string;
    }

    string = string.replace("[", "");
    string = string.replace("]", "");
    string = string_operation.replace_all(string, " ", "");

    return string.split(",");
  }
};

/*
Function to detect THE INITIAL device, whether it is a touch screen or
non-touch screen display.
*/
var is_touch_device = function () {
  return (("ontouchstart" in window)
    || (navigator.MaxTouchPoints > 0)
    || (navigator.msMaxTouchPoints > 0));
}