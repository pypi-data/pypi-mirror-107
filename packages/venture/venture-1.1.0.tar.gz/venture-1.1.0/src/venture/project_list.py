from typing import Dict, Optional
from pathlib import Path
import os

from .types import DirectorySchema
from .config import config
from .icons import icon
from . import util

GLOB = "/*"
EXCLUDED_DIRS = [
    "node_modules",
    ".git",
]


class Project:
    """OO Representation of a project directory

    `self.specificity` will change the amount of the full path shown.

    path: `/home/sean/sourcecode/rust`
    - specificity 1 => rust
    - specificity 2 => sourcecode/rust
    - specificity 3 => sean/sourcecode/rust
    ...

    If a prefix path is provided, the initial specificity is
    is equal to the number of path components in the path and not in
    the prefix

    path: `/home/sean/sourcecode/rust`
    - prefix: `/home/sean/sourcecode` => rust
    - prefix: `/home/sean` => sourcecode/rust
    ...
    """

    def __init__(self, path: str, prefix: Optional[str]):
        self.path: Path = Path(path).expanduser().resolve()
        self.fullpath = str(self.path)
        self.icon: Optional[str] = (
            self.get_icon("directory")
            if self.path.is_dir()
            else self.get_icon(self.path.suffix)
        )
        self.specificity = 1

        if prefix:
            # breakpoint()
            self.specificity = len(
                str(self.path).removeprefix(prefix).lstrip("/").split("/")
            )

    @property
    def name(self):
        parts = self.path.parts
        start = len(parts) - (self.specificity)
        start = 0 if start < 0 else start
        name = "/".join(parts[start:])

        # The first element of self.path.parts is a / instead
        # of an empty string like in my implementation, which may cause some
        # issues if we end up showing the entire string, so we just set it to ""
        if start == 0:
            name = name[1:]

        return name

    def __str__(self):
        return f"{self.icon + '  ' if self.icon else ''}{self.name}"

    def __repr__(self):
        return f"<Project {self.path}>"

    @staticmethod
    def get_icon(filetype: str) -> Optional[str]:
        """Returns the icon associated with a specific file type,
        returns none if config.show_icons is set to False"""
        if not config.show_icons:
            return None

        return icon(filetype)


class ProjectList:
    def __init__(self, directories: DirectorySchema):
        self.dirs = directories
        self.projects: Dict[str, Project] = {}

        self.handle_directories()

    def handle_directories(self):
        for directory in self.dirs:
            if directory in EXCLUDED_DIRS:
                continue

            if isinstance(directory, str):
                self.projects |= {
                    str(project): project for project in self.get_projects(directory)
                }
            elif isinstance(directory, dict):
                self.handle_nested_dirs(**directory)

    def handle_nested_dirs(self, base: str, subs: list[str]):
        """handle a base directory and it's sub-dirs"""
        directories = [f"{base}/{sub.lstrip('/')}" for sub in subs]
        # if config.include_parent_folder:
        directories.append(base)

        for directory in directories:
            self.projects |= {
                str(project): project for project in self.get_projects(directory, base)
            }

    def get_projects(self, directory: str, prefix: Optional[str] = None):
        """Gets all the projects / files from the specified directory
        appends icons to each path if `config['show_icons']` is `True`
        """
        directory = util.resolve(directory)
        prefix = prefix or directory

        if directory.endswith(GLOB):
            self.handle_glob(directory)
            return

        for obj in os.scandir(directory):
            path = Path(obj.path)
            if (path.name.startswith(".") and not config.show_hidden) or (
                path.is_file() and not config.show_files
            ):
                continue

            project = Project(str(path), prefix)
            while str(project) in self.projects:
                # Handle this going on for too long?
                project.specificity += 1

            yield project

    def handle_glob(self, directory: str):
        directory = directory.rstrip(GLOB)
        dirs = [
            obj.path.removeprefix(directory)
            for obj in os.scandir(directory)
            if obj.is_dir()
            and (True if config.show_hidden else not obj.name.startswith("."))
        ]

        self.handle_nested_dirs(
            directory,
            dirs,
        )
