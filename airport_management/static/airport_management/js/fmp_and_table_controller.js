// Initiate controller and set the views.
airport_manager_wrong_password_modal =
  new airport_manager_wrong_password_modal();
atc_list_modal = new atc_list_modal(app);
atc_registration_form_modal = new atc_registration_form_modal(app);
navbar_right = new navbar_right(app);
flight_online_atcs_form_modal = new flight_online_atcs_form_modal(app);
inner_table = new inner_table();

flight_management_panel = new flight_management_panel(app,
  flight_online_atcs_form_modal.DOM_ID.FLIGHT_ATC_FORM_MODAL);
console.log([atc_list_modal, atc_registration_form_modal] );
navbar_left = new navbar_left(app,
  navbar_right.JQUERY_SELECTOR.AIRPORT_MANAGER_BUTTON,
  [atc_list_modal, atc_registration_form_modal]  
);

table = new table(app,
  flight_management_panel.DOM_ID.FLIGHT_MANAGEMENT_PANEL_INFORMATION,
  flight_online_atcs_form_modal);

// Functions that need to be initiated after all views ready.
airport_manager_wrong_password_modal.check_wrong_password();