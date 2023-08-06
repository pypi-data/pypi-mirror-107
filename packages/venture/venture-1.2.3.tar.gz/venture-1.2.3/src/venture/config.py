from typing import Any
import os
import yaml
from arc.utils import timer

from .types import DirectorySchema, QuickLaunchSchema
from . import util


class Config:
    __config_file = util.resolve("~/.config/venture.yaml")
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
        return os.path.exists(self.__config_file)

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
        with open(self.__config_file, "w") as f:
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


config_path = util.resolve("~/.config/venture.yaml")
if os.path.isfile(config_path):
    config = Config.from_file(config_path)
else:
    config = Config()
