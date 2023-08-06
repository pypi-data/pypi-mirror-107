"""A model object for a checked out Hypothesis project."""

import json
from enum import Enum
from json import JSONDecodeError
from pathlib import Path

from hdev.configuration import Configuration
from hdev.requirements.requirements_file import RequirementsFile
from hdev.requirements.setup_file import SetupConfigFile


class Project:
    """A checked out Hypothesis project (app or lib)."""

    # For easy mocking
    root_dir = None
    type = None

    class Type(Enum):
        APP = "app"
        LIBRARY = "library"

    def __init__(self, root_dir, type_=None):
        """Initialize a Project object.

        :param root_dir: The root of the project
        :param type_: The type of the project (if this is not specified it will
            be automatically determined)
        """
        self.root_dir = Path(root_dir).absolute()
        self.type = self.Type(type_) if type_ else self.get_type()

    @property
    def config(self):
        return Configuration.load(self.root_dir / "pyproject.toml")

    def requirements(self):
        """Get a dict of lists of requirements."""
        if self.type == self.Type.APP:
            # Should be reading from pyproject.toml to get the requirements dir?
            req_files = RequirementsFile.find(self.root_dir / "requirements")

            return {
                req_file.stem: list(req_file.plain_dependencies)
                for req_file in req_files
            }

        return SetupConfigFile(self.root_dir / "setup.cfg").requirements()

    _PRODUCT_ROOT_FILES = (
        "tox.ini",
        "setup.cfg",
        "setup.py",
        "pyproject.toml",
        "Makefile",
        ".cookiecutter.json",
    )

    @classmethod
    def from_child_dir(cls, dir_path):
        dir_path = Path(dir_path).absolute()
        search_dir = Path(dir_path)
        if not search_dir.exists():
            raise NotADirectoryError(search_dir)

        while not cls.is_product_dir(search_dir):
            if search_dir == search_dir.parent:
                raise EnvironmentError(
                    f"Cannot find a project in any parent directory of '{dir_path}'"
                )

            search_dir = search_dir.parent

        return Project(search_dir)

    @classmethod
    def is_product_dir(cls, dir_path):
        """Check if a particular directory looks like a project root."""

        return any(
            (dir_path / filename).exists() for filename in cls._PRODUCT_ROOT_FILES
        )

    def get_type(self):
        """Get the type of this project (app or library)."""

        # This will obviously all change as our boiler-plate does
        if not self.is_product_dir(self.root_dir):
            raise EnvironmentError(
                f"Directory {self.root_dir} does not look like " "a Hypothesis product"
            )

        cookie_cutter = self.root_dir / ".cookiecutter.json"
        if not cookie_cutter.exists():
            return Project.Type.APP

        try:
            data = json.loads(cookie_cutter.read_text("utf-8"))
        except JSONDecodeError as err:
            raise EnvironmentError("Cannot parse cookiecutter file") from err

        if data["_template"] == "gh:hypothesis/h-cookiecutter-pypackage":
            return Project.Type.LIBRARY

        if data["_template"] == ".":
            # This is a cookie cutter template itself, for now that means a lib
            return Project.Type.LIBRARY

        raise EnvironmentError(
            f"Cannot work out product type from cookie cutter: '{data['_template']}'"
        )
