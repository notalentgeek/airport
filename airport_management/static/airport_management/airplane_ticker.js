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

app.controller("table_arrivaldeparture_main", function ($scope) {
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
});

// Function to set the arrival and departure paginations.
var set_table_pagination_for_arrivaldeparture = function (
  pagination_id
) {
  $(pagination_id).pagination({
      cssStyle: '',
      currentPage: 1,
      itemOnPage: 8,
      items: 20,
      nextText: '<span aria-hidden="true">&raquo;</span>',
      prevText: '<span aria-hidden="true">&laquo;</span>',
      onPageClick: function (page, event) {
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
            var li_content = $(li_children[j]);

            if (li_content.hasClass("next") || li_content.hasClass("prev")) {
              li.addClass("pagination-fixed-width");
              break;
            }
            else {
              li.addClass("pagination-dynamic-width");
              break;
            }
          }
        }

        // Only adjust the size of the non-next and non-previous buttons.
        var children_count = pagination_children.length - 2;
        $(pagination_id + ">li.pagination-dynamic-width")
          .css("width", (80/children_count) + "%");
      }
  });
};

// Function to initiated arrival and departure paginations.
$(function() {
  set_table_pagination_for_arrivaldeparture("#pagination-arrival");
  set_table_pagination_for_arrivaldeparture("#pagination-departure");
});