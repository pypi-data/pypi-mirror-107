from __future__ import annotations
import subprocess
import shlex
from typing import Mapping
from arc import CLI, ExecutionError, CommandType as ct
from arc.color import fg, effects
from arc.utils import timer

# Intiialzie the CLI first, so
# that the arc_logger gets properly setuo
cli = CLI(name="venture", version="1.2.3")

# pylint: disable=wrong-import-position
from .project_list import ProjectList
from .ui import get_ui_provider, OpenContext
from .ui.ui_provider import T
from . import util
from .tags import get_tags
from .config import config


def pick(items: Mapping[str, T], pick_config, open_context: OpenContext) -> T:
    provider_type = get_ui_provider(pick_config.ui_provider, open_context)
    provider = provider_type(items, config)
    choice: T | None = provider.run()
    if not choice:
        raise ExecutionError("No Valid Option Picked")

    return choice


def execute(path: str):
    command = config.exec.format(path=util.resolve(path))
    command = shlex.split(command)
    subprocess.run(command, check=True)


@timer("Project Loading")
def get_projects():
    if util.Cache.exists and config.use_cache:
        projects = util.Cache.read()
    else:
        projects = ProjectList(config.directories).projects
        if config.use_cache:
            util.Cache.write(projects)

    return projects


@cli.base()
@cli.command()
def run():
    """Open the venture selection menu"""
    projects = get_projects()
    choice = pick(projects, config, OpenContext.DEFAULT)
    execute(choice)


@cli.command()
def dump(force: bool = False):
    """Dump Default Config to ~/.config/venture.yaml if it does not exist"""
    if config.exists and not force:
        raise ExecutionError(
            "Configuration already exists. Run again with --force to overwrite"
        )

    with open(util.resolve("~/.config/venture.yaml"), "w+") as f:
        f.write(config.dump_default())


@cli.command()
def quicklaunch():
    """Open the Quick Launch Menu"""
    choice = pick(config.quicklaunch, config, OpenContext.QUICK_LAUNCH)
    execute(choice["path"])


@quicklaunch.subcommand("list")
def list_quicklaunch():
    """List quick-launch entries"""
    if len(config.quicklaunch) == 0:
        print(
            "No quick-launch items, add one with "
            f"{fg.GREEN}quicklaunch:add{effects.CLEAR}"
        )
        return

    print("Quicklaunch Items:")
    for name, values in config.quicklaunch.items():
        print(
            f"- {values['icon']}  {name} {fg.BLACK.bright}({values['path']}){effects.CLEAR}"
        )


@quicklaunch.subcommand()
def add(
    name: str,
    path: str,
    icon: str = "\uf192",
    tags: str = None,
    no_default_tags: bool = False,
):
    """\
    Add a new quick-launch entry

    Arguments:
    name=NAME            Display name for the quick-launch entry
    path=PATH            File path to launch when the entry is picked
    icon=ICON            Icon to display along with the name, optional
    tags=TAG1,TAG2       Comma-seperated values to tag the entry with.
                         Will be displayed along with the name of the
                         entry

    --no-default-tags    Disable the generation of default tags for this
                         quick-launch entry
    --disable-short-tags Disables Venture's tag shorthand matching feature.
                         use this if you want your tags to always look exactly
                         as you input them
    """

    all_tags = get_tags(
        path,
        tags.split(",") if tags else [],
        no_default_tags,
    )

    config.quicklaunch[name] = {
        "path": path,
        "icon": icon,
        "tags": list(all_tags),
    }
    config.write()

    print(f"{fg.GREEN}{name} Added!{effects.CLEAR}")


@quicklaunch.subcommand(command_type=ct.POSITIONAL)
def remove(name: str):
    """\
    Remove a quick-launch entry

    `quicklaunch:remove <NAME>`
    """
    if name not in config.quicklaunch:
        raise ExecutionError(f"{name} is not a quick-launch entry")

    config.quicklaunch.pop(name)
    with open(util.resolve("~/.config/venture.yaml"), "w+") as f:
        f.write(config.dump())
    print(f"{fg.GREEN}{name} Removed!{effects.CLEAR}")


@cli.command()
def cache(enable: bool = False, disable: bool = False):
    """\
    Interact with the Venture cache. if no arguments are provided,
    will display the current state of the cache

    The cache stores the data generated to display the main listing.
    For most reasonably sized outputs, the cache isn't necessary, but
    can still speed things up (if only by a fraction of a second). If
    you find running refresh to be annoying, try disabling it and review
    your performance.

    Arguments:
    --enable  enables the cache
    --disable disables the cache
    """
    if all((enable, disable)):
        print("Cannot enable and disable the cache at the same time!")
        return

    if enable:
        config.use_cache = True
        config.write()
        print("Cache Enabled")

    if disable:
        config.use_cache = False
        config.write()
        print("Cache Disabled")

    if not any((enable, disable)):
        state = fg.GREEN + "enabled" if config.use_cache else fg.RED + "disabled"
        print(f"Cache is {state}{effects.CLEAR}")
        print("Cache is present" if util.Cache.exists else "Cache empty")


@cache.subcommand()
def refresh():
    """Refreshes the contents of the cache"""
    projects = ProjectList(config.directories).projects
    util.Cache.write(projects)
    print("Cache Refreshed")
