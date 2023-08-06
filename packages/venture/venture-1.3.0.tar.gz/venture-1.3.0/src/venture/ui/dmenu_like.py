from __future__ import annotations
from typing import Iterable
import subprocess
from .ui_provider import UIProvider
from .. import util


class DmenuLike(UIProvider):
    command: str
    default_args: Iterable[str] = []
    argument_format: str
    seperator: str = "\n"

    def run(self):
        args = self.get_commandline_args()
        output = self.execute(args)
        parsed = self.parse_output(output)
        return self.items.get(self._display_items.get(parsed))

    def get_commandline_args(self) -> Iterable[str]:
        configuration: dict = self.config.get(self.command)
        if not configuration:
            return []

        return [
            item
            for name, value in configuration.items()
            for item in self.format_arg(name, value)
        ]

    def format_arg(self, name, value):
        if value == False:
            return []
        if value == True:
            value = ""

        return (
            self.argument_format.format(name=name, value=value).rstrip(" ").split(" ")
        )

    def execute(self, args):
        """Execute the UI command.

        This implementation expects the UI to be an external process
        and for it to recieve it's input as a newline-seperated
        list of strings from stdin.
        """
        proc = subprocess.Popen(
            [self.command, *self.default_args, *args],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        return proc.communicate(
            bytes(self.seperator.join(self._display_items), "utf-8")
        )[0]

    def parse_output(self, output: bytes):
        choice = output.decode("utf-8").strip("\n")
        return choice


class Dmenu(DmenuLike):
    command = "dmenu"
    argument_format = "--{name} {value}"


class Rofi(DmenuLike):
    command = "rofi"
    seperator = "|"
    default_args = ["-dmenu", "-markup-rows", "-sep", seperator]
    argument_format = "-{name} {value}"


def tags(item):
    return util.pango_span(
        ", ".join(item.get("tags", [])),
        color="#9c9c9c",
        size="smaller",
        weight="light",
    )


class RofiQL(Rofi):
    default_args = Rofi.default_args + ["-eh", "2"]

    def format_items(self, items):
        return {
            f"{item.get('icon', ''):<2} {name} \n {tags(item)}": name
            for name, item in items.items()
        }


class Wofi(DmenuLike):
    command = "wofi"
    default_args = ["--dmenu", "--allow-markup"]
    argument_format = "--{name} {value}"


class WofiQL(Wofi):
    def format_items(self, items):
        return {
            f"{item.get('icon', ''):<2} {name} {tags(item)}": name
            for name, item in items.items()
        }
