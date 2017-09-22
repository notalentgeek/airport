// Create pagination HTML.
var create_pagination_for_arrivaldeparture_table = function (
  table_aod,
  table_dom_class,
  table_dom_id,
  aod,
  pagination_id,
  number_of_pages,
  requested_page
) {
  // If `requested_page` is not provided then set it to `1`.
  if (!requested_page) {
    requested_page = 1;
  }

  // Function for when the pagination button is clicked or initiated.
  function click_and_init (current_page) {
    if (!current_page) {
      current_page = 1;
    }

    /*
    When a pagination button is pressed it will destroyed and created new
    one (this basic behavior from the library). These codes below are meant to
    adjust the width (based from percentage of the parent) based on how many
    paginations buttons are there.

    The next and previous buttons will always be 10% width of the parent.
    */

    var pagination = $("#" + pagination_id);
    var pagination_children = pagination.children();

    // The next page.
    var next_page = current_page + 1 > number_of_pages ?
      number_of_pages : current_page + 1;

    // The previous page.
    var previous_page = current_page - 1 < 1 ?
      number_of_pages : current_page - 1;

    for (var i = 0; i < pagination_children.length; i ++) {
      var li = $(pagination_children[i]);
      var li_children = li.children();

      for (var j = 0; j < li_children.length; j ++) {
        var a_or_span = $(li_children[j]);
        var a_page = isNaN(parseInt($(a_or_span).html())) ? null : parseInt(
          $(a_or_span).html());

        /*
        This if statement is to make sure that inside `a_or_spane` is an
        `<a>`. If `a_page` returns a `NaN` then it is a `<span>` or an `<a>`
        for next or previous buttons. Since, only `<a>` that exactly point out
        to the next page will return an int.
        */
        if (a_page || a_or_span.hasClass(table_dom_class.CLICKABLE)) {
          // Pagination page buttons have dynamic width.
          li.addClass(table_dom_class.PAGINATION_BUTTON_DYNAMIC_WIDTH);

          /*
          Only add `ng-click` controller to pagination buttons with number on
          it.
          */
          if (a_page) {
            a_or_span.attr(
              "ng-click",
              "pagination_requests_flight_table(" + aod + ", " + a_page + ")"
            );
          }
        }
        /*
        This is meant for the next and previous button to trigger the
        pagination request AJAX.
        */
        else if (!a_page) {
          /*
          Pagination next and previous buttons always have 10% width of their
          parent.
          */
          li.addClass(table_dom_class.PAGINATION_BUTTON_FIXED_WIDTH);

          // Adjust the `ng-click`.
          if (a_or_span.hasClass("next")) {
            a_or_span.attr(
              "ng-click",
              "pagination_requests_flight_table(" + aod + ", " + 
                next_page + ")"
            );
          }
          else if (a_or_span.hasClass("prev")) {
            li.addClass("pagination-button-fixed-width");
            a_or_span.attr(
              "ng-click",
              "pagination_requests_flight_table(" + aod + ", " + 
                previous_page + ")"
            );
          }
        }
      }
    }

    /*
    Adjust the width of all pagination buttons that are not next or previous.
    The `exact_pagination_buttons_count` is the total pagination buttons minus
    the next and previous buttons.
    */
    var pagination_page_buttons_count = pagination_children.length - 2;

    /*
    The next and previous buttons always occupy 10% width from their parent.
    The other pagination buttons should occupy the max (100% - 20%) of the
    parent's width.
    */
    $("#" + pagination_id + ">." +
      table_dom_class.PAGINATION_BUTTON_DYNAMIC_WIDTH).css(
        "width",
        (80/pagination_page_buttons_count) + "%"
      );

    /*
    Re-compile/re-render AngularJS controller for the pagination buttons.
    Please compile it accordingly (do not re-compile all AngularJS controllers)
    to prevent shadow DOMs.
    */
    if (aod === table_aod.ARRIVAL) {
      angularjs_operation.get_angular_scope_by_dom_id(
        table_dom_id.ARRIVALDEPARTURE_TABLE_SETS_CONTAINER
      ).recompile_arrival_flight_table_pagination();
    }
    else if (aod === table_aod.DEPARTURE) {
      angularjs_operation.get_angular_scope_by_dom_id(
        table_dom_id.ARRIVALDEPARTURE_TABLE_SETS_CONTAINER
      ).recompile_departure_flight_table_pagination();
    }
  }

  return $("#" + pagination_id).pagination({
      arrival_or_departure: aod,
      cssStyle: "",
      currentPage: requested_page,
      itemOnPage: 8,
      items: number_of_pages,
      nextText: "<span aria-hidden='true'>&raquo;</span>",
      prevText: "<span aria-hidden='true'>&laquo;</span>",
      onInit: function () {
        click_and_init();
      },
      onPageClick: function (current_page, event) {
        click_and_init(current_page);
      }
  });
};