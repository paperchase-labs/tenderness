---
icon: lucide/rocket
hide:
  - path
---

# Install

## Prerequisites

**tenderness** depends on [pycairo](https://pycairo.readthedocs.io/en/latest/getting_started.html) and [PyGObject](https://pygobject.gnome.org/getting_started.html), which require system libraries before installing. 

## Virtual environment

[uv](https://docs.astral.sh/uv/) is recommended, but any virtual environment manager works.

=== "uv"
    ```bash
    uv venv --python 3.13
    source .venv/bin/activate
    ```

## Installation

=== "uv"

    ```bash
    uv pip install tenderness
    ```
=== "pip"

    ```bash
    pip install tenderness
    ```

## Validate installation

[`scripts/debug_env.py`](https://github.com/paperchase-labs/tenderness/blob/main/scripts/debug_env.py) checks that PyGObject, Cairo, and Pango are correctly installed and able to render:

=== "uv"

    ```bash
    uv run scripts/debug_env.py
    ```
=== "python"

    ```bash
    python scripts/debug_env.py
    ```

## Troubleshooting

### Minimum system library versions

**tenderness** requires the underlying C libraries to be reasonably recent:

- Cairo `>= 1.18`
- Pango `>= 1.57`

Older versions may be missing APIs that `pycairo`/PyGObject bindings or **tenderness** itself rely on. If [`scripts/debug_env.py`](https://github.com/paperchase-labs/tenderness/blob/main/scripts/debug_env.py) fails or renders incorrectly, check your installed versions (e.g. `pkg-config --modversion cairo pango`) and upgrade via your system package manager (Homebrew, apt, etc.) if needed.

### macOS: `GLib`/`GObject` import errors

On macOS, importing `gi.repository.GLib` may fail even though GLib is installed via Homebrew:

```
GLib-GIRepository-WARNING **: Failed to load shared library 'libgobject-2.0.0.dylib' referenced by the typelib: dlopen(libgobject-2.0.0.dylib, 0x0009): tried: 'libgobject-2.0.0.dylib' (no such file), ...
GLib-GIRepository-WARNING **: Failed to load shared library 'libglib-2.0.0.dylib' referenced by the typelib: dlopen(libglib-2.0.0.dylib, 0x0009): tried: 'libglib-2.0.0.dylib' (no such file), ...
Traceback (most recent call last):
  ...
  File ".venv/lib/python3.13/site-packages/gi/overrides/__init__.py", line 209, in override
    assert g_type != TYPE_NONE
AssertionError
```

**Cause**: GObject-Introspection typelibs reference `libglib`/`libgobject` by bare filename and rely on the dynamic linker's default search path to resolve them — but macOS's `dyld` no longer searches Homebrew's lib directory (`/usr/local/lib` on Intel, `/opt/homebrew/lib` on Apple Silicon) by default. PyGObject `>= 3.56` surfaces this as a hard `AssertionError` on import; `3.50.2` only logs the warning without crashing.

=== "Set DYLD_FALLBACK_LIBRARY_PATH (recommended)"

    Point the dynamic linker at Homebrew's lib directory so it can find the libraries:

    ```bash
    export DYLD_FALLBACK_LIBRARY_PATH="/usr/local/lib:/opt/homebrew/lib"
    ```

    Add this to your shell profile for a permanent, global fix, or scope it to the project with a `.env` file and `uv run --env-file .env ...` so it doesn't leak into your global shell environment.

=== "Pin PyGObject to 3.50.2"

    If you don't need the latest PyGObject, pinning avoids the crash without any environment changes:

    ```bash
    uv pip install "PyGObject==3.50.2"
    ```

    This only hides the crash — the underlying `dyld` search-path gap is still there, and later PyGObject releases may reintroduce the failure. Prefer the `DYLD_FALLBACK_LIBRARY_PATH` fix above where possible.

