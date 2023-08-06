from pathlib import Path
from .icons import icon
from .util import resolve

file_tags = {
    "py": "python",
    "rb": "ruby",
    "cr": "crystal",
    "rs": "rust",
    "js": "javascript",
    "c": "",
    "cpp": "",
    "cs": "",
    "css": "css",
    "go": "go",
    "html": "html",
    "php": "php",
    "r": "r",
    "swift": "swift",
    "ts": "typescript",
    "json": "json",
    "fish": "fish",
    "tsx": "react",
    "jsx": "react",
}


def get_icon_tag(suffix):
    file_tag = file_tags.get(suffix)
    if file_tag:
        return f"{icon(suffix)} {file_tag}"
    return None


def get_tags(filepath: str, user_tags: list[str], no_default_tags=False):
    filepath = resolve(filepath)
    if no_default_tags:
        return set(user_tags)

    path = Path(filepath)
    tags = set(
        map(lambda tag: get_icon_tag(tag) if tag in file_tags else tag, user_tags)
    )

    extension = path.suffix.lstrip(".")

    if path.is_file() and extension in file_tags:
        tags.add(get_icon_tag(extension))
    if "config" in str(path.absolute()):
        tags.add("\ue615 config")

    return tags
