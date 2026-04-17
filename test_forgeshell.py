import os
import tempfile
import unittest

from forgeshell import ForgeShell


class ForgeShellTests(unittest.TestCase):
    def test_pwd_builtin(self):
        shell = ForgeShell(cwd="/tmp")
        result = shell.execute("pwd")
        self.assertEqual(result.output, "/tmp")

    def test_cd_builtin(self):
        with tempfile.TemporaryDirectory() as tempdir:
            shell = ForgeShell(cwd="/")
            result = shell.execute(f"cd {tempdir}")
            self.assertEqual(result.output, "")
            self.assertEqual(shell.cwd, os.path.abspath(tempdir))

    def test_unknown_command(self):
        shell = ForgeShell(cwd="/")
        result = shell.execute("command_that_should_not_exist_123")
        self.assertIn("command not found", result.output)


if __name__ == "__main__":
    unittest.main()
