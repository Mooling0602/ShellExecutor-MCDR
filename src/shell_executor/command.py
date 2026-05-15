import os
import re
import subprocess
import threading
from pathlib import Path

from mcdreforged.api.all import (
    CommandContext,
    CommandSource,
    PluginServerInterface,
    QuotableText,
    RColor,
    SimpleCommandBuilder,
    new_thread,
)

import shell_executor.runtime as rt
from shell_executor.utils import tr, tr_to_rtr, update_json

EXECUTION_TIMEOUT = 30
ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]|\x1b\].*?\x07|\x1b[()][0-9A-Za-z]")
COMMAND_ALIASES_MAP = {"$": "!!shell"}
COMMAND_ALIASES_CONFIG = Path("config/command_aliases/config.json")


builder = SimpleCommandBuilder()

_running_lock = threading.Lock()
_proc_lock = threading.Lock()
_current_proc: subprocess.Popen | None = None


def command_register(server: PluginServerInterface):
    builder.arg("command", QuotableText)
    builder.register(server)
    update_json(COMMAND_ALIASES_CONFIG, COMMAND_ALIASES_MAP, "alias")


@builder.command("!!shell <command>")
def on_execute_shell_command(src: CommandSource, ctx: CommandContext):
    server = src.get_server().psi()
    if not src.has_permission(4):
        src.reply(tr(server, "permission_denied"))
        return
    command = ctx["command"]
    if not _running_lock.acquire(blocking=False):
        src.reply(tr_to_rtr(rt.psi, "process_already_running").set_color(RColor.red))
        return
    execute_shell(src, command)


@builder.command("!!shell status")
def show_shell_status(src: CommandSource):
    with _proc_lock:
        running = _current_proc is not None
    if running:
        src.reply(tr_to_rtr(rt.psi, "process_status_running").set_color(RColor.green))
    else:
        src.reply(tr_to_rtr(rt.psi, "process_status_idle").set_color(RColor.gray))


@builder.command("!!shell stop")
def stop_shell_process(src: CommandSource):
    with _proc_lock:
        proc = _current_proc
    if proc is not None:
        try:
            proc.kill()
        except OSError:
            pass
        src.reply(tr_to_rtr(rt.psi, "process_stopped").set_color(RColor.yellow))
    else:
        src.reply(tr_to_rtr(rt.psi, "no_process_running").set_color(RColor.gray))


@new_thread("ShellExecutor")
def execute_shell(src: CommandSource, command: str):
    global _current_proc
    try:
        proc = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            env={**os.environ, "TERM": "dumb"},
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        with _proc_lock:
            _current_proc = proc
        timed_out = False

        def kill_on_timeout():
            nonlocal timed_out
            timed_out = True
            proc.kill()

        timeout_timer = threading.Timer(EXECUTION_TIMEOUT, kill_on_timeout)
        timeout_timer.start()

        try:
            if proc.stdout is None:
                src.reply(tr_to_rtr(rt.psi, "process_error").set_color(RColor.red))
                return
            for line in iter(proc.stdout.readline, ""):
                src.reply(ANSI_ESCAPE.sub("", line.rstrip("\n")))
            proc.stdout.close()

            timeout_timer.cancel()
            return_code = proc.wait()
            if timed_out:
                src.reply(tr_to_rtr(rt.psi, "process_timeout").set_color(RColor.red))
            elif return_code != 0:
                src.reply(
                    tr_to_rtr(rt.psi, "process_exit_code", return_code).set_color(
                        RColor.gray
                    )
                )
        finally:
            timeout_timer.cancel()
    finally:
        with _proc_lock:
            _current_proc = None
        _running_lock.release()
