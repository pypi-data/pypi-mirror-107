import tempfile
import typing


def save_yaml_to_file(s: str, delete: bool = True) -> tempfile.NamedTemporaryFile:
    tempf = tempfile.NamedTemporaryFile(suffix=".yml", delete=delete)
    write_to_file(s, tempf.name)
    return tempf


def write_to_file(s: str, filename: str) -> None:
    with open(filename, "w") as f:
        f.write(s)


def merge_dicts(
    dict1: typing.Dict[typing.Any, typing.Any],
    dict2: typing.Dict[typing.Any, typing.Any],
) -> typing.Dict[typing.Any, typing.Any]:
    """ Recursively merges dict2 into dict1 """
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        return dict1
    for k in dict2:
        if k in dict1:
            dict1[k] = merge_dicts(dict1[k], dict2[k])
        else:
            dict1[k] = dict2[k]
    return dict1
