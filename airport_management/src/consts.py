"""
This file is just collection of constants. I use this to maintain (kinda)
reference to DOM ID.
"""

from collections import namedtuple

AOD = namedtuple("AOD", "ARRIVAL DEPARTURE")
AOD = AOD(
    ARRIVAL="1",
    DEPARTURE="2"
)
DOM_CLASS = namedtuple(
    "CLASS",
    "\
        FMP_INFORMATION_NON_STATUS_KEY \
        FMP_INFORMATION_NON_STATUS_VALUE \
    "
)
DOM_CLASS = DOM_CLASS(
    FMP_INFORMATION_NON_STATUS_KEY="fmp-information-non-status-key",
    FMP_INFORMATION_NON_STATUS_VALUE="fmp-information-non-status-value"
)
DOM_ID = namedtuple(
    "DOM_ID",
    "\
        ARRIVAL_FLIGHT_TABLE \
        ARRIVAL_FLIGHT_TABLE_ERROR \
        ARRIVAL_FLIGHT_TABLE_PAGINATION \
        ARRIVAL_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES \
        ARRIVAL_FLIGHT_TABLE_REQUESTING \
        DEPARTURE_FLIGHT_TABLE \
        DEPARTURE_FLIGHT_TABLE_ERROR \
        DEPARTURE_FLIGHT_TABLE_PAGINATION \
        DEPARTURE_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES \
        DEPARTURE_FLIGHT_TABLE_REQUESTING \
    "
)
DOM_ID = DOM_ID(
    ARRIVAL_FLIGHT_TABLE="arrival-flight-table",
    ARRIVAL_FLIGHT_TABLE_ERROR="arrival-flight-table-error",
    ARRIVAL_FLIGHT_TABLE_PAGINATION="arrival-flight-table-pagination",
    ARRIVAL_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES=\
        "arrival-flight-table-pagination-number-of-pages",
    ARRIVAL_FLIGHT_TABLE_REQUESTING="arrival-flight-table-requesting",
    DEPARTURE_FLIGHT_TABLE="departure-flight-table",
    DEPARTURE_FLIGHT_TABLE_ERROR="departure-flight-table-error",
    DEPARTURE_FLIGHT_TABLE_PAGINATION="departure-flight-table-pagination",
    DEPARTURE_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES=\
        "departure-flight-table-pagination-number-of-pages",
    DEPARTURE_FLIGHT_TABLE_REQUESTING="departure-flight-table-requesting"
)
KEY = namedtuple(
    "KEY",
    "\
        AIRPORT_MANAGER \
        AIRPORT_MANAGER_LOGIN_OR_REGISTER_BUTTON \
        AIRPORT_MANAGER_NAME \
        AIRPORT_MANAGER_NAME_INPUT \
        AIRPORT_MANAGER_PASSWORD_INPUT \
        ARRIVALDEPARTUREFLIGHT_OBJECTS \
        ARRIVAL_FLIGHT_TABLE_PAGINATION \
        ATC_CODE \
        ATC_CODE_INPUT \
        ATC_FIRST_NAME_INPUT \
        ATC_LAST_NAME_INPUT \
        ATC_OBJECTS \
        CLASS \
        DEPARTURE_FLIGHT_TABLE_PAGINATION \
        DOM_ID \
        DOM_PARAMETERS \
        FLIGHT_ONLINE_ATC_FORM_ARRIVALDEPARTURE \
        FLIGHT_ONLINE_ATC_FORM_FLIGHT_ID \
        FLIGHT_ONLINE_ATC_FORM_FLIGHT_ONLINE_ATCS_ID \
        FLIGHT_ID \
        FLIGHT_LANE_FORM_ARRIVALDEPARTURE \
        FLIGHT_LANE_FORM_FLIGHT_ID \
        FLIGHT_LANE_FORM_FLIGHT_ONLINE_ATCS \
        FLIGHT_MANAGEMENT_PANEL_INITIAL_PROPERTIES \
        FLIGHT_OBJECTS \
        FLIGHT_ONLINE_ATC_CHECK_BOXES \
        FMP_DOM \
        FMP_NON_STATUS_ARRIVALDEPARTURE \
        FMP_NON_STATUS_DOM_PARAMETERS \
        FMP_NON_STATUS_FLIGHT_ID \
        FMP_NON_STATUS_LANE \
        FMP_NON_STATUS_ONLINE_ATCS \
        FMP_STATUS \
        LANE_OBJECTS \
        NUMBER_OF_PAGES \
        OBJECTS \
        REQUESTED_TABLE \
        REQUESTED_TABLE_PAGINATION_PAGE \
        TABLES_PROPERTIES \
        TABLE_ERROR_ID \
        TABLE_HTML \
        TABLE_ID \
        TABLE_PAGINATION_ID \
        TABLE_PAGINATION_NUMBER_OF_PAGES \
        TABLE_PAGINATION_NUMBER_OF_PAGES_ID \
        TABLE_PROPERTIES_ARRIVALDEPARTUREFLIGHT_OBJECTS \
        TABLE_TITLE \
        TABLE_REQUESTING_ID \
        TEXT \
    "
)

