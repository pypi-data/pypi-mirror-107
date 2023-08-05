# pylint: disable=unused-variable


import pytest

from datafiles import formats
from datafiles.utils import dedent


def describe_serialize():
    @pytest.fixture
    def data():
        return {'key': "value", 'items': [1, 'a', None]}

    def describe_yaml():
        def it_indents_blocks_by_default(expect, data):
            text = formats.serialize(data, '.yaml')
            expect(text) == dedent(
                """
            key: value
            items:
              - 1
              - a
              -
            """
            )


def describe_deserialize():
    @pytest.fixture
    def path(tmp_path):
        path = tmp_path / "sample"
        path.write_text("")
        return path

    def describe_yaml():
        def with_empty_file(expect, path):
            data = formats.deserialize(path, '.yaml')
            expect(data) == {}

    def describe_json():
        def with_empty_file(expect, path):
            path.write_text("{}")
            data = formats.deserialize(path, '.json')
            expect(data) == {}

    def describe_toml():
        def with_empty_file(expect, path):
            data = formats.deserialize(path, '.toml')
            expect(data) == {}

    def with_unknown_extension(expect, path):
        with expect.raises(ValueError):
            formats.deserialize(path, '.xyz')
