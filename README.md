- English
- [中文（简体）](README_zh_CN.md)

# ShellExecutor-MCDR
Quickly execute shell commands in MCDR console or in the game.
> Require MCDR permission level reach 4 to use.

## Usage
Use `!!shell <command>` to execute a command in default shell environment.
> Commands include spaces should be quoted by `"`, like this: `!!shell "ls server/mods/"`

Default alias for `!!shell` is `$`, install [Command Aliases](https://mcdreforged.com/plugin/command_aliases) to activate this feature.

## NOTE
- Support Linux shell at present, the plugin may not work properly on other operating systems.
> Test on Windows is welcome, feel free to submit an issue if you find any problem.

- Do not execute TUI binaries in ShellExecutor, it breaks rendering the MCDR console and even freezes it. I've no idea to solve this problem at present, if you have any solution, please submit an issue or a pull request, thanks.