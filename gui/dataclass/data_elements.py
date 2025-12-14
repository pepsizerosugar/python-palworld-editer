"""State containers for runtime data shared across the UI."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DataElements:
    """Data bucket for metadata, translations, and loaded settings."""

    metadata: Optional[Dict[str, str]] = None
    translation_code: Optional[str] = None
    special_settings_file_path: Optional[str] = None
    palworld_options_type: Optional[Dict[str, str]] = None
    settings_file_path: Optional[str] = None
    is_first_load: Optional[bool] = None
    special_palworld_options: Optional[Dict[str, Any]] = None
    palworld_options: Optional[Dict[str, Any]] = None
    palworld_options_to_save: Optional[Dict[str, Any]] = None
    options_translations: Optional[Dict[str, Dict[str, str]]] = None
    input_value: Optional[float] = None
    menu_translations: Optional[Dict[str, Dict[str, str]]] = None
    translation_code_list: Optional[List[str]] = None
