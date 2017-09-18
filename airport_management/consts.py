# Enumeration class to refer to `ArrivalFlight` or `DepartureFlight`.
class AOD():
    ARRIVAL = 1
    DEPARTURE = 2

# Enumeration for all CSS id and class used for front-end.
class CSS():
    # CSS IDs.
    AIRPORT_MANAGER_BUTTON_ID = "airport-manager-button"
    AIRPORT_MANAGER_WRONG_PASSWORD_MODAL_ID =\
        "airport-manager-wrong-password-modal"
    AIRPORT_MANAGER_NAME_INPUT_ID = "airport-manager-name-input"
    AIRPORT_MANAGER_PASSWORD_INPUT_ID = "airport-manager-password-input"
    AIRPORT_MANAGER_REGISTER_BUTTON_ID = "airport-manager-register-button"
    ARRIVALDEPARTURE_TABLE_SET_CONTAINER_ID =\
        "arrivaldeparture-table-sets-container"
    ARRIVAL_FLIGHT_TABLE_ERROR_ID = "arrival-flight-table-error"
    ARRIVAL_FLIGHT_TABLE_ID = "arrival-flight-table"
    ARRIVAL_FLIGHT_TABLE_PAGINATION_ID = "arrival-flight-table-pagination"
    ARRIVAL_FLIGHT_TABLE_REQUESTING_ID = "arrival-flight-table-requesting"
    ARRIVAL_FLIGHT_TABLE_SET_CONTAINER_ID = "arrival-flight-table-set-container"
    ATC_FORM_CODE_INPUT_ID = "atc-code-input"
    ATC_FORM_MODAL_BUTTON_CONTAINER_ID = "atc-form-modal-button-container"
    ATC_FORM_MODAL_BUTTON_ID = "atc-form-modal-button"
    ATC_FORM_MODAL_ID = "atc-form-modal"
    ATC_FORM_REGISTER_BUTTON_ID = "atc-form-register-button"
    ATC_LIST_MODAL_BUTTON_CONTAINER_ID = "atc-list-modal-button-container"
    ATC_LIST_MODAL_BUTTON_ID = "atc-list-modal-button"
    ATC_LIST_MODAL_ID = "atc-list-modal"
    ATC_MODAL_BUTTONS_CONTAINER_HIDE_MOBILE_ID =\
        "atc-menu"
    ATC_MODAL_BUTTONS_MOVE_MOBILE_ID = "atc-modal-buttons-move-mobile"
    ATC_MODAL_BUTTONS_MOVE_NON_MOBILE_ID = "atc-modals-buttons-container"
    DEPARTURE_FLIGHT_TABLE_ERROR_ID = "departure-flight-table-error"
    DEPARTURE_FLIGHT_TABLE_ID = "departure-flight-table"
    DEPARTURE_FLIGHT_TABLE_PAGINATION_ID = "departure-flight-table-pagination"
    DEPARTURE_FLIGHT_TABLE_REQUESTING_ID = "departure-flight-table-requesting"
    DEPARTURE_FLIGHT_TABLE_SET_CONTAINER_ID =\
        "departure-flight-table-set-container"
    FLIGHT_MANAGEMENT_PANEL_CONTENT_ID = "flight-management-panel-content"
    FLIGHT_MANAGEMENT_PANEL_ID = "flight-management-panel"
    PAGINATION_REQUEST_FLIGHT_TABLE_ID = "pagination-request-flight-table"
    TABLE_REQUEST_FLIGHT_ID = "table-request-flight"
    TITLE_ID =  "title"

    # CSS classes.
    FLIGHT_MANAGEMENT_PANEL_KEY_CLASS = "flight-management-panel-information-non-status-key"
    FLIGHT_MANAGEMENT_PANEL_VALUE_CLASS = "flight-management-panel-information-non-status-value"
    HIDE_FOR_SMALL_WIDTH_CLASS = "hide-for-small-width"
    PAGINATION_BUTTON_DYNAMIC_WIDTH_CLASS = "pagination-button-dynamic-width"
    PAGINATION_BUTTON_FIXED_WIDTH_CLASS = "pagination-button-fixed-width"

# GET and POST keys.
class KEY():
    # GET.
    AIRPORT_MANAGER_NAME = "airport_manager_name"
    ATC_CODE = "atc_code"
    FLIGHT_ID = "flight_id"
    REQUESTED_TABLE_PAGINATION_PAGE = "requested_table_pagination_page"
    REQUESTED_TABLE = "requested_table"

    # POST usually come from DOM input.
    AIRPORT_MANAGER_PASSWORD_INPUT = "airport_manager_password_input"
    AIRPORT_MANAGER_NAME_INPUT = "airport_manager_name_input"
    AIRPORT_MANAGER_SUBMIT_BUTTON = "airport_manager_submit_button"
    ATC_FORM_CODE_INPUT = "atc_form_code_input"
    ATC_FORM_FIRST_NAME_INPUT = "atc_form_first_name_input"
    ATC_FORM_LAST_NAME_INPUT = "atc_form_last_name_input"

    # Sent key to the client.
    AIRPORT_MANAGER = "airport_manager"
    ATCS = "atcs"
    CLASS = "class"
    DOMS = "doms"
    FLIGHT_MANAGEMENT_PANEL_INITIAL_ARRIVALDEPARTURE =\
        "flight_management_panel_initial_arrivaldeparture"
    FLIGHT_MANAGEMENT_PANEL_INITIAL_DOMS =\
        "flight_management_panel_initial_doms"
    FLIGHT_MANAGEMENT_PANEL_INITIAL_FLIGHT_ID =\
        "flight_management_panel_initial_flight_id"
    FLIGHT_MANAGEMENT_PANEL_INITIAL_FLIGHT_LANE =\
        "flight_management_panel_initial_flight_lane"
    FLIGHT_MANAGEMENT_PANEL_INITIAL_FLIGHT_ONLINE_ATCS =\
        "flight_management_panel_initial_flight_online_atcs"
    FLIGHT_MANAGEMENT_PANEL_INITIAL_STATUS_DOM =\
        "flight_management_panel_initial_status_dom"
    LANE = "lane"
    NUMBER_OF_PAGES = "number_of_pages"
    OBJECTS = "objects"
    ONLINE_ATC = "online_atc"
    STATUS = "status"
    TABLE_HTML = "html_table"
    TABLES_PROPERTIES = "tables_properties"
    TEXT = "text"