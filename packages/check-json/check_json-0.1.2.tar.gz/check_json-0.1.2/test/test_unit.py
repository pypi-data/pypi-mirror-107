"""
Unit tests for check_json
"""
import os
import tempfile

import nagiosplugin  # type:ignore
import pytest  # type:ignore

import check_json.__main__ as check_json  # type:ignore

# pylint: disable=no-self-use
# pylint: disable=redefined-outer-name
# pylint: disable=too-few-public-methods


def test_file_to_string():
    """Test"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tfile:
        test_string = "This is a string\nand another string"
        filename = tfile.name
        tfile.write(test_string)
    file_contents = check_json.file_to_string(tfile.name)
    os.remove(filename)
    assert file_contents == test_string


def test_gen_filter_name():
    """Test"""

    tfilters = [
        ('.somekey == "something" # filter-name', "filter-name"),
        (".somekey", "0"),
    ]
    for filter_string, filt_name in tfilters:
        assert (
            check_json.gen_filter_name(filter_string=filter_string, default="0")
            == filt_name
        )


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            ["--filter", ".somefilter", "--", "somefile.json"],
            {
                "fail_status": "warning",
                "filters": [".somefilter"],
                "jsonfile": "somefile.json",
                "verbosity": 0,
            },
        ),
        (
            [
                "--filter",
                ".somefilter",
                "--fail-status",
                "critical",
                "--",
                "somefile.json",
            ],
            {
                "fail_status": "critical",
                "filters": [".somefilter"],
                "jsonfile": "somefile.json",
                "verbosity": 0,
            },
        ),
    ],
)
def test_parse_args(test_input, expected):
    """Test"""
    assert vars(check_json.parse_args(test_input)) == expected


def test_parse_args_fail():
    """Test"""
    argv = [
        "--filter",
        ".somefilter",
        "critical",
    ]
    with pytest.raises(SystemExit):
        check_json.parse_args(argv)

    argv = [
        "--",
        "somefile.json",
    ]
    with pytest.raises(SystemExit):
        check_json.parse_args(argv)


class JsonfileManager:
    """Holds a JsonFile object and its inputs for testing"""

    def __init__(self):
        self.filters = [".key1", ".key2 # named-filter"]
        self.jsonstr = '{"key1": "value1",\n "key2": "value2"}'
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as jsonfile:
            jsonfile.write(self.jsonstr)
        self.obj = check_json.JsonFile(filters=self.filters, filepath=jsonfile.name)
        jsonfile.close()


@pytest.fixture
def jsonfile_manager():
    """Create a JsonFile object and save its inputs"""
    return JsonfileManager()


class TestJsonFile:
    """Test"""

    def test_init(self, jsonfile_manager):
        """Test that the JsonFile object is constructed as expected"""
        assert jsonfile_manager.obj.json == jsonfile_manager.jsonstr
        assert [
            f.filtobj.program_string for f in jsonfile_manager.obj.filters
        ].sort() == jsonfile_manager.filters.sort()
        assert jsonfile_manager.obj.filters[0].name == "filter0"
        assert jsonfile_manager.obj.filters[1].name == "named-filter"

    def test_probe(self, jsonfile_manager):
        """Test that probe returns all Metric objects"""
        for metric in jsonfile_manager.obj.probe():
            assert isinstance(metric, nagiosplugin.Metric)
