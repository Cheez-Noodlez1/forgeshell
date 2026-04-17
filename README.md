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
- External commands run through your system shell for real shell behavior:
  - pipes (`|`)
  - redirects (`>`, `>>`, `<`)
  - globs (`*`)
  - environment variable expansion (`$HOME`)

## Run

```bash
python3 forgeshell.py
```

## Example

```text
forgeshell:/workspace$ pwd
/workspace
forgeshell:/workspace$ printf 'a\nb\n' | wc -l
2
forgeshell:/workspace$ echo $HOME
/root
```
