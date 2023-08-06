import os


def resolve(path: str) -> str:
    return os.path.expanduser(path)


def pango_span(content, **kwargs):
    return (
        "<span "
        + " ".join(f'{key}="{value}"' for key, value in kwargs.items())
        + f">{content}</span>"
    )
