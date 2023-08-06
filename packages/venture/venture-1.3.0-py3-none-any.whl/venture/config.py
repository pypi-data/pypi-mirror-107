from typing import Any
import os
import yaml
from arc.utils import timer, logger

from .types import DirectorySchema, QuickLaunchSchema
from . import util

CONFIG_FILE = os.getenv("VENTURE_CONFIG") or util.resolve("~/.config/venture.yaml")


class Config:
    directories: DirectorySchema = ["~"]
    exec: str = "code -r {path}"
    ui_provider: str = "rofi"
    show_icons: bool = True
    show_hidden: bool = False
    show_files: bool = True
    include_parent_folder: bool = False
    quicklaunch: QuickLaunchSchema = {}
    use_cache: bool = True

    def get(self, item, default=None):
        return getattr(self, item, default)

    @property
    def exists(self):
        return os.path.exists(CONFIG_FILE)

    def dict(self):
        return dict(
            {
                prop: getattr(self, prop)
                for prop in dir(self)
                if not prop.startswith("_")
                and not callable(getattr(self, prop))
                and not prop == "exists"
            }
        )

    def write(self):
        with open(CONFIG_FILE, "w") as f:
            f.write(self.dump())

    def dump(self):
        return yaml.dump(
            self.dict(),
            Dumper=yaml.CDumper,
        )

    @classmethod
    @timer("Loading Config")
    def from_file(cls, file):
        file = open(file)
        contents = file.read()
        file.close()
        data: dict[str, Any] = yaml.load(contents, Loader=yaml.CLoader)

        obj = cls()
        if not data:
            return obj

        for key, value in data.items():
            if key == "ui_provider" and value not in dir(obj):
                setattr(obj, value, {})

            setattr(obj, key, value)

        return obj

    @classmethod
    def dump_default(cls):
        return yaml.dump(
            Config.dict(Config),
            Dumper=yaml.CDumper,
        )


if os.path.isfile(CONFIG_FILE):
    logger.debug("Loading %s", CONFIG_FILE)
    config = Config.from_file(CONFIG_FILE)
else:
    logger.debug("Config File not found, loading defaults")
    config = Config()
