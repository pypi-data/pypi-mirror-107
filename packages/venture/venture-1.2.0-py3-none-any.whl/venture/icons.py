from typing import Dict, Optional

# Uses Nerd Fonts Icons
__icons: Dict[str, str] = {
    "directory": "",
    "default": "",
    "py": "",
    "rb": "",
    "cr": "",
    "rs": "",
    "js": "",
    "c": "ﭰ",
    "cpp": "ﭱ",
    "cs": "",
    "css": "",
    "go": "ﳑ",
    "html": "",
    "php": "",
    "r": "ﳒ",
    "swift": "ﯣ",
    "ts": "ﯤ",
    "json": "",
    "zip": "遲",
    "fish": "",
    "tsx": "",
    "jsx": "",
}


def icon(name: str) -> Optional[str]:
    """Get an icon associated with a filename,
    returns the default if it doesn't exist"""
    name = name.lstrip(".")
    return __icons.get(name)
