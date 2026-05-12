from mcdreforged.api.all import PluginServerInterface
from shell_executor.utils import tr


def on_load(s: PluginServerInterface, _):
    s.logger.info(tr(s, "on_load"))


def on_unload(s: PluginServerInterface, _):
    s.logger.info(tr(s, "on_load"))
