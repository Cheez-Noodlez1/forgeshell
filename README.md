# ForgeShell

ForgeShell is a tiny, hackable interactive shell written in Python.

## Features

- Interactive prompt with current working directory context.
- Built-in commands:
  - `help`
  - `pwd`
  - `cd <path>`
  - `history`
  - `exit` / `quit`
- Falls back to external system commands when input is not built-in.

## Run

```bash
python3 forgeshell.py
```

## Example

```text
forgeshell:/workspace$ pwd
/workspace
forgeshell:/workspace$ echo hello
hello
forgeshell:/workspace$ history
1: pwd
2: echo hello
```
