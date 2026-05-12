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
