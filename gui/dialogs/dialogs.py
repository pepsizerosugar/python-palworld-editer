"""Convenience wrappers for file dialogs used by the editor."""

from PyQt5.QtWidgets import QFileDialog, QWidget


def dialog_for_load_settings_file(window: QWidget) -> str:
    """Open a read-only file dialog for selecting ``PalWorldSettings.ini``.

    Args:
        window (QWidget): Parent window for modal behavior.

    Returns:
        str: Selected file path or an empty string when cancelled.
    """

    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    filename, _ = QFileDialog.getOpenFileName(
        window,
        "Load Settings File",
        "",
        "INI Files (*.ini);;All Files (*)",
        options=options,
    )
    return filename


def dialog_for_save_settings_file(window: QWidget) -> str:
    """Open a dialog for choosing where to save the settings file.

    Args:
        window (QWidget): Parent window for modal behavior.

    Returns:
        str: Destination file path or an empty string when cancelled.
    """

    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    filename, _ = QFileDialog.getSaveFileName(
        window,
        "Save Settings File",
        "",
        "INI Files (*.ini);;All Files (*)",
        options=options,
    )
    return filename
