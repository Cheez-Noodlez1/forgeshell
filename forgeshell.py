#!/usr/bin/env python3
"""ForgeShell: a minimal interactive shell."""

from __future__ import annotations

import os
import shlex
import subprocess
from dataclasses import dataclass, field


@dataclass
class CommandResult:
    output: str = ""
    should_exit: bool = False


@dataclass
class ForgeShell:
    cwd: str = field(default_factory=os.getcwd)
    history: list[str] = field(default_factory=list)
    shell_executable: str = field(default_factory=lambda: os.environ.get("SHELL", "/bin/sh"))

    def prompt(self) -> str:
        return f"forgeshell:{self.cwd}$ "

    def run(self) -> int:
        print("ForgeShell started. Type 'help' for commands.")
        while True:
            try:
                raw = input(self.prompt())
            except EOFError:
                print()
                return 0

            result = self.execute(raw)
            if result.output:
                print(result.output)
            if result.should_exit:
                return 0

    def execute(self, raw: str) -> CommandResult:
        command = raw.strip()
        if not command:
            return CommandResult()

        self.history.append(command)

        if command in {"exit", "quit"}:
            return CommandResult("bye", should_exit=True)
        if command == "help":
            return CommandResult(self._help_text())
        if command == "pwd":
            return CommandResult(self.cwd)
        if command == "history":
            return CommandResult("\n".join(f"{i}: {cmd}" for i, cmd in enumerate(self.history, start=1)))
        if command.startswith("cd"):
            return self._cd(command)

        return self._run_external(command)

    def _help_text(self) -> str:
        return (
            "Built-ins:\n"
            "  help            Show this message\n"
            "  pwd             Show current directory\n"
            "  cd <path>       Change directory\n"
            "  history         Show command history\n"
            "  exit | quit     Exit ForgeShell\n"
            "\n"
            "External commands run in your system shell, so pipes, redirects, globs, "
            "and environment-variable expansion work as expected."
        )

    def _cd(self, command: str) -> CommandResult:
        try:
            parts = shlex.split(command)
        except ValueError as exc:
            return CommandResult(f"parse error: {exc}")

        if len(parts) == 1:
            target = os.path.expanduser("~")
        else:
            target = os.path.expanduser(parts[1])
            if not os.path.isabs(target):
                target = os.path.join(self.cwd, target)

        target = os.path.abspath(target)
        if not os.path.isdir(target):
            return CommandResult(f"cd: no such directory: {target}")

        self.cwd = target
        return CommandResult()

    def _run_external(self, command: str) -> CommandResult:
        proc = subprocess.run(
            command,
            cwd=self.cwd,
            check=False,
            capture_output=True,
            text=True,
            shell=True,
            executable=self.shell_executable,
        )

        output = (proc.stdout or "") + (proc.stderr or "")
        if proc.returncode != 0:
            output = output.rstrip("\n")
            if output:
                output += "\n"
            output += f"[exit {proc.returncode}]"
        return CommandResult(output.rstrip("\n"))


def main() -> int:
    shell = ForgeShell()
    return shell.run()


if __name__ == "__main__":
    raise SystemExit(main())
