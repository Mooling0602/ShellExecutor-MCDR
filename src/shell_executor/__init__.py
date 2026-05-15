from mcdreforged.api.all import PluginServerInterface

import shell_executor.runtime as rt
from shell_executor.command import (
    _current_proc,
    _proc_lock,
    _running_lock,
    command_register,
)
from shell_executor.utils import tr


def on_load(server: PluginServerInterface, _):
    rt.psi = server
    command_register(server)
    server.logger.info(tr(server, "on_load"))


def on_unload(server: PluginServerInterface):
    if not _running_lock.acquire(blocking=False):
        with _proc_lock:
            proc = _current_proc
        if proc is not None:
            try:
                proc.kill()
            except OSError:
                pass
    else:
        _running_lock.release()
    server.logger.info(tr(server, "on_unload"))
