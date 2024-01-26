from dataclasses import dataclass


@dataclass
class UIElements:
    # borowse widget elements
    browse_window: None
    browse_central_widget: None
    banner_label: None
    browse_box_layout: None
    browse_interaction_layout: None
    browse_translation_label: None
    browse_translation_combo: None
    browse_load_file_button: None

    # settings widget elements
    settings_window: None
    settings_central_widget: None
    settings_box_layout: None
    settings_menu_bar: None
    settings_menu_bar_file: None
    settings_table_widget: None

    # settings value widget elements
    settings_value_widget: None