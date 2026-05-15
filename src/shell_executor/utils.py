import json
from pathlib import Path

from mcdreforged.api.all import PluginServerInterface, RTextMCDRTranslation


def tr(
    server: PluginServerInterface, tr_key: str, return_str: bool = False, *args
) -> str | RTextMCDRTranslation:
    """Optimized method for using `PluginServerInterface.rtr()` provided by MCDR.

    :param server: A `PluginServerInterface()` instance, will be used to use MCDR interfaces and get the plugin id.
    :param tr_key: Translation key string.
    :param return_str: If returns a `str` object as result.
    :param *args: Used for template strings.

    :return: A `str` object or a `RTextMCDRTranslation` instance.
    """
    plg_id = server.get_self_metadata().id
    if tr_key.startswith(f"{plg_id}"):
        translation = server.rtr(f"{tr_key}")
    else:
        if tr_key.startswith("#"):
            translation = server.rtr(tr_key.replace("#", ""), *args)
        else:
            translation = server.rtr(f"{plg_id}.{tr_key}", *args)
    if return_str:
        tr_to_str: str = str(translation)
        return tr_to_str
    else:
        return translation


def tr_to_str(server: PluginServerInterface, tr_key: str, *args) -> str:
    """Call `tr()` and require a :class:`str` output."""
    return str(tr(server, tr_key, True, *args))


def tr_to_rtr(
    server: PluginServerInterface, tr_key: str, *args
) -> RTextMCDRTranslation:
    """Call `tr()` and require a :class:`RTextMCDRTranslation` instance."""
    rtr = tr(server, tr_key, False, *args)
    assert isinstance(rtr, RTextMCDRTranslation)
    return rtr


def update_json(
    file_path: str | Path,
    data: dict,
    key_path: str | None = None,
    encoding: str | None = None,
    encoding_fallbacks: list[str] | None = None,
):
    """Merge a dict object to a JSON file.

    If merged dict is existing, it will be overwritten.

    :param file_path: The path of the JSON file.
    :param data: The dict object to be written.
    :param key_path: A dot-separated string representing the nested path to update within the JSON structure, if `None`, the top-level will be updated.
    :param encoding: The encoding of the JSON file, default is UTF-8.
    :param encoding_fallbacks: A list of fallback encodings, will be used if the specified encoding fails, default is `["utf-8", "gbk"]`.
    """
    if encoding_fallbacks is None:
        encoding_fallbacks = ["utf-8", "gbk"]
    file_path = Path(file_path)
    if not file_path.exists():
        return
    for enc in [encoding] + encoding_fallbacks:
        try:
            with file_path.open("r", encoding=enc) as f:
                existing_data = json.load(f)
            break
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
    else:
        existing_data = {}
    if key_path is not None:
        keys = key_path.split(".")
        current = existing_data
        for key in keys[:-1]:
            current = current.setdefault(key, {})
        current[keys[-1]] = data
    else:
        existing_data.update(data)
    with file_path.open("w", encoding=encoding or "utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
