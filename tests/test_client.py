import os
import pytest
import graphite_client as gc


class TestArgHandler(object):

    @classmethod
    def setup_class(cls):
        cls.parser = gc.get_parser()
        cls.filename = 'delete.log'
        open(cls.filename, 'w+').close()

    @classmethod
    def teardown_class(cls):
        os.remove(cls.filename)

    def test_file_exists(self):
        assert gc.is_valid_file(self.parser, self.filename)

    def test_file_missing(self):
        with pytest.raises(SystemExit) as exc:
            gc.is_valid_file(self.parser, 'missing.log')
        assert exc.value.code == 2

