"""DocBlockr for Python.

Author: Adam Bullmer <adam.bullmer@gmail.com>
Website: https://github.com/adambullmer/sublime-docblockr-python

Credit to `spadgos` and the team at DocBlockr for providing some source code
to support this project
"""
import re
import sublime
import sublime_plugin

from typing import Optional

from .utils.consts import PACKAGE_NAME
from .utils.log import child_logger
from .formatters.utils import get_formatter, get_setting
from .parsers.parser import PythonParser, get_parser


log = child_logger(__name__)


def write(view, string):
    """Write a string to the view as a snippet.

    Arguments:
        view   {sublime.View} -- view to have content written to
        string {String}       -- String representation of a snippet to be
            written to the view
    """
    view.run_command("insert_snippet", {"contents": string})


def escape(string):
    r"""Escape the special characters.

    Escapes characters that are also in snippet tab fields so that inserting into the view
    doesn't accidentally create another tabbable field
    Arguments:
        string {String} -- String to be excaped

    Examples:
        >>> escape('function $test() {}')
        'function \$test() \{\}'

    Returns:
        {String} String with escaped characters

    """
    return string.replace("$", r"\$").replace("{", r"\{").replace("}", r"\}")


class DocblockrPythonCommand(sublime_plugin.TextCommand):
    """Sublime Text Command.

    Command to be run by Sublime Text

    Extends:
        sublime_plugin.TextCommand

    Variables:
        position        {Integer}
        trailing_rgn    {String}
        trailing_string {String}
        settings        {String}
        indent_spaces   {String}
        parser          {Object}
        line            {String}
        contents        {String}
    """

    position = 0
    trailing_rgn = ""
    trailing_string = ""
    settings = ""
    indent_spaces = ""
    parser: Optional[PythonParser] = None
    line = ""
    contents = ""
    view_settings = None
    project_settings = None

    def run(self, edit):
        """Sublime Command Entrypoint.

        Entrypoint for the Sublime Text Command. Outputs the result of the parsing to
        the view.

        Arguments:
            edit {sublime.edit} -- Sublime Edit buffer
        """
        assert self.parser is not None

        self.initialize(self.view)

        # If this docstring is already closed, then generate a new line
        if self.parser.is_docstring_closed(self.view, self.view.sel()[0].end()) is True:
            write(self.view, "\n")
            return

        self.view.erase(edit, self.trailing_rgn)

        output = self.parser.parse(self.line, self.contents)

        log.debug("output -> %s", output)

        snippet = self.create_snippet(output)

        log.debug("snippet -> %s", snippet)

        write(self.view, snippet)

    def initialize(self, view: sublime.View):
        """Set up the command's settings.

        Begins preparsing the file to gather some basic information.
        - Which parser to use
        - Store any trailing characters

        Arguments:
            view {sublime.View} -- The view to be edited
        """
        self.view_settings = view.settings()

        project_settings = (view.window().project_data() or {}).get("settings", {})
        self.project_settings = project_settings.get(PACKAGE_NAME, {})

        position = view.sel()[0].end()

        # trailing characters are put inside the body of the comment
        self.trailing_rgn = sublime.Region(position, view.line(position).end())
        self.trailing_string = view.substr(self.trailing_rgn).strip()
        # drop trailing '"""'
        self.trailing_string = escape(
            re.sub(r'\s*("""|\'\'\')\s*$', "", self.trailing_string)
        )

        self.parser = get_parser(view)

        log.debug("get the parser -> %s", self.parser)

        if not self.parser:
            return

        # read the previous line
        self.line, multiline = self.parser.get_definition(view, position)
        self.contents = self.parser.get_definition_contents(
            view, view.line(position).end(), multiline
        )

        if self.line and re.match(r"^\s*async\s+def", self.line):
            log.debug("the function is asynchronous")
            self.line = re.sub(r"async\s+", "", self.line)
            self.contents = re.sub(r"async\s+", "", self.contents)

    def create_snippet(self, parsed_attributes):
        """Format a Sublime Text snippet syntax string.

        Iterates through the list of field groups, and then through each item
        in the group to create the snippets using the user specified formatter.

        Arguments:
            parsed_attributes {dict} -- key value of attributes groups

        Returns:
            str -- sublime text formatted snippet string

        """
        project_formatter = self.project_settings.get("formatter", None)
        formatter = get_formatter(project_formatter or get_setting("formatter"))()

        # Make sure the summary line has the trailing text, or a placeholder
        if not self.trailing_string:
            self.trailing_string = formatter.summary()

        snippet = self.trailing_string + "\n"#formatter.description()

        for attribute_type, attributes in parsed_attributes:
            if len(attributes) == 0:
                continue

            segment = getattr(formatter, attribute_type)
            snippet += segment(attributes)

        snippet += self.parser.closing_string

        return snippet
