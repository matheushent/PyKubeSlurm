"""
This module contains unit tests for the `settings.py` module.

The `settings.py` module contains static settings and configurations for the application.
These tests ensure that the settings are correctly defined and that they can be
accessed and modified as expected.
"""
from pykubeslurm.settings import Settings


def test_validate_log_level():
    assert Settings.validate_debug_level("DEBUG", None) == "DEBUG"
    assert Settings.validate_debug_level("INFO", None) == "INFO"
    assert Settings.validate_debug_level("WARNING", None) == "WARNING"
    assert Settings.validate_debug_level("ERROR", None) == "ERROR"
    assert Settings.validate_debug_level("CRITICAL", None) == "CRITICAL"
    assert Settings.validate_debug_level("NOTSET", None) == "NOTSET"

    try:
        Settings.validate_debug_level("INVALID", None)
    except ValueError as e:
        assert str(e) == "Invalid debug level: INVALID"
