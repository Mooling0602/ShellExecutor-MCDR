# ShellExecutor-MCDR
在 MCDR 控制台或游戏中快速执行 shell 命令。
> 需要 MCDR 权限等级达到 4 才能使用。

## 用法
使用 `!!shell <command>` 在默认 shell 环境中执行命令。
> 包含空格的命令应该用 `"` 引起来，例如：`!!shell "ls server/mods/"`

`!!shell` 的默认别名是 `$`，安装 [Command Aliases](https://mcdreforged.com/plugin/command_aliases) 来激活此功能（命令别名）。

## 注意
目前支持 Linux shell，插件可能在其他操作系统上无法正常工作。
> 欢迎在 Windows 上测试，如果发现任何问题，请随时提交 issue。