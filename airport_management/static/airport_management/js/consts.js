/*
Simple enumeration for arrival or departure. `AOD` is meant for "arrival or
departure". Do not use `0` as an enumeration value because it can be coerced
into `false`.
*/
var AOD = Object.freeze({
  ARRIVAL: 1,
  DEPARTURE: 2
});

// AngularJS controller strings.
var CONTROLLER_STRING = Object.freeze({
  ATC_MENU: "atc_menu",
  ATC_FORM: "atc_form",
  FLIGHT_MANAGEMENT_PANEL: "flight_management_panel",
  LOGIN_AND_REGISTER_FORM: "login_and_register_form",
  ARRIVALDEPARTURE_TABLE: "arrivaldeparture_table"
});

// CSS classes.
var CSS = Object.freeze({
  // CSS IDs.
  AIRPORT_MANAGER_BUTTON_ID: "airport-manager-button",
  AIRPORT_MANAGER_WRONG_PASSWORD_MODAL_ID:
    "airport-manager-wrong-password-modal",
  AIRPORT_MANAGER_NAME_INPUT_ID: "airport-manager-name-input",
  AIRPORT_MANAGER_PASSWORD_INPUT_ID: "airport-manager-password-input",
  AIRPORT_MANAGER_REGISTER_BUTTON_ID: "airport-manager-register-button",
  ARRIVALDEPARTURE_TABLE_SET_CONTAINER_ID:
    "arrivaldeparture-table-set-container",
  ARRIVAL_FLIGHT_TABLE_ERROR_ID: "arrival-flight-table-error",
  ARRIVAL_FLIGHT_TABLE_ID: "arrival-flight-table",
  ARRIVAL_FLIGHT_TABLE_PAGINATION_ID: "arrival-flight-table-pagination",
  ARRIVAL_FLIGHT_TABLE_REQUESTING_ID: "arrival-flight-table-requesting",
  ARRIVAL_FLIGHT_TABLE_SET_CONTAINER_ID: "arrival-flight-table-set-container",
  ATC_FORM_CODE_INPUT_ID: "atc-form-code-input",
  ATC_FORM_MODAL_BUTTON_CONTAINER_ID: "atc-form-modal-button-container",
  ATC_FORM_MODAL_BUTTON_ID: "atc-form-modal-button",
  ATC_FORM_MODAL_ID: "atc-form-modal",
  ATC_FORM_REGISTER_BUTTON_ID: "atc-form-register-button",
  ATC_LIST_MODAL_BUTTON_CONTAINER_ID: "atc-list-modal-button-container",
  ATC_LIST_MODAL_BUTTON_ID: "atc-list-modal-button",
  ATC_LIST_MODAL_ID: "atc-list-modal",
  ATC_MODAL_BUTTONS_CONTAINER_HIDE_MOBILE_ID:
    "atc-modal-buttons-container-hide-mobile",
  ATC_MODAL_BUTTONS_MOVE_MOBILE_ID: "atc-modal-buttons-move-mobile",
  ATC_MODAL_BUTTONS_MOVE_NON_MOBILE_ID: "atc-modal-buttons-move-non-mobile",
  DEPARTURE_FLIGHT_TABLE_ERROR_ID: "departure-flight-table-error",
  DEPARTURE_FLIGHT_TABLE_ID: "departure-flight-table",
  DEPARTURE_FLIGHT_TABLE_PAGINATION_ID: "departure-flight-table-pagination",
  DEPARTURE_FLIGHT_TABLE_REQUESTING_ID: "departure-flight-table-requesting",
  DEPARTURE_FLIGHT_TABLE_SET_CONTAINER_ID:
    "departure-flight-table-set-container",
  FLIGHT_MANAGEMENT_PANEL_CONTENT_ID: "flight-management-panel-content",
  FLIGHT_MANAGEMENT_PANEL_ID: "flight-management-panel",
  PAGINATION_REQUEST_FLIGHT_TABLE_ID: "pagination-request-flight-table",
  TABLE_REQUEST_FLIGHT_ID : "table-request-flight",
  TITLE_ID:  "title",

  // CSS classes.
  FLIGHT_MANAGEMENT_PANEL_KEY_CLASS: "flight-management-panel-key",
  FLIGHT_MANAGEMENT_PANEL_VALUE_CLASS: "flight-management-panel-value",
  HIDE_FOR_SMALL_WIDTH_CLASS: "hide-for-small-width",
  PAGINATION_BUTTON_DYNAMIC_WIDTH_CLASS: "pagination-button-dynamic-width",
  PAGINATION_BUTTON_FIXED_WIDTH_CLASS: "pagination-button-fixed-width"
});

// HTTP keys.
var KEY = Object.freeze({
  // GET.
  AIRPORT_MANAGER_NAME: "airport_manager_name",
  ATC_CODE: "atc_code",
  FLIGHT_ID: "flight_id",
  REQUESTED_PAGINATION_PAGE: "requested_pagination_page",
  REQUESTED_TABLE: "requested_table",

  // POST usually come from DOM input.
  AIRPORT_MANAGER_PASSWORD_INPUT: "airport_manager_password_input",
  AIRPORT_MANAGER_NAME_INPUT: "airport_manager_name_input",
  AIRPORT_MANAGER_SUBMIT_BUTTON: "airport_manager_submit_button",
  ATC_FORM_CODE_INPUT: "atc_form_code_input",
  ATC_FORM_FIRST_NAME_INPUT: "atc_form_first_name_input",
  ATC_FORM_LAST_NAME_INPUT: "atc_form_last_name_input",

  // Received key to the client.
  NUMBER_OF_PAGES: "number_of_pages",
  TABLE_HTML: "html_table"
});