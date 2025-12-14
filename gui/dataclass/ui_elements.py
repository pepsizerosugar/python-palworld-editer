"""Containers for commonly accessed UI widget instances."""

from dataclasses import dataclass
from typing import Optional

from PyQt5.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)


@dataclass
class UIElements:
    """Registry of PyQt widgets used across the application."""

    browse_window: Optional[QMainWindow] = None
    browse_central_widget: Optional[QWidget] = None
    banner_label: Optional[QLabel] = None
    browse_box_layout: Optional[QVBoxLayout] = None
    browse_interaction_layout: Optional[QVBoxLayout | QHBoxLayout] = None
    browse_translation_label: Optional[QLabel] = None
    browse_translation_combo: Optional[QComboBox] = None
    browse_load_file_button: Optional[QPushButton] = None

    editor_window: Optional[QMainWindow] = None
    editor_central_widget: Optional[QWidget] = None
    editor_box_layout: Optional[QVBoxLayout] = None
    editor_menu_bar: Optional[QMenuBar] = None
    editor_menu_bar_file: Optional[QMenu] = None
    editor_table_widget: Optional[QTableWidget] = None

    is_from_update_line_edit: bool = False
