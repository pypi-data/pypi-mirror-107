from .dnc_sdk import MobioDNCSDK


def int_or_str(value):
    try:
        return int(value)
    except ValueError:
        return value


__version__ = "1.0.1"
VERSION = tuple(map(int_or_str, __version__.split(".")))

__all__ = [MobioDNCSDK]