KEY = KEY(
    AIRPORT_MANAGER="airport_manager",
    AIRPORT_MANAGER_LOGIN_OR_REGISTER_BUTTON=\
        "airport_manager_login_or_register_button",
    AIRPORT_MANAGER_NAME="airport_manager_name",
    AIRPORT_MANAGER_NAME_INPUT="airport_manager_name_input",
    AIRPORT_MANAGER_PASSWORD_INPUT="airport_manager_password_input",
    ARRIVALDEPARTUREFLIGHT_OBJECTS="arrivaldepartureflight_objects",
    ARRIVAL_FLIGHT_TABLE_PAGINATION="arrival_flight_table_pagination",
    ATC_CODE="atc_code",
    ATC_CODE_INPUT="atc_code_input",
    ATC_FIRST_NAME_INPUT="atc_first_name_input",
    ATC_LAST_NAME_INPUT="atc_last_name_input",
    ATC_OBJECTS="atc_objects",
    CLASS="class",
    DEPARTURE_FLIGHT_TABLE_PAGINATION="departure_flight_table_pagination",
    DOM_ID="dom_id",
    DOM_PARAMETERS="dom_parameters",
    FLIGHT_ONLINE_ATC_FORM_ARRIVALDEPARTURE=\
        "flight_online_atc_form_arrivaldeparture",
    FLIGHT_ONLINE_ATC_FORM_FLIGHT_ID="flight_online_atc_form_flight_id",
    FLIGHT_ONLINE_ATC_FORM_FLIGHT_ONLINE_ATCS_ID=\
        "flight_online_atc_form_flight_online_atcs_id",
    FLIGHT_ID="flight_id",
    FLIGHT_LANE_FORM_ARRIVALDEPARTURE="flight_lane_form_arrivaldeparture",
    FLIGHT_LANE_FORM_FLIGHT_ID="flight_lane_form_flight_id",
    FLIGHT_LANE_FORM_FLIGHT_ONLINE_ATCS="flight_lane_form_flight_lane",
    FLIGHT_MANAGEMENT_PANEL_INITIAL_PROPERTIES=\
        "flight_management_panel_initial_properties",
    FLIGHT_OBJECTS="flight_objects",
    FLIGHT_ONLINE_ATC_CHECK_BOXES="flight_online_atc_check_boxes",
    FMP_DOM="fmp_dom",
    FMP_NON_STATUS_ARRIVALDEPARTURE="fmp_non_status_arrivaldeparture",
    FMP_NON_STATUS_DOM_PARAMETERS="fmp_non_status_dom_parameters",
    FMP_NON_STATUS_FLIGHT_ID="fmp_non_status_flight_id",
    FMP_NON_STATUS_LANE="fmp_non_status_lane",
    FMP_NON_STATUS_ONLINE_ATCS="fmp_non_status_online_atcs",
    FMP_STATUS="fmp_status",
    LANE_OBJECTS="lane_objects",
    NUMBER_OF_PAGES="number_of_pages",
    OBJECTS="objects",
    REQUESTED_TABLE="requested_table",
    REQUESTED_TABLE_PAGINATION_PAGE="requested_table_pagination_page",
    TABLES_PROPERTIES="tables_properties",
    TABLE_ERROR_ID="table_error_id",
    TABLE_HTML="table_html",
    TABLE_ID="table_id",
    TABLE_PAGINATION_ID="table_pagination_id",
    TABLE_PAGINATION_NUMBER_OF_PAGES="table_pagination_number_of_pages",
    TABLE_PAGINATION_NUMBER_OF_PAGES_ID="table_pagination_number_of_pages_id",
    TABLE_PROPERTIES_ARRIVALDEPARTUREFLIGHT_OBJECTS=\
        "table_properties.arrivaldepartureflight_objects",
    TABLE_REQUESTING_ID="table_requesting_id",
    TABLE_TITLE="table_title",
    TEXT="text"
)
MODAL_FIELD = namedtuple(
    "MODEL_FIELD",
    "\
        AIRPORT_MANAGER_NAME \
        ATC_CODE \
        SCHEDULED_DATETIME \
    "
)
MODAL_FIELD = MODAL_FIELD(
    AIRPORT_MANAGER_NAME="username",
    ATC_CODE="code",
    SCHEDULED_DATETIME="scheduled_datetime"
)
STRING = namedtuple(
    "STRING",
    "\
        AIRPORT_MANAGER_GROUP \
        ARRIVAL_TABLE_TITLE \
        DEPARTURE_TABLE_TITLE \
        FLIGHT_AIRPORT_KEY \
        FLIGHT_CODE_KEY \
        FLIGHT_DAY_KEY \
        FLIGHT_SCHEDULE_KEY \
        LOGIN \
        NO_ATC \
        NO_ATC_AND_NO_LANE \
        NO_LANE \
        REGISTER \
    "
)
STRING = STRING(
    AIRPORT_MANAGER_GROUP="airport_manager_group",
    ARRIVAL_TABLE_TITLE="arrival table",
    DEPARTURE_TABLE_TITLE="departure table",
    FLIGHT_AIRPORT_KEY="airport: ",
    FLIGHT_CODE_KEY="code: ",
    FLIGHT_DAY_KEY="day: ",
    FLIGHT_SCHEDULE_KEY="schedule: ",
    LOGIN="login",
    NO_ATC="no atc",
    NO_ATC_AND_NO_LANE="no atc and not lane",
    NO_LANE="no lane",
    REGISTER="register"
)
VALUE = namedtuple("VALUE", "PAGINATION_OBJECTS_COUNT_PER_PAGE")
VALUE = VALUE(
    PAGINATION_OBJECTS_COUNT_PER_PAGE=100
)