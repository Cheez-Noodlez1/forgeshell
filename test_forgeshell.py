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

    def test_command_not_found(self):
        shell = ForgeShell(cwd="/")
        result = shell.execute("command_that_should_not_exist_123")
        self.assertIn("not found", result.output)
        self.assertIn("[exit", result.output)

    def test_pipe_and_system_shell_features(self):
        shell = ForgeShell(cwd="/")
        result = shell.execute("printf 'a\\nb\\n' | wc -l")
        self.assertEqual(result.output.strip(), "2")

    def test_env_variable_expansion(self):
        shell = ForgeShell(cwd="/")
        os.environ["FORGESHELL_TEST_VAR"] = "forge"
        result = shell.execute("printf '%s' $FORGESHELL_TEST_VAR")
        self.assertEqual(result.output, "forge")


if __name__ == "__main__":
    unittest.main()
