import json

from kombu.log import get_logger

LOGGER = get_logger(__name__)


class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


def dict_upper(data):
    if isinstance(data, dict):
        return {key.upper(): dict_upper(value) for key, value in data.items()}
    else:
        return data


def to_json(data):
    return json.dumps(data, ensure_ascii=False, default=str)


def from_json(data):
    return json.loads(data)


def to_file(data, file):
    return json.dump(data, file, ensure_ascii=False, default=str)


def from_file(file):
    return json.load(file)


def to_format_json(data):
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


def to_format_file(data, file):
    return json.dump(data, file, indent=2, ensure_ascii=False, default=str)
