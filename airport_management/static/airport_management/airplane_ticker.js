// AngularJS controllers.
app.controller("flight_management_panel", function ($scope) {
  $scope.buttons = [
    {
      "bootstrap_color": "btn-success",
      "text": "submit"
    },
    {
      "bootstrap_color": "btn-warning",
      "text": "go to <br /> current flight"
    },
    {
      "bootstrap_color": "btn-primary",
      "text": "go to <br /> current flight"
    }
  ];
});

app.controller("table_arrivaldeparture_main", function ($scope, $compile) {
  $scope.arrival_pagination;
  $scope.departure_pagination;
  $scope.properties = [
    {
      "class": "arrival-table",
      "id": "pagination-arrival",
      "text": "arrival table"
    },
    {
      "class": "departure-table",
      "id": "pagination-departure",
      "text": "departure table"
    }
  ];
  $scope.test_text = "hello world";
  $scope.get_new_arrivaldeparture_pagination = function (page) {
    // Get the table later from here!
    console.log(page);
  };
  $scope.recompile_pagination = function () {
    $compile($scope.arrival_pagination)($scope);
    $compile($scope.departure_pagination)($scope);
  };
});

// Function to set the arrival and departure paginations.
var set_table_pagination_for_arrivaldeparture = function (pagination_id) {
  function click_and_init () {
    /*
    When a pagination button is pressed it will destroyed and created new
    one. These codes below are meant to adjust the width (based from
    percentage of the parent) based on how many paginations buttons are
    there.

    The next and previous buttons will always be 10% width of the parent.
    */
    var pagination = $(pagination_id);
    var pagination_children = pagination.children();

    for (var i = 0; i < pagination_children.length; i ++) {
      var li = $(pagination_children[i]);
      var li_children = li.children();

      for (var j = 0; j < li_children.length; j ++) {
        var a_or_span = $(li_children[j]);
        var a_page = parseInt($(a_or_span).html());

        /*
        This if statement is to make sure that inside `a_or_spane` is an `<a>`.
        If `a_page` returns a `NaN` then it is a `<span>` or an `<a>` for next
        or previous pagination. Since, only `<a>` that exactly point out to the
        next page will return an int.
        */
        if (a_page) {
          // Set attribute to access AngularJS controller.
          a_or_span.attr(
            "ng-click",
            "get_new_arrivaldeparture_pagination(" + a_page + ")"
          );
        }

        /*
        These codes below are to adjust whether the pagination buttons' width is
        fixed or dynamic. The fixed width is used for pagination buttons next
        and previous. The dynamically adjusted width is for pagination buttons
        that point to an exact pagination page.
        */
        if (a_or_span.hasClass("next") || a_or_span.hasClass("previous")) {
          li.addClass("pagination-fixed-width");
        }
        else {
          li.addClass("pagination-dynamic-width");
        }
      }
    }

    /*
    Adjust the width of all pagination buttons that are not next or previous.
    The `exact_pagination_buttons_count` is the total pagination buttons minus
    the next and previous buttons.
    */
    var exact_pagination_buttons_count = pagination_children.length - 2;

    /*
    The next and previous buttons always occupy 10% width from their parent. The
    other pagination buttons should occupy the max (100% - 20%) of the parent's
    width.
    */
    $(pagination_id + ">li.pagination-dynamic-width").css(
      "width", (80/exact_pagination_buttons_count) + "%");

    // Set all link to point to `"#"`.
    var as = $(pagination_id + ">li>a");
    as.attr("href", "#");

    /*
    Get the AngularJS controller for the pagination buttons. The `.element()`'s
    parameter for some reason cannot accept JQuery selector.
    */
    var scope_angularjs_controller = angular.element(
      document.getElementById("table-arrivaldeparture-main")).scope();

    // Re-compile/re-render AngularJS controller for the pagination buttons.
    scope_angularjs_controller.recompile_pagination();
  }

  return $(pagination_id).pagination({
      cssStyle: '',
      currentPage: 1,
      itemOnPage: 8,
      items: 20,
      nextText: '<span aria-hidden="true">&raquo;</span>',
      prevText: '<span aria-hidden="true">&laquo;</span>',
      onInit: function () {
        click_and_init();
      },
      onPageClick: function (page, event) {
        click_and_init();
      }
  });
};

// Function to initiated arrival and departure paginations.
$(function() {
  /*
  Get the reference to arrival pagination and departure pagination AngularJS
  controller.
  */
  var scope_angularjs_controller = angular.element(
    document.getElementById("table-arrivaldeparture-main")).scope();

  // Create the pagination and assign it to AngularJS controller's scope.
  scope_angularjs_controller.arrival_pagination =
    set_table_pagination_for_arrivaldeparture("#pagination-arrival");
  scope_angularjs_controller.departure_pagination =
    set_table_pagination_for_arrivaldeparture("#pagination-departure");

  // Re-compile/re-render the paginations.
  scope_angularjs_controller.recompile_pagination();
});