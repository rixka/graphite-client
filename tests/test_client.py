import os
import pytest
from graphite_client import get_parser, is_valid_file


class TestArgHandler(object):

    @classmethod
    def setup_class(cls):
        cls.parser = get_parser()
        cls.filename = "delete.log"
        open(cls.filename, "w+").close()


    @classmethod
    def teardown_class(cls):
        os.remove(cls.filename)


    def test_file_exists(self):
        assert is_valid_file(self.parser, self.filename)


