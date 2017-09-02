// AngularJS controllers.
app.controller("flight_management_panel", function ($scope) {
  $scope.buttons = [
    {
      "bootstrap_color": "btn-success",
      "text": "submit"
    },
    {
      "bootstrap_color": "btn-warning",
      "text": "go to <br /> next flight"
    },
    {
      "bootstrap_color": "btn-primary",
      "text": "go to <br /> current flight"
    }
  ];
});

app.controller("table_arrivaldeparture_main", function ($scope, $compile,
  $http) {
  $scope.arrival_pagination;
  $scope.departure_pagination;
  $scope.get_new_arrivaldeparture_table = function (
    arrival_or_departure_enum, page) {
    var id_partial, arrivaldeparture_pagination,
      recompile_arrivaldeparture_pagination;

    var url = document.getElementById("pagination-request-url")
      .getAttribute("param");

    if (arrival_or_departure_enum === AOD.ARRIVAL) {
      id_partial = "arrival";
      num_pages = arrival_num_pages;
      arrivaldeparture_pagination = $scope.arrival_pagination;
      recompile_arrivaldeparture_pagination =
        $scope.recompile_arrival_pagination;
    }
    else if (arrival_or_departure_enum === AOD.DEPARTURE) {
      id_partial = "departure";
      num_pages = departure_num_pages;
      arrivaldeparture_pagination = $scope.departure_pagination;
      recompile_arrivaldeparture_pagination =
        $scope.recompile_departure_pagination;
    }

    document.getElementById(id_partial + "-table-content").style.display =
      "none";
    document.getElementById(id_partial + "-table-request").style.display =
      "block";
    document.getElementById(id_partial + "-table-server-problem").style.display
      = "none";

    $http({
      method: "GET",
      params: {
        "page": page,
        "which_pagination": arrival_or_departure_enum
      },
      url: url
    }).then(function (data) {
      if (data.status === 200) {
        document.getElementById(id_partial + "-table-content")
          .style.display = "block";
        document.getElementById(id_partial + "-table-request")
          .style.display = "none";
        document.getElementById(id_partial + "-table-server-problem")
          .style.display = "none";

        $("#" + id_partial + "-table-content").html(data.data["html"]);
        auto_adjust_tables();

        if (data.data["num_pages"] != num_pages) {
          $("#pagination-" + id_partial).pagination("destroy");
            arrivaldeparture_pagination =
            set_table_pagination_for_arrivaldeparture(
              arrival_or_departure_enum,   // Enumeration for flights.
              "#pagination-" + id_partial, // ID for table pagination.
              data.data["num_pages"],      // Total pages for this pagination.
              page                         // Currently selected page.
            );
          recompile_arrivaldeparture_pagination();
        }
      }
      else {
        document.getElementById(id_partial + "-table-content")
          .style.display = "none";
        document.getElementById(id_partial + "-table-request")
          .style.display = "none";
        document.getElementById(id_partial + "-table-server-problem")
          .style.display = "block";
      }
    });
  };
  $scope.recompile_pagination = function () {
    $scope.recompile_arrival_pagination();
    $scope.recompile_departure_pagination();
  };
  $scope.recompile_arrival_pagination = function () {
    if ($scope.arrival_pagination) {
      $compile($scope.arrival_pagination.contents())($scope);
    }
  };
  $scope.recompile_departure_pagination = function () {
    if ($scope.departure_pagination) {
      $compile($scope.departure_pagination.contents())($scope);
    }
  };
});

var auto_adjust_tables = function () {
  if (document.documentElement.clientWidth <= 1000) {
    $(".td-hide-for-small-width").css("display", "none");
  }
  else {
    $(".td-hide-for-small-width").css("display", "");
  }
};

// Function to set the arrival and departure paginations.
var set_table_pagination_for_arrivaldeparture = function (
  arrival_or_departure_enum, pagination_id, num_pages, init_page) {
  // Set the default value for `init_page` to `1`.
  if (!init_page) {
    init_page = 1;
  }

  function click_and_init (current_page) {
    // Set the default value of `current_page` to `1`.
    if (!current_page) {
      current_page = 1;
    }

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
        var next_page =
          current_page + 1 > num_pages ? num_pages : current_page + 1;
        var previous_page = current_page - 1 < 1 ? 1 : current_page - 1;

        /*
        This if statement is to make sure that inside `a_or_spane` is an `<a>`.
        If `a_page` returns a `NaN` then it is a `<span>` or an `<a>` for next
        or previous pagination. Since, only `<a>` that exactly point out to the
        next page will return an int.
        */
        if (a_page && !li.hasClass("active")) {
          // Set attribute to access AngularJS controller.
          a_or_span.attr(
            "ng-click",
            "get_new_arrivaldeparture_table(" + arrival_or_departure_enum +
              ", " + a_page + ")"
          );
        }
        /*
        This is meant for the next and previous button to trigger the pagination
        request AJAX.
        */
        else if (!a_page && !li.hasClass("active")) {
          if (a_or_span.hasClass("next")) {
            a_or_span.attr(
              "ng-click",
              "get_new_arrivaldeparture_table(" + arrival_or_departure_enum +
                ", " + next_page + ")"
            );
          }
          else if (a_or_span.hasClass("prev")) {
            a_or_span.attr(
              "ng-click",
              "get_new_arrivaldeparture_table(" + arrival_or_departure_enum +
                ", " + previous_page + ")"
            );
          }
        }

        /*
        These codes below are to adjust whether the pagination buttons' width is
        fixed or dynamic. The fixed width is used for pagination buttons next
        and previous. The dynamically adjusted width is for pagination buttons
        that point to an exact pagination page.
        */
        if (a_or_span.hasClass("next") || a_or_span.hasClass("prev")) {
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

    PENDING: `scope_angularjs_controller` is duplicated, perhaps make it as a
    function to put value to AngularJS controller?
    */
    var scope_angularjs_controller = angular.element(
      document.getElementById("table-arrivaldeparture-main")).scope();

    /*
    Re-compile/re-render AngularJS controller for the pagination buttons. Please
    compile it accordingly (do not re-compile all AngularJS controllers) to
    prevent shadow DOMs.
    */
    if (arrival_or_departure_enum === AOD.ARRIVAL) {
      scope_angularjs_controller.recompile_arrival_pagination();
    }
    else if (arrival_or_departure_enum === AOD.DEPARTURE) {
      scope_angularjs_controller.recompile_departure_pagination();
    }
  }

  return $(pagination_id).pagination({
      arrival_or_departure: arrival_or_departure_enum,
      cssStyle: "",
      currentPage: init_page,
      itemOnPage: 8,
      items: num_pages,
      nextText: '<span aria-hidden="true">&raquo;</span>',
      prevText: '<span aria-hidden="true">&laquo;</span>',
      onInit: function () {
        click_and_init();
      },
      onPageClick: function (page, event) {
        click_and_init(page);
      }
  });
};