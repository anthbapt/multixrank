"""
Example of module documentation which can be
multiple-lined
"""

import multixrank
import os
import pathlib
import tempfile

class PathManager:

    def __init__(self):
        self.tempdir = None

    @classmethod
    def get_tempdir(self):
        """
        Find the Src directory of the project

        :return: the output leading to the src file of the project
        """
        if self.tempdir is None:
            self.tempdir = tempfile.mkdtemp()
        pathlib.Path(self.tempdir).mkdir(parents=True, exist_ok=True)
        return self.tempdir

    @classmethod
    def get_doc_path(cls):
        """
        Returns the document folder

        :return: config_path to the document folder
        """

        doc_path = os.path.join(cls.get_package_path(), "../doc")
        return doc_path

    @classmethod
    def get_project_path(cls):
        """
        Returns the config_path to the project root

        :return: config_path to the root of the project
        """

        project_path = os.path.join(cls.get_package_path(), "..")
        return project_path

    @staticmethod
    def get_package_path():
        """
        Returns the multixrank.__path__[0]

        :return: config_path to the package
        """

        package_path = multixrank.__path__[0]
        return package_path

    @classmethod
    def get_test_path(cls):
        """
        Find the tests output of the project

        :return: the output leading to the tests output of the project
        """

        test_path = os.path.join(cls.get_package_path(), "tests")
        return test_path
