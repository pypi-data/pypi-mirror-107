"""Entry point for the hdev script."""
import pathlib
import sys
from argparse import ArgumentParser, Namespace
from functools import cached_property

from hdev import command


class HParser(ArgumentParser):
    """Overwrites ArgumentParser to control the `error` behaviour."""

    def error(self, message):
        """Change the default behavior to print help on errors."""
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


class HArgs(Namespace):  # pylint: disable=too-few-public-methods
    """A child of Namespace which adds HDev specific tweaks."""

    @cached_property
    def project(self):
        """Get the project associated with this call if any.

        This is based on the specified `--project-dir`.

        :return: A project
        :raise EnvironmentError: If the project directory cannot be found
            from the specified directory or any of it's parents.
        """
        # pylint: disable=import-outside-toplevel
        from hdev.model.project import Project

        # pylint: disable=no-member
        # The member is added by the parser
        return Project.from_child_dir(self._project_dir)


def create_parser():
    """Create the root parser for the `hdev` command."""

    parser = HParser()

    parser.add_argument(
        "--project-dir",
        metavar="PROJECT_DIR",
        dest="_project_dir",
        type=pathlib.Path,
        default=pathlib.Path("."),
        help="Path of the project's root. Defaults to .",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debugging info",
    )

    subparsers = parser.add_subparsers()

    for sub_command in [
        command.Alembic(),
        command.Clean(),
        command.Deps(),
        command.InstallPython(),
        command.PythonVersion(),
        command.Requirements(),
        command.Run(),
        command.Template(),
    ]:
        sub_command.add_to_parser(subparsers)

    return parser


def main():
    """Create an argsparse cmdline tools to expose hdev functionality.

    Main entry point of hdev
    """
    parser = create_parser()
    args = parser.parse_args(namespace=HArgs())

    # When we are using Python 3.7, this can be replaced with
    # add_argument(required=True) above
    try:
        handler = getattr(args, "handler")
    except AttributeError:
        parser.print_help()
        sys.exit(2)

    try:
        handler(args)

    except SystemExit:  # pylint: disable=try-except-raise
        # The handler is controlling the exit, and we should respect that
        raise

    except Exception as err:  # pylint: disable=broad-except
        if args.debug:
            raise

        # Another error has been raised, so dump it and print the help too
        print(f"Error: {err}\n")
        parser.print_usage()
        sys.exit(2)


if __name__ == "__main__":  # pragma: nocover
    main()
