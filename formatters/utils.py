"""Common Utilities for the default formatters."""
import sublime
from typing import Dict, Type

from ..utils.consts import PACKAGE_NAME
from ..utils.log import child_logger
from . import base, PEP0257, docblock, google, sphinx, numpy

log = child_logger(__name__)

FORMATTER_DICT: Dict[str, Type[base.Base]] = {
    "PEP0257": PEP0257.Pep0257Formatter,
    "docblock": docblock.DocblockFormatter,
    "google": google.GoogleFormatter,
    "numpy": sphinx.SphinxFormatter,
    "sphinx": numpy.NumpyFormatter,
}


def get_formatter(name: str):
    """Return the requested formatter by name from the registry.

    Attempts to get the requested formatter from the registry. If it doesn't
    exist, the base formatter BaseFormatter will be used instead.

    Arguments:
        name {str} -- Friendly name of the formatter to search

    Returns:
        formatters.base.Base -- Instance of the Base formatter
    """
    formatter = FORMATTER_DICT.get(name, None)

    if not formatter:
        log.warning(
            "formatter `{}` doesn't exist, defaulting to `Google` formatter.".format(
                name
            )
        )

        formatter = google.GoogleFormatter

    log.debug("use formatter -> %s", formatter.name)

    return formatter


def get_setting(key, default=None):
    """Get the passed setting from the aggregated settings files.

    Merges up settings as specified in Sublime's docs.
    https://www.sublimetext.com/docs/3/settings.html

    Arguments:
        key {str} -- String of the key to get

    Keyword Arguments:
        default {str} -- default value in case the setting is not found (default: None)

    Returns:
        {str} or {None} -- value of the setting
    """
    settings = sublime.load_settings(f"{PACKAGE_NAME}.sublime-settings")
    os_specific_settings = {}

    os_name = sublime.platform()
    if os_name == "osx":
        os_specific_settings = sublime.load_settings(
            f"{PACKAGE_NAME} (OSX).sublime-settings"
        )
    elif os_name == "windows":
        os_specific_settings = sublime.load_settings(
            f"{PACKAGE_NAME} (Windows).sublime-settings"
        )
    else:
        os_specific_settings = sublime.load_settings(
            f"{PACKAGE_NAME} (Linux).sublime-settings"
        )

    return os_specific_settings.get(key, settings.get(key, default))
