# ShellExecutor-MCDR
It's a [MCDReforged](https://github.com/MCDReforged/MCDReforged) plugin project, and based on Python.

Add more useful informations to this file as you need.

## Pay attension to
- Think and reply user with his or her language, but write commit messages or comments only by English, it's helpful for i18n.
- Do type linting, but comments or docstring is not necessary, write these only when you need.
- When import modules, using absolute paths instead of relative paths.
- Use `from mcdreforged.api.all import ...` to import apis from MCDReforged, and maintain the compatibility with earlier versions.
- For translations of this plugin, see the source code in `shell_executor.utils`.
- Write semantic commit messages.

## Best implementations
### Unused arguments in a function
Use `_` to express a unused argument.

E.g. in plugin public method `on_load()`, the required arguments is `server: PluginServerInterface` and `prev_module: Any`. Usually the `prev_module` argument is unused.

In this case, write code like this:

```python
from mcdreforged.api.all import PluginServerInterface


def on_load(server: PluginServerInterface, _):
    pass
```

But should not like this:

```python
# Some content omitted.
def on_load(server, prev_module):
    pass
```

## TEST
### Check code
Do not compile codes, it causes `__pycache__` shits.

Use tools like `ty`, `ruff` to check any error in source code, if LSP tools usable from agent tool, use them either.

Here is a simple way to check:

```sh
ty check src
ruff check src
```

### Test the source code
Make sure the tests module is existing, like this:

```python
.
├── src
│   └── ...
├── tests
...
```

Then write unittest submodules in `tests/`.

### Test in MCDR running instance
Follow the user's promt and attach to MCDR's working directory. Then, use `mcdreforged pack` to build a plugin package, and move to `/path/to/mcdr-server/plugins/`. In MCDR console, execute `!!MCDR reload plg` or `!!MCDR plg load <filename>`.

Now you can see what happened in console, and check if the plugin is operating normally.
