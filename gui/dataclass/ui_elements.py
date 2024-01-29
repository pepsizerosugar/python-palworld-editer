from dataclasses import dataclass


@dataclass
class UIElements:
    browse_window: None
    browse_central_widget: None
    banner_label: None
    browse_box_layout: None
    browse_interaction_layout: None
    browse_translation_label: None
    browse_translation_combo: None
    browse_load_file_button: None

    editor_window: None
    editor_central_widget: None
    editor_box_layout: None
    editor_menu_bar: None
    editor_menu_bar_file: None
    editor_table_widget: None

    is_from_update_line_edit: bool = False
