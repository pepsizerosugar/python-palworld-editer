"""Thin wrappers around ``QMessageBox`` for consistent user feedback."""

from typing import Any

from PyQt5.QtWidgets import QMessageBox


def if_settings_file_is_not_loaded() -> None:
    """Warn the user when attempting to save without a loaded file."""

    QMessageBox.warning(None, "Warning", "Settings file not loaded. Please load a settings file first.")


def if_load_settins_file_is_finished() -> None:
    """Inform the user that settings finished loading."""

    QMessageBox.information(None, "Information", "Settings file loaded finished.")


def if_update_settings_finished() -> None:
    """Inform the user that settings were updated."""

    QMessageBox.information(None, "Information", "Settings updated finished.")


def if_error_when_load_metadata(error: Exception) -> None:
    """Show an error message when metadata cannot be read."""

    QMessageBox.warning(None, "Warning", f"Error loading metadata: {error}")


def if_error_when_load_palworld_options_type(error: Exception) -> None:
    """Show an error when the option type map fails to load."""

    QMessageBox.warning(None, "Warning", f"Error loading palworld options type: {error}")


def if_error_when_load_special_options_file(error: Exception) -> None:
    """Show an error when a custom options file cannot be loaded."""

    QMessageBox.warning(None, "Warning", f"Error loading special options file: {error}")


def if_error_when_load_banner_image(error: Exception) -> None:
    """Show an error when the banner image cannot be displayed."""

    QMessageBox.warning(None, "Warning", f"Error loading banner image: {error}")


def if_error_when_load_translations(error: Exception) -> None:
    """Show an error when translations fail to load."""

    QMessageBox.warning(None, "Warning", f"Error loading translations: {error}")


def if_error_when_load_settings_file(error: Exception) -> None:
    """Show an error when the settings file cannot be opened."""

    QMessageBox.warning(None, "Warning", f"Error loading settings file: {error}")


def if_error_when_save_settings_file(error: Exception) -> None:
    """Show an error when saving settings fails."""

    QMessageBox.warning(None, "Warning", f"Error saving settings file: {error}")


def if_save_settings_file_success() -> None:
    """Inform the user that settings were saved successfully."""

    QMessageBox.information(None, "Information", "Settings file saved successfully.")


def if_error_when_update_settings(option: str, value: Any) -> None:
    """Show an error when a setting cannot be updated in the UI.

    Args:
        option (str): Option name being updated.
        value (Any): Value that failed to apply.
    """

    QMessageBox.warning(None, "Warning", f"Error updating settings: {option}={value}")


def if_error_when_save_settings_elements_is_none() -> None:
    """Notify the user when no table values are available to save."""

    QMessageBox.warning(None, "Warning", "Error saving settings file: Please try again.")


def if_error_when_load_menu_translation(error: Exception) -> None:
    """Show an error when menu translation strings cannot be read."""

    QMessageBox.warning(None, "Warning", f"Error loading menu translation: {error}")
