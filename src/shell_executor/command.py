from mcdreforged.api.all import (
    PluginServerInterface,
    CommandContext,
    CommandSource,
    QuotableText,
    SimpleCommandBuilder,
)
from shell_executor.utils import tr

builder = SimpleCommandBuilder()


def command_register(s: PluginServerInterface):
    builder.arg("command", QuotableText)
    builder.register(s)


@builder.command("!!shell <command>")
def on_execute_shell_command(src: CommandSource, ctx: CommandContext):
    s = src.get_server().psi()
    if not src.has_permission(4):
        src.reply(tr(s, "permission_denied"))
    command = ctx["command"]
    src.reply("Not implemented yet!")
