import os
import functools


def resolve(path: str) -> str:
    return os.path.expanduser(path)


def pango_span(content, **kwargs):
    return (
        "<span "
        + " ".join(f'{key}="{value}"' for key, value in kwargs.items())
        + f">{content}</span>"
    )


def catch(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise Cache.CacheError(f"Cache {func.__name__} failed") from e

    return wrapper


class Cache:
    cache_path = "/tmp/venture-cache"

    class CacheError(Exception):
        ...

    @classmethod
    @catch
    def read(cls):
        f = open(cls.cache_path, "r")
        data = dict([line.split("=") for line in f.readlines()])
        f.close()
        return data

    @classmethod
    @catch
    def write(cls, data: dict):
        f = open(cls.cache_path, "w")
        f.write("\n".join("=".join(item) for item in data.items()))
        f.close()

    @classmethod
    @property
    def exists(cls):
        return os.path.isfile(cls.cache_path)
